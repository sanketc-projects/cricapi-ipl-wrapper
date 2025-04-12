import requests
import json
import re
from concurrent.futures import ThreadPoolExecutor


API_KEY = ""
SERIES_LIST_URL = "https://api.cricapi.com/v1/series"

def set_api_key(api_key):
    global API_KEY
    if not isinstance(api_key, str):
        raise TypeError("API key must be a string.")
    if not api_key:
        raise ValueError("API key cannot be empty.")
    # check if the API key is in GUID format using regex
    pattern = re.compile(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$')
    if not pattern.match(api_key):
        raise ValueError("API key must be in GUID format.")
    API_KEY = api_key

class Series:
    def __init__(self, series_json):
        self.id = series_json.get("id", "N/A")
        self.name = series_json.get("name", "N/A")
        self.num_matches = series_json.get("matches", "N/A")
        self.start_date = series_json.get("startDate", "N/A")
        self.end_date = series_json.get("endDate", "N/A")

    def __str__(self):
        return f"{self.name:<40}, Matches: {self.num_matches:<10}, Start Date: {self.start_date:<15}, End Date: {self.end_date:15}"

    def __repr__(self):
        return self.__str__()

 # Function to fetch series for multiple offsets
def _fetch_series(offset_chunk):
    results = []
    for offset in offset_chunk:
        params = {
            "apikey": API_KEY,
            "offset": offset
        }
        try:
            response = requests.get(SERIES_LIST_URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json().get("data", [])
            for series in data:
                if "Indian Premier League" in series.get("name", ""):
                    results.append(series)
        except requests.RequestException as e:
            print(f"Error fetching offset {offset}: {e}")
    return results

def get_series_list():
    if not API_KEY:
        raise ValueError("API key is not set. Use set_api_key() to set it.")

    # Generate offsets list
    offsets = list(range(0, 1001, 25))

    # Split offsets into chunks of 4
    def chunk_list(lst, n):
        for i in range(0, len(lst), n):
            yield lst[i:i + n]

    offset_chunks = list(chunk_list(offsets, 4))
    all_results = []

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(_fetch_series, chunk) for chunk in offset_chunks]

        for future in futures:
            all_results.extend(future.result())

    series_list = [Series(series) for series in all_results]
    # remove duplicates based on series id
    seen = set()
    unique_series_list = []
    for series in series_list:
        if series.id not in seen:
            seen.add(series.id)
            unique_series_list.append(series)
    return unique_series_list
