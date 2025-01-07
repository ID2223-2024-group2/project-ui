import openmeteo_requests
from openmeteo_sdk.WeatherApiResponse import WeatherApiResponse

om_client = openmeteo_requests.Client()

FORECAST_URL = "https://api.open-meteo.com/v1/forecast"


def fetch_forecast_weather(longitude, latitude, url=FORECAST_URL) -> WeatherApiResponse:
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": ["temperature_2m", "apparent_temperature", "precipitation", "rain", "snowfall", "snow_depth",
                   "cloud_cover", "wind_speed_10m", "wind_speed_100m", "wind_gusts_10m", "weather_code"]
    }
    responses = om_client.weather_api(url, params=params)
    return responses[0]