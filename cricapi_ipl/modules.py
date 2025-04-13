import requests
import json
import re
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime


API_KEY = ""
SERIES_SEARCH_TERM = "Indian Premier League"

# API URLs
SERIES_SERACH_URL = "https://api.cricapi.com/v1/series"
SERIES_INFO_URL = "https://api.cricapi.com/v1/series_info"


class Match:
    def __init__(self, match_json):
        self.id = match_json.get("id", "N/A")
        self.name = match_json.get("name", "N/A")
        date_str = match_json.get("date")
        try:
            self.date = datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            self.date = datetime.now()
        self.status = match_json.get("status", "N/A")
        self.venue = match_json.get("venue", "N/A")
        self.home_team = match_json.get("teams", ["N/A", "N/A"])[0]
        self.away_team = match_json.get("teams", ["N/A", "N/A"])[1]

    def __str__(self):
        return f"{self.name:<40}, Date: {self.date.strftime('%B %d %Y'):<15}, Status: {self.status:<10}"

    def __repr__(self):
        return self.__str__()

class Series:
    def __init__(self, series_json):
        self.id = series_json.get("id", "N/A")
        self.name = series_json.get("name", "N/A")
        self.num_matches = series_json.get("matches", "N/A")
        start_date_str = series_json.get("startDate")
        try:
            self.start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        except ValueError:
            self.start_date = datetime.now()
        end_date_str = series_json.get("endDate")
        end_date_str_formatted = f"{end_date_str} {self.start_date.year}"
        try:
            self.end_date = datetime.strptime(end_date_str_formatted, "%B %d %Y")
        except ValueError:
            self.end_date = datetime.now()
        self.matches = []

    def __str__(self):
        return f"{self.name:<40}, Matches: {self.num_matches:<10}, Start Date: {self.start_date.strftime('%B %d %Y'):<15}, End Date: {self.end_date.strftime('%B %d %Y'):15}"

    def __repr__(self):
        return self.__str__()

    def update_matches(self):
        if not API_KEY:
            raise ValueError("API key is not set. Use set_api_key() to set it.")

        params = {
            "apikey": API_KEY,
            "id": self.id
        }
        response = requests.get(SERIES_INFO_URL, params=params, timeout=10)
        response.raise_for_status()
        series_data = response.json().get("data", {})
        all_results = series_data.get("matchList", [])

        info = response.json().get("info", {})
        _update_hits_info(info)

        self.matches = [Match(match) for match in all_results]

class HitInfo:
    def __init__(self):
        self.hits_today = 0
        self.hits_used = 0
        self.hits_limit = 100

    def __str__(self):
        return f"Hits Today: {self.hits_today}, Hits Used: {self.hits_used}, Hits Limit: {self.hits_limit}"

    def __repr__(self):
        return self.__str__()

hits = HitInfo()

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

def clear_api_key():
    global API_KEY
    API_KEY = ""

def get_hits_info():
    return hits

def _update_hits_info(info):
    global hits
    hits.hits_today = info.get("hitsToday", 0)
    hits.hits_used = info.get("hitsUsed", 0)
    hits.hits_limit = info.get("hitsLimit", 100)

def get_series_list():
    if not API_KEY:
        raise ValueError("API key is not set. Use set_api_key() to set it.")

    # Generate offsets list
    params = {
        "apikey": API_KEY,
        "offset": 0,
        "search": SERIES_SEARCH_TERM
    }
    response = requests.get(SERIES_SERACH_URL, params=params, timeout=10)
    response.raise_for_status()
    all_results = response.json().get("data", [])

    info = response.json().get("info", {})
    _update_hits_info(info)
    return [Series(series) for series in all_results]
