GAEVLE_LONGITUDE = 17.1412
GAEVLE_LATITUDE = 60.6748

STATIC_PREFIX = "/app/static/"

def get_relative_static_url(path):
    return f"{STATIC_PREFIX}{path}"

def get_relative_static_path(path):
    return f"static/{path}"