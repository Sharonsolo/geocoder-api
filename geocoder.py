import requests
import json
import redis
from config import Config

# ---------------------------
# Cache Setup
# ---------------------------
if Config.USE_REDIS:
    cache = redis.Redis(
        host=Config.REDIS_HOST,
        port=Config.REDIS_PORT,
        db=Config.REDIS_DB,
        decode_responses=True
    )
else:
    cache = {}   # fallback in-memory cache


# ---------------------------
# External API Request
# ---------------------------
def geocode_address(address: str):
    address_key = address.lower().strip()

    # Check cache
    if Config.USE_REDIS:
        cached = cache.get(address_key)
        if cached:
            print("cachedddddddd")
            return json.loads(cached)
    else:
        if address_key in cache:
            print("cachedddddddd 4444")
            return cache[address_key]

    # Call Nominatim API
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": address,
        "format": "json",
        "limit": 1
    }

    response = requests.get(url, params=params, headers={"User-Agent": "FlaskGeocoder"})
    data = response.json()

    if not data:
        return None

    result = {
        "latitude": data[0]["lat"],
        "longitude": data[0]["lon"],
        "display_name": data[0]["display_name"]
    }

    # Store in cache
    if Config.USE_REDIS:
        cache.set(address_key, json.dumps(result))
    else:
        cache[address_key] = result

    return result
