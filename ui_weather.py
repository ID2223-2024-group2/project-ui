import datetime
import streamlit as st

import pandas as pd
import pytz

import weather.fetch as wf
import weather.parse as wp
import weather.icons as wi
from shared.constants import GAEVLE_LONGITUDE, GAEVLE_LATITUDE


MAX_FORECAST_HOURS = 12
TTL = 60 * 5

@st.cache_data(ttl=TTL, show_spinner="Preparing weather data")
def get_current_weather_df() -> (pd.DataFrame, list[wi.Wmo]):
    weather_df = wp.parse_weather_response(wf.fetch_forecast_weather(GAEVLE_LONGITUDE, GAEVLE_LATITUDE))

    now_utc = datetime.datetime.now(pytz.utc)
    # Get only future weather up to MAX_FORECAST_HOURS
    weather_df = weather_df[(weather_df["date"] >= now_utc) & (weather_df["date"] <= now_utc + datetime.timedelta(hours=MAX_FORECAST_HOURS))]
    # Make sure weather is sorted by date such that the first row is the current weather
    weather_df = weather_df.sort_values("date")
    # Format "display_time" to be a string HH:MM
    weather_df["display_time"] = weather_df["date"].dt.strftime("%H:%M")

    weather_icons = [wi.Wmo.from_code(code) for code in weather_df["weather_code"]]
    return weather_df, weather_icons
