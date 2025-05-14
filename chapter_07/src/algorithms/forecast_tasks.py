import pandas as pd
import plotly.express as px
from sktime.forecasting.base import ForecastingHorizon
from sktime.forecasting.compose import ForecastingPipeline
from sktime.forecasting.exp_smoothing import ExponentialSmoothing


def filter_dataframe(df, gender_forecast, generation_forecast, product_forecast):
    if gender_forecast != "All":
        df = df[df["gender"] == gender_forecast]
    if generation_forecast != "All":
        df = df[df["generation"] == generation_forecast]
    if product_forecast != "All":
        df = df[df["type"] == product_forecast]
    df = df.reset_index(drop=True)
    return df


def prepare_data(df, target):
    """
    Prepares the input dataframe for time series forecasting.

    Parameters:
        df (pd.DataFrame): Input dataframe with at least a date column and a numeric target column.
        target (str): Name of the column to forecast.

    Returns:
        pd.DataFrame: Aggregated and indexed dataframe with regular daily frequency.
    """
    df_agg = df.groupby("date")[target].sum().reset_index()
    df_agg["date"] = pd.to_datetime(df_agg["date"])
    df_agg = df_agg.set_index("date")
    df_agg.index = pd.date_range(
        start=df_agg.index.min(), periods=len(df_agg), freq="D"
    )  # Ensure regular frequency
    return df_agg


def create_pipeline():
    """
    Creates a forecasting pipeline with Exponential Smoothing for trend and seasonality.

    Returns:
        ForecastingPipeline: Configured forecasting pipeline.
    """
    pipeline = ForecastingPipeline(
        steps=[
            (
                "model",
                ExponentialSmoothing(
                    trend="mul",
                    seasonal="mul",
                    sp=91,
                    initialization_method="estimated",
                    use_boxcox=True,
                    optimized=True,
                    method="L-BFGS-B",
                ),
            )
        ]
    )
    return pipeline


def fit_and_forecast_future(df_agg, target, number_of_days):
    """
    Fits the forecasting pipeline on the entire data and forecasts future values.

    Parameters:
        df_agg (pd.DataFrame): Prepared dataframe with a datetime index.
        target (str): Name of the target column to forecast.
        number_of_days (int): Number of future days to predict.

    Returns:
        tuple: (y_future, future_dates) where y_future is the predicted values and future_dates are the dates for predictions.
    """
    pipeline = create_pipeline()
    y = df_agg[target]
    pipeline.fit(y)

    last_date = y.index[-1]
    future_dates = pd.date_range(
        start=last_date + pd.Timedelta(days=1), periods=number_of_days, freq="D"
    )
    fh_future = ForecastingHorizon(future_dates, is_relative=False)
    y_future = pipeline.predict(fh_future)

    return y_future, future_dates


def compute_confidence_intervals(y_pred, sigma=1.96):
    """
    Computes confidence intervals for predicted values.

    Parameters:
        y_pred (pd.Series): Predicted values.
        sigma (float): Multiplier for standard deviation to compute the interval width (default is 1.96 for ~95% CI).

    Returns:
        tuple: (conf_min, conf_max) confidence interval bounds.
    """

    pred_values = y_pred.values
    std_dev = pred_values.std()  # Simplified assumption
    conf_min = pred_values - sigma * std_dev
    conf_max = pred_values + sigma * std_dev
    return conf_min, conf_max


def create_forecast_dataframe(future_dates, y_future, conf_min, conf_max):
    """
    Creates a dataframe containing forecasted values and their confidence intervals.

    Parameters:
        future_dates (pd.DatetimeIndex): Dates for the forecast.
        y_future (pd.Series): Forecasted values.
        conf_min (array-like): Lower bounds of the confidence interval.
        conf_max (array-like): Upper bounds of the confidence interval.

    Returns:
        pd.DataFrame: Dataframe with forecast, conf_min, and conf_max columns.
    """
    forecast_df = pd.DataFrame(
        {
            "date": future_dates,
            "forecast": y_future.values,
            "conf_min": conf_min,
            "conf_max": conf_max,
        }
    )
    return forecast_df


def plot_forecast(df_agg, target, forecast_df):
    """
    Plots the actual and forecasted values with confidence intervals.

    Parameters:
        df_agg (pd.DataFrame): Historical data with actual values.
        target (str): Name of the target column.
        forecast_df (pd.DataFrame): Dataframe with forecasted values and confidence intervals.

    Returns:
        plotly.express fig.
    """
    df_agg_reset = df_agg.reset_index().rename(columns={"index": "date"})
    fig = px.line(
        df_agg_reset, x="date", y=target, title=f"{target.capitalize()} Forecast"
    )
    fig.add_scatter(
        x=forecast_df["date"], y=forecast_df["forecast"], mode="lines", name="Forecast"
    )
    fig.add_scatter(
        x=forecast_df["date"],
        y=forecast_df["conf_min"],
        mode="lines",
        name="Lower Bound",
        line=dict(dash="dash"),
    )
    fig.add_scatter(
        x=forecast_df["date"],
        y=forecast_df["conf_max"],
        mode="lines",
        name="Upper Bound",
        line=dict(dash="dash"),
    )
    return fig


def summarize_forecast(forecast_df):
    """
    Summarizes the forecast data by computing total values of forecast and confidence intervals.

    Parameters:
        forecast_df (pd.DataFrame): Dataframe with forecasted values and confidence intervals.

    Returns:
        dict: Dictionary containing the max of forecast, conf_min, and conf_max.
    """
    summary = {
        "total_forecast": forecast_df["forecast"].sum(),
        "total_conf_min": forecast_df["conf_min"].sum(),
        "total_conf_max": forecast_df["conf_max"].sum(),
    }
    return summary
