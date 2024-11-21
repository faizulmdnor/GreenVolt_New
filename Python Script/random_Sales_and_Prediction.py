import pandas as pd
import random
from statsmodels.tsa.arima.model import ARIMA
from matplotlib import pyplot as plt

def create_data():
    # Define customer data
    customers = {'customer_id': [1001, 1002, 1003, 1004, 1005, 1006],
                 'customer': ['AT&S', 'OSRAM', 'First Solar', 'Celestica', 'Intel', 'Siltera']}

    # Create a dictionary to map customer_id to customer names
    customer_map = dict(zip(customers['customer_id'], customers['customer']))

    # Generate date range
    dates = pd.date_range('2022-01-01', '2024-10-31')
    datelist = dates.tolist()

    # Initialize list for sales data
    sales_data = []

    # Loop over each date and generate random sales data
    for date in datelist:
        num_entries = random.randint(0, 5)  # Random number of entries per date

        # Initialize a set to track selected customers for the day
        selected_customers = set()

        for _ in range(num_entries):
            # Randomly select a customer_id but ensure it's not already selected today
            customer_id = random.choice(customers['customer_id'])

            # Keep selecting a customer until one is found that's not already selected for this day
            while customer_id in selected_customers:
                customer_id = random.choice(customers['customer_id'])

            # Add the selected customer to the set
            selected_customers.add(customer_id)

            # Get the customer name based on customer_id
            customer_name = customer_map[customer_id]

            # Generate random sales value
            sales = round(random.uniform(100.00, 5000.00), 2)

            # Append data to sales_data list
            sales_data.append(
                {'Date': date, 'Customer_id': customer_id, 'Customer_name': customer_name, 'total_sales': sales})

    # Create DataFrame from sales data
    total_sales = pd.DataFrame(sales_data)

    # Reset index for the DataFrame
    total_sales.reset_index(drop=True, inplace=True)

    # Display the DataFrame
    total_sales.to_csv('../Data Files/total_charges.csv', index=False)
    return total_sales

def plot_graph(title, df, figure):
    plt.figure(figure)
    plt.plot(df['Timeline'], df['total_sales'].astype(float), color='b', marker='x')
    plt.plot(df['Timeline'], df['Predicted_Sales'].astype(float), color='r', marker='s', linestyle='dotted')
    plt.title(title)
    plt.ylabel('Sales(RM)')
    plt.xlabel('Month')
    plt.legend()

def arima_prediction(df):
    forecast_period = 6
    arima = ARIMA(df['total_sales'], order=(0, 0, 6))
    model_arima = arima.fit()

    forecast = model_arima.forecast(steps=forecast_period)
    predicted_sales = forecast.tolist()
    actual = df['total_sales'].tolist()
    actual_predicted = actual + predicted_sales
    formatted_actual_predicted = [f"{value:.2f}" for value in actual_predicted]
    df['total_sales'] = [f"{value:.2f}" for value in df['total_sales']]
    df['Timeline'] = pd.to_datetime(df['Timeline']).dt.strftime('%Y-%m')
    timeline = pd.date_range(min(df['Timeline']), periods=len(df) + forecast_period, freq='ME')
    timeline = timeline.strftime("%Y-%m")
    forecast_df = pd.DataFrame({'Timeline': timeline,
                                'Predicted_Sales': formatted_actual_predicted})

    actual_vs_forecasted = pd.merge(df, forecast_df, left_on='Timeline', right_on='Timeline', how='right')
    actual_vs_forecasted = actual_vs_forecasted[['Timeline', 'total_sales', 'Predicted_Sales']]
    return actual_vs_forecasted

def forecast_sales(df):
    df['Month'] = pd.to_datetime(df['Date']).dt.strftime('%Y-%m')
    df_months = df.groupby(by='Month').agg({'total_sales': 'sum'}).round(2)
    df_months['Timeline'] = df_months.index
    df_months.reset_index(drop=True, inplace=True)
    df_customers = df.groupby(by=['Date', 'Customer_name']).agg({'total_sales': 'sum'})
    df_customers.reset_index(inplace=True)
    df_customers.rename(columns={'Date': 'Timeline'}, inplace=True)
    min_month = min(df_months['Timeline'])
    max_month = max(df_months['Timeline'])
    total_sales_title = f"Total Sales Vs. Forecasted Sales from {min_month} to {max_month}"

    monthly_total_sales_vs_forecast = arima_prediction(df_months)

    plot_graph(title=total_sales_title, df=monthly_total_sales_vs_forecast, figure=1)

    f=2
    customers_list = df_customers['Customer_name'].unique().tolist()
    for customer in customers_list:
        df_customer = df_customers[df_customers['Customer_name'] == customer]
        df_customer['Timeline'] = pd.to_datetime(df_customer['Timeline']).dt.strftime('%Y-%m')
        df_customer_monthly = df_customer.groupby(by='Timeline').agg({'total_sales':'sum'}).round(2)
        df_customer_monthly.reset_index(inplace=True)
        df_customer_sales_vs_predict = arima_prediction(df_customer_monthly)
        customer_title = f"{customer}: Total Sales Vs. Forecasted Sales from {min_month} to {max_month}"
        plot_graph(title=customer_title, df=df_customer_sales_vs_predict, figure=f)
        f += 1

    plt.show()

df = create_data()
forecast_sales(df)
