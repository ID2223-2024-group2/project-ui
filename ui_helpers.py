import pandas as pd

TO_USE = ["route_type", "mean_arrival_delay_seconds_lag_5stops", "stop_count", "temperature_2m", "snowfall", "snow_depth", "wind_gusts_10m", "hour"]
_route_types = [100, 101, 102, 103, 105, 106, 401, 700, 714, 900, 1000, 1501]


def strip_dates(df):
    return df.drop(["date", "arrival_time_bin"], axis=1)


def one_hot(df):
    if "route_type" in df:
        encoded = pd.get_dummies(df["route_type"], prefix="route_type", dtype="int64")
        for rt in _route_types:
            if f"route_type_{rt}" not in encoded.columns:
                encoded[f"route_type_{rt}"] = 0
        df = pd.concat([df, encoded], axis=1).drop(columns=["route_type"])
    return df


def transport_int(transport_string):
    if transport_string == "Train":
        return 100
    elif transport_string == "Bus":
        return 700
    else:
        raise RuntimeError("unknown transportation type " + transport_string)


def get_interval(date, full=False):
    return date.strftime("**%H:%M**" + (" *(%Y-%m-%d)*" if full else ""))


def seconds_to_minute_string(seconds):
    mins = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{mins}m {secs}s"


def get_current_prediction_values(df: pd.DataFrame) -> (float, float, str):
    current_prediction = df.iloc[-1]
    delay = current_prediction["predicted_delay"]
    on_time = current_prediction["predicted_on_time"]
    date = current_prediction["arrival_time_bin"]
    return delay, on_time, date


def get_prediction_trends(df: pd.DataFrame) -> (float, float):
    delay_trend = df["predicted_delay"].diff().mean()
    on_time_trend = df["predicted_on_time"].diff().mean()
    return delay_trend, on_time_trend