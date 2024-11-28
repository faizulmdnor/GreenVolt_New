import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX

class arima_predicted:
    """
    Handles ARIMA model prediction for a given time series dataset.

    This class manages the ARIMA forecasting process, including fitting the ARIMA
    model to the data, making predictions for a specified period, and appending
    the forecasted values to the original dataset.

    :ivar forecast: The predicted values from the ARIMA model.
    :type forecast: pandas.Series
    :ivar model_arima: The ARIMA model fitted to the data.
    :type model_arima: statsmodels.tsa.arima.model.ARIMAResults
    :ivar df: The original dataframe with the added forecasted values.
    :type df: pandas.DataFrame
    """
    def arima_model(forecast_period, df_arima, colname, period_name):
        arima = ARIMA(df_arima[colname], order=(1, 1, 1))
        model_arima = arima.fit()

        forecast_arima = model_arima.forecast(steps=forecast_period)


        df_arima[period_name] = pd.to_datetime(df_arima['date'])

        forecast_start_idx = len(df_arima)

        for i in range(forecast_period):
            df_arima.loc[forecast_start_idx + i, f'Predicted_{colname}'] = forecast_arima.iloc[i]
            df_arima.loc[forecast_start_idx + i, period_name] = forecast_arima.index[i]

        df_arima[f'Predicted_{colname}'] = df_arima[f'Predicted_{colname}'].round(2)
        df_arima['date'] = pd.date_range(start=min(df_arima['date']), periods=len(df_arima), freq='ME' )

        df_arima = df_arima[['date', period_name, colname, f'Predicted_{colname}']]

        return df_arima

    def sarimax_model(forecast_period, df_sarimax, colname, period_name):
        sarimax = SARIMAX(df_sarimax[colname], order=(1, 1, 1), seasonal_order=(1, 1, 1, 12))
        model_sarimax = sarimax.fit()

        forecast_sarimax = model_sarimax.forecast(steps=forecast_period)

        df_sarimax[period_name] = pd.to_datetime(df_sarimax['date'])

        forecast_start_idx = len(df_sarimax)

        for i in range(forecast_period):
            df_sarimax.loc[forecast_start_idx + i, f'Predicted_{colname}'] = forecast_sarimax.iloc[i]
            df_sarimax.loc[forecast_start_idx + i, period_name] = forecast_sarimax.index[i]

        df_sarimax[f'Predicted_{colname}'] = df_sarimax[f'Predicted_{colname}'].round(2)
        df_sarimax['date'] = pd.date_range(start=min(df_sarimax['date']), periods=len(df_sarimax), freq='ME')
        df_sarimax = df_sarimax[['date', period_name, colname, f'Predicted_{colname}']]

        return df_sarimax
