
from matplotlib import pyplot as plt
from GreenVold_Predicted import arima_predicted
from GreenVolt_db import greenvolt
data = greenvolt.query_table('Monthly_Sales')
groupby_YearMonth = data.groupby(by=['YearMonth']).agg({'totalSales': 'sum'}).round(2)
df_PredictedSales_Monthly = arima_predicted.arima_model(forecast_period=6, df=groupby_YearMonth, colname='totalSales', period_name='Month')
plt.plot(df_PredictedSales_Monthly['Month'], df_PredictedSales_Monthly['totalSales'], color='b', marker='s')
plt.plot(df_PredictedSales_Monthly['Month'], df_PredictedSales_Monthly['Predicted_totalSales'], color='r', marker='s', linestyle='dotted')
plt.show()