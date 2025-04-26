
from .series import Series
from .hitinfo import update_hits_info
import requests
import re
from .config import CONFIG, CONSTANTS

def set_api_key(api_key):
    if not isinstance(api_key, str):
        raise TypeError("API key must be a string.")
    if not api_key:
        raise ValueError("API key cannot be empty.")
    # check if the API key is in GUID format using regex
    pattern = re.compile(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$')
    if not pattern.match(api_key):
        raise ValueError("API key must be in GUID format.")
    CONFIG["API_KEY"] = api_key

def clear_api_key():
    CONFIG["API_KEY"] = ""

def get_series_map():
    if not CONFIG["API_KEY"]:
        raise ValueError("API key is not set. Use set_api_key() to set it.")

    # Generate offsets list
    params = {
        "apikey": CONFIG["API_KEY"],
        "offset": 0,
        "search": CONSTANTS["SERIES_SEARCH_TERM"]
    }
    response = requests.get(CONSTANTS["SERIES_SERACH_URL"], params=params, timeout=10)
    response.raise_for_status()
    all_results = response.json().get("data", [])

    info = response.json().get("info", {})
    update_hits_info(info)
    series_list = [Series(series) for series in all_results]
    # create a map with key as year of start date of the series
    series_map = {}
    for series in series_list:
        # assume there is only one series per year
        year = series.get_start_date().year
        series_map[year] = series
    return series_map
