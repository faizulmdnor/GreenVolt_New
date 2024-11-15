# Import necessary libraries
from matplotlib import pyplot as plt
import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX

from GreenVolt_db import greenvolt
from sklearn.linear_model import LinearRegression
from statsmodels.tsa.arima.model import ARIMA
import numpy as np
import mplcursors

def plot_sales_chart(df, title):
    '''
    :param df:
    :param title:
    :return:
    '''

    df['Timeline'] = df['Timeline'].astype(str)
    df['TotalSales'] = df['TotalSales'].astype(float).round(2)
    df['Predicted_Sales'] = df['Predicted_Sales'].astype(float).round(2)

    start = min(df['Timeline'])
    end = max(df['Timeline'])

    plt.plot(df['Timeline'], df['TotalSales'],  color='b', marker='s', linewidth=3)
    plt.plot(df['Timeline'], df['Predicted_Sales'],  color='b', marker='s', linestyle='dotted')
    plt.xlabel(f'{title}')
    plt.ylabel('Sales(RM)')
    plt.title(f"{title}: Total Sales and Predicted Sales, from {start} to {end}")
    plt.legend()
    plt.grid(True)  # Add gridlines

    cursor = mplcursors.cursor(hover=True)
    cursor.connect(
        "add", lambda sel: sel.annotation.set_text(f"{sel.artist.get_label()}: {sel.target[1]:.2f}")
    )

def arima_model(colname, forecast_period, df, d):

    '''
    order=(0, 0, 1): This specifies the parameters of the ARIMA model:
    AR (AutoRegressive): The first parameter (0) is the order of the autoregressive part. An AR(0) means that the model does not use any past values of the series for predictions. In other words, it does not include any lag terms (previous values in the series) in its calculation.
    I (Integrated): The second parameter (0) represents the order of differencing required to make the series stationary. A value of 0 means no differencing is applied, implying that the series is already stationary (its statistical properties do not change over time).
    MA (Moving Average): The third parameter (1) is the order of the moving average part. An MA(1) model uses the past residual errors (the differences between the predicted and actual values) for forecasting. This means the model will use the previous period's error to adjust future predictions.
    :param colname:
    :param forecast_period:
    :param df:
    :param d:
    :return:
    '''

    """    
    AutoRegressive = 1
    Integrated = 0
    MovingAverage = 0
    """

    # Fit ARIMA model
    arima = ARIMA(df[colname], order=(1, 0, 0))
    model_arima = arima.fit()
    model = model_arima

    # Forecast future periods
    forecast = model.forecast(steps=forecast_period)
    predicted_sales = forecast.tolist()
    actual = df[f'{colname}'].to_list()
    actual_predicted = actual + predicted_sales
    formatted_actual_predicted = [f"{value:.2f}" for value in actual_predicted]

    # Generate forecast index based on frequency ('Y' for years, 'M' for months)
    if d == 'Year':
        freq = 'Y'
        df['Timeline'] = pd.to_datetime(df['Timeline']).dt.strftime('%Y')
        timeline = pd.date_range(min(df['Timeline']), periods=len(df)+forecast_period, freq=freq)
        timeline = timeline.strftime("%Y")

    elif d == 'Month':
        freq = 'M'
        df['Timeline'] = pd.to_datetime(df['Timeline']).dt.strftime('%Y-%m')
        timeline = pd.date_range(min(df['Timeline']), periods=len(df) + forecast_period, freq=freq)
        timeline = timeline.strftime("%Y-%m")

    else:
        raise ValueError("Parameter 'd' should be either 'Year' or 'Month'.")

    # Create forecast DataFrame
    forecast_df = pd.DataFrame({'Timeline':timeline,
                                'Predicted_Sales': formatted_actual_predicted})

    return forecast_df

def sarimax_model(colname, forecast_period, df, d):
    '''

    :param colname:
    :param forecast_period:
    :param df:
    :param d:
    :return:
    '''

    """ 
    AutoRegressive = 1
    Integrated = 1
    MovingAverage = 1
    """

    # Fit SARIMAX model
    model_sarima = SARIMAX(df[colname], order=(1, 1, 1), seasonal_order=(1, 1, 1, 12))
    model_sarima_fitted = model_sarima.fit(disp=False)
    model = model_sarima_fitted

    # Forecast future periods
    forecast = model.forecast(steps=forecast_period)
    predicted_sales = forecast.tolist()
    actual = df[f'{colname}'].to_list()
    actual_predicted = actual + predicted_sales
    formatted_actual_predicted = [f"{value:.2f}" for value in actual_predicted]

    # Generate forecast index based on frequency ('Y' for years, 'M' for months)
    if d == 'Year':
        freq = 'Y'
        df['Timeline'] = pd.to_datetime(df['Timeline']).dt.strftime('%Y')
        timeline = pd.date_range(min(df['Timeline']), periods=len(df) + forecast_period, freq=freq)
        timeline = timeline.strftime("%Y")

    elif d == 'Month':
        freq = 'M'
        df['Timeline'] = pd.to_datetime(df['Timeline']).dt.strftime('%Y-%m')
        timeline = pd.date_range(min(df['Timeline']), periods=len(df) + forecast_period, freq=freq)
        timeline = timeline.strftime("%Y-%m")

    else:
        raise ValueError("Parameter 'd' should be either 'Year' or 'Month'.")

    # Create forecast DataFrame
    forecast_df = pd.DataFrame({'Timeline': timeline,
                                'Predicted_Sales': formatted_actual_predicted})

    return forecast_df



# Step 1: Load Data from Database
sales_table = 'Monthly_Sales'
df_sales = greenvolt.query_table(sales_table)  # Query monthly sales data from the database

# Step 2: Data Preparation
# Convert 'YearMonth' to datetime and round 'totalSales' to 2 decimal places for consistency
df_sales['YearMonth'] = pd.to_datetime(df_sales['YearMonth'])
df_sales['Year_Sales'] = df_sales['YearMonth'].dt.strftime("%Y")

# Step 3: Aggregate Sales Data
# Group and sum sales by year and round to 2 decimal places, then rename the column for clarity
df_sales_Years = df_sales.groupby(by=['Year_Sales']).agg({'totalSales': 'sum'}).round(2)
df_sales_Years = df_sales_Years.rename(columns={'totalSales': 'TotalSales_Year'})
df_sales_Years['Year'] = df_sales_Years.index
df_sales_Years.reset_index(drop=True, inplace=True)
df_sales_Years['Timeline'] = pd.to_datetime(df_sales_Years['Year'])

# Group and sum sales by month and rename column
df_sales_Months = df_sales.groupby(by=['YearMonth']).agg({'totalSales': 'sum'}).round(2)
df_sales_Months = df_sales_Months.rename(columns={'totalSales': 'TotalSales_Month'})
df_sales_Months['YearMonth'] = df_sales_Months.index
df_sales_Months.reset_index(drop=True, inplace=True)
df_sales_Months['Timeline'] = pd.to_datetime(df_sales_Months['YearMonth'])
df_sales_Months['YearMonth'] = df_sales_Months['YearMonth'].dt.strftime("%Y-%m")

# ARIMA
df_sales_Years_Predicted_arima = arima_model(colname='TotalSales_Year', forecast_period=3, df=df_sales_Years, d='Year')
df_sales_Months_Predicted_arima = arima_model(colname='TotalSales_Month', forecast_period=3, df=df_sales_Months, d='Month')
df_sales_Months_Predicted_arima['TotalSales'] = df_sales_Months['TotalSales_Month'].apply(lambda value: f"{value:.2f}")
df_sales_Years_Predicted_arima['TotalSales'] = df_sales_Years['TotalSales_Year'].apply(lambda value: f"{value:.2f}")

# SARIMAX
df_sales_Years_Predicted_sarimax = sarimax_model(colname='TotalSales_Year', forecast_period=3, df=df_sales_Years, d='Year')
df_sales_Months_Predicted_sarimax = sarimax_model(colname='TotalSales_Month', forecast_period=3, df=df_sales_Months, d='Month')
df_sales_Months_Predicted_sarimax['TotalSales'] = df_sales_Months['TotalSales_Month'].apply(lambda value: f"{value:.2f}")
df_sales_Years_Predicted_sarimax['TotalSales'] = df_sales_Years['TotalSales_Year'].apply(lambda value: f"{value:.2f}")

# Step 4: Calculate Moving Averages
# Calculate a 3-month rolling average for monthly sales, rounded to 2 decimal places
df_sales_Months['Mov Avg'] = df_sales_Months['TotalSales_Month'].rolling(window=3).mean().round(2)
df_sales_Years['Mov Avg'] = df_sales_Years['TotalSales_Year'].rolling(window=4).mean().round(2)


plt.ion()
plt.figure()
plot_sales_chart(df=df_sales_Months_Predicted_arima, title='ARIMA Model: Month')

plt.figure()
plot_sales_chart(df=df_sales_Years_Predicted_arima, title='ARIMA Model: Year')

plt.figure()
plot_sales_chart(df=df_sales_Months_Predicted_sarimax, title='SARIMAX Model: Month')

plt.figure()
plot_sales_chart(df=df_sales_Years_Predicted_sarimax, title='SARIMAX Model: Year')
plt.ioff()
plt.show()


