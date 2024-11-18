import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX

class arima_predicted:
    '''

    '''
    def arima_model(forecast_period, df, colname, period_name):
        arima = ARIMA(df[colname], order=(1, 1, 1))
        model_arima = arima.fit()

        forecast = model_arima.forecast(steps=forecast_period)

        df[period_name] = df.index
        df[period_name] = pd.to_datetime(df[period_name])

        forecast_start_idx = len(df)

        print(df.loc[forecast_start_idx - 1, colname])

        for i in range(forecast_period):
            df.loc[forecast_start_idx + i, f'Predicted_{colname}'] = forecast.iloc[i]
            df.loc[forecast_start_idx + i, period_name] = forecast.index[i]



        df[f'Predicted_{colname}'] = df[f'Predicted_{colname}'].round(2)

        df = df[[period_name, colname, f'Predicted_{colname}']]

        return df
