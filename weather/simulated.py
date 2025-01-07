import pandas as pd

# NOTE: Simulate the weather of the current hour based on the weather condition
# Used columns: "temperature_2m", "snowfall", "snow_depth", "wind_gusts_10m"
def simulate_weather(df: pd.DataFrame, weather_condition: str):
    if weather_condition == "Clear":
        # Imaginary ideal weather
        df.iloc[-1, df.columns.get_loc("temperature_2m")] = 20
        df.iloc[-1, df.columns.get_loc("snowfall")] = 0
        df.iloc[-1, df.columns.get_loc("snow_depth")] = 0
        df.iloc[-1, df.columns.get_loc("wind_gusts_10m")] = 0
    elif weather_condition == "Snow":
        # Taken from a very snowy day in Gävle (End of November 2024)
        df.iloc[-1, df.columns.get_loc("temperature_2m")] = -5
        df.iloc[-1, df.columns.get_loc("snowfall")] = 0.8
        df.iloc[-1, df.columns.get_loc("snow_depth")] = 0.3
        df.iloc[-1, df.columns.get_loc("wind_gusts_10m")] = 70
    elif weather_condition == "Windy":
        # Taken from a very windy day in Gävle (End of November 2024)
        df.iloc[-1, df.columns.get_loc("temperature_2m")] = 2
        df.iloc[-1, df.columns.get_loc("snowfall")] = 0
        df.iloc[-1, df.columns.get_loc("snow_depth")] = 0
        df.iloc[-1, df.columns.get_loc("wind_gusts_10m")] = 80
    else:
        # Unknown weather condition
        print(f"Unknown weather condition: {weather_condition}")
    return df