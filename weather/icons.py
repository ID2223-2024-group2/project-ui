class Wmo:
    def __init__(self, description, icon, open_weather_icon_url):
        self.description = description
        self.icon = icon
        self.open_weather_icon_url = open_weather_icon_url

    def __repr__(self):
        return f"Wmo(description={self.description}, icon={self.icon}, open_weather_icon_url={self.open_weather_icon_url})"

    @classmethod
    def from_code(cls, code):
        return WMO_CODES.get(code, WMO_CODES[0])

    def to_emoji(self):
        return EMOJI_MAPPING.get(self.description, "❓")


def make_wmo(description, icon_name, open_weather_icon_url) -> Wmo:
    icon = f"icons/{icon_name}@4x.png"
    return Wmo(description, icon, open_weather_icon_url)


OWM_BASE_URL = "https://openweathermap.org/img/wn/"

WMO_CODES = {
    0: make_wmo('Clear', 'clear', f"{OWM_BASE_URL}01d@2x.png"),
    1: make_wmo('Mostly Clear', 'mostly-clear', f"{OWM_BASE_URL}01d@2x.png"),
    2: make_wmo('Partly Cloudy', 'partly-cloudy', f"{OWM_BASE_URL}02d@2x.png"),
    3: make_wmo('Overcast', 'overcast', f"{OWM_BASE_URL}03d@2x.png"),
    45: make_wmo('Fog', 'fog', f"{OWM_BASE_URL}50d@2x.png"),
    48: make_wmo('Icy Fog', 'rime-fog', f"{OWM_BASE_URL}50d@2x.png"),
    51: make_wmo('L.Drizzle', 'light-drizzle', f"{OWM_BASE_URL}09d@2x.png"),
    53: make_wmo('Drizzle', 'moderate-drizzle', f"{OWM_BASE_URL}09d@2x.png"),
    55: make_wmo('H.Drizzle', 'dense-drizzle', f"{OWM_BASE_URL}09d@2x.png"),
    80: make_wmo('L.Showers', 'light-rain', f"{OWM_BASE_URL}09d@2x.png"),
    81: make_wmo('Showers', 'moderate-rain', f"{OWM_BASE_URL}09d@2x.png"),
    82: make_wmo('H.Showers', 'heavy-rain', f"{OWM_BASE_URL}09d@2x.png"),
    61: make_wmo('L.Rain', 'light-rain', f"{OWM_BASE_URL}10d@2x.png"),
    63: make_wmo('Rain', 'moderate-rain', f"{OWM_BASE_URL}10d@2x.png"),
    65: make_wmo('H.Rain', 'heavy-rain', f"{OWM_BASE_URL}10d@2x.png"),
    56: make_wmo('L.Icy Drizzle', 'light-freezing-drizzle', f"{OWM_BASE_URL}09d@2x.png"),
    57: make_wmo('Icy Drizzle', 'dense-freezing-drizzle', f"{OWM_BASE_URL}09d@2x.png"),
    66: make_wmo('L.Icy Rain', 'light-freezing-rain', f"{OWM_BASE_URL}10d@2x.png"),
    67: make_wmo('Icy Rain', 'heavy-freezing-rain', f"{OWM_BASE_URL}10d@2x.png"),
    77: make_wmo('Snow Grains', 'snowflake', f"{OWM_BASE_URL}13d@2x.png"),
    85: make_wmo('L.Snow Showers', 'slight-snowfall', f"{OWM_BASE_URL}13d@2x.png"),
    86: make_wmo('Snow Showers', 'heavy-snowfall', f"{OWM_BASE_URL}13d@2x.png"),
    71: make_wmo('Light Snow', 'slight-snowfall', f"{OWM_BASE_URL}13d@2x.png"),
    73: make_wmo('Snow', 'moderate-snowfall', f"{OWM_BASE_URL}13d@2x.png"),
    75: make_wmo('Heavy Snow', 'heavy-snowfall', f"{OWM_BASE_URL}13d@2x.png"),
    95: make_wmo('Thunder Storm', 'thunderstorm', f"{OWM_BASE_URL}11d@2x.png"),
    96: make_wmo('T-Storm + L.Hail', 'thunderstorm-with-hail', f"{OWM_BASE_URL}11d@2x.png"),
    99: make_wmo('T-Storm + Hail', 'thunderstorm-with-hail', f"{OWM_BASE_URL}11d@2x.png")
}

EMOJI_MAPPING = {
    "Clear": "☀️",
    "Mostly Clear": "🌤️",
    "Partly Cloudy": "⛅",
    "Overcast": "☁️",
    "Fog": "🌫️",
    "Icy Fog": "🌫️",
    "L.Drizzle": "🌧️",
    "Drizzle": "🌧️",
    "H.Drizzle": "🌧️",
    "L.Showers": "🌧️",
    "Showers": "🌧️",
    "H.Showers": "🌧️",
    "L.Rain": "🌧️",
    "Rain": "🌧️",
    "H.Rain": "🌧️",
    "L.Icy Drizzle": "🌧️",
    "Icy Drizzle": "🌧️",
    "L.Icy Rain": "🌧️",
    "Icy Rain": "🌧️",
    "Snow Grains": "❄️",
    "L.Snow Showers": "❄️",
    "Snow Showers": "❄️",
    "Light Snow": "❄️",
    "Snow": "❄️",
    "Heavy Snow": "❄️",
    "Thunder Storm": "⛈️",
    "T-Storm + L.Hail": "⛈️",
    "T-Storm + Hail": "⛈️"
}

