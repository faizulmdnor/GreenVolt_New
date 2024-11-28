import pandas as pd
from matplotlib import pyplot as plt
from GreenVolt_Predicted import arima_predicted
from GreenVolt_db import greenvolt

data = greenvolt.query_table('Monthly_Sales')
groupby_YearMonth = data.groupby(by=['YearMonth']).agg({'totalSales': 'sum'}).round(2)
groupby_YearMonth.reset_index(inplace=True)
groupby_YearMonth['date'] = pd.to_datetime(groupby_YearMonth['YearMonth'])

groupby_YearMonth_arima = groupby_YearMonth
groupby_YearMonth_sarimax = groupby_YearMonth

df_PredictedSales_Monthly = arima_predicted.arima_model(forecast_period = 6, df_arima=groupby_YearMonth_arima, colname='totalSales', period_name='Month')
df_PredictedSales_Monthly['date'] = pd.to_datetime(df_PredictedSales_Monthly['date']).dt.strftime('%Y-%m')

plt.figure(1)
plt.plot(df_PredictedSales_Monthly['date'], df_PredictedSales_Monthly['totalSales'], color='b', marker='s', label='total sales')
plt.plot(df_PredictedSales_Monthly['date'], df_PredictedSales_Monthly['Predicted_totalSales'], color='r', marker='s', linestyle='dotted', label='predicted total sales')


df_PredictedSales_Monthly_sarimax = arima_predicted.sarimax_model(forecast_period = 6, df_sarimax=groupby_YearMonth_sarimax, colname='totalSales', period_name='Month')
df_PredictedSales_Monthly_sarimax['date'] = pd.to_datetime(df_PredictedSales_Monthly_sarimax['date']).dt.strftime('%Y-%m')

plt.figure(2)
plt.plot(df_PredictedSales_Monthly_sarimax['date'], df_PredictedSales_Monthly_sarimax['totalSales'], color='y', marker='s', label='total sales')
plt.plot(df_PredictedSales_Monthly_sarimax['date'], df_PredictedSales_Monthly_sarimax['totalSales'], color='g', marker='s', label='predicted sales')

plt.show()