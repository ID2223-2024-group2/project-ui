class Wmo:
    def __init__(self, description, icon):
        self.description = description
        self.icon = icon

    def __repr__(self):
        return f"Wmo(description={self.description}, icon={self.icon})"

    @classmethod
    def from_code(cls, code):
        return WMO_CODES.get(code, WMO_CODES[0])


def make_wmo(description, icon_name) -> Wmo:
    icon = f"icons/{icon_name}@4x.png"
    return Wmo(description, icon)


WMO_CODES = {
    0: make_wmo('Clear', 'clear'),
    1: make_wmo('Mostly Clear', 'mostly-clear'),
    2: make_wmo('Partly Cloudy', 'partly-cloudy'),
    3: make_wmo('Overcast', 'overcast'),
    45: make_wmo('Fog', 'fog'),
    48: make_wmo('Icy Fog', 'rime-fog'),
    51: make_wmo('L.Drizzle', 'light-drizzle'),
    53: make_wmo('Drizzle', 'moderate-drizzle'),
    55: make_wmo('H.Drizzle', 'dense-drizzle'),
    80: make_wmo('L.Showers', 'light-rain'),
    81: make_wmo('Showers', 'moderate-rain'),
    82: make_wmo('H.Showers', 'heavy-rain'),
    61: make_wmo('L.Rain', 'light-rain'),
    63: make_wmo('Rain', 'moderate-rain'),
    65: make_wmo('H.Rain', 'heavy-rain'),
    56: make_wmo('L.Icy Drizzle', 'light-freezing-drizzle'),
    57: make_wmo('Icy Drizzle', 'dense-freezing-drizzle'),
    66: make_wmo('L.Icy Rain', 'light-freezing-rain'),
    67: make_wmo('Icy Rain', 'heavy-freezing-rain'),
    77: make_wmo('Snow Grains', 'snowflake'),
    85: make_wmo('L.Snow Showers', 'slight-snowfall'),
    86: make_wmo('Snow Showers', 'heavy-snowfall'),
    71: make_wmo('Light Snow', 'slight-snowfall'),
    73: make_wmo('Snow', 'moderate-snowfall'),
    75: make_wmo('Heavy Snow', 'heavy-snowfall'),
    95: make_wmo('Thunder Storm', 'thunderstorm'),
    96: make_wmo('T-Storm + L.Hail', 'thunderstorm-with-hail'),
    99: make_wmo('T-Storm + Hail', 'thunderstorm-with-hail')
}