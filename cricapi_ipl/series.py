import requests
import json
from datetime import datetime
from .config import CONFIG, CONSTANTS
from .hitinfo import update_hits_info
from .team import Team
from .match import Match

class Series:
    def __init__(self, series_json):
        self.__series_json = series_json
        start_date_str = series_json.get("startDate")
        try:
            self.__start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        except ValueError:
            self.__start_date = datetime.now()
        end_date_str = series_json.get("endDate")
        end_date_str_formatted = f"{end_date_str} {self.__start_date.year}"
        try:
            self.__end_date = datetime.strptime(end_date_str_formatted, "%B %d %Y")
        except ValueError:
            self.__end_date = datetime.now()
        self.matches = []
        self.teams = {}
        self.venues = {}

    def __str__(self):
        return f"{self.get_name():<30} Matches: {self.get_num_matches():<5} Start Date: {self.__start_date.strftime('%B %d %Y'):<15} End Date: {self.__end_date.strftime('%B %d %Y'):15}"

    def __repr__(self):
        return json.dumps(self.__series_json, indent=4)

    def get_id(self):
        return self.__series_json.get("id", "N/A")

    def get_name(self):
        return self.__series_json.get("name", "N/A")

    def get_num_matches(self):
        return self.__series_json.get("matches", "N/A")

    def get_start_date(self):
        return self.__start_date

    def get_end_date(self):
        return self.__end_date

    def get_start_date_str(self):
        return self.__start_date.strftime("%B %d %Y")

    def get_end_date_str(self):
        return self.__end_date.strftime("%B %d %Y")

    def update_matches(self):
        if not CONFIG["API_KEY"]:
            raise ValueError("API key is not set. Use set_api_key() to set it.")

        params = {
            "apikey": CONFIG["API_KEY"],
            "id": self.get_id(),
        }
        response = requests.get(CONSTANTS["SERIES_INFO_URL"], params=params, timeout=10)
        response.raise_for_status()
        series_data = response.json().get("data", {})
        all_results = series_data.get("matchList", [])
        self.matches = [Match(match) for match in all_results]
        update_hits_info(response.json().get("info", {}))
        for match in self.matches:
            if match.get_home_team() == Team('Tbc') or match.get_away_team() == Team('Tbc'):
                continue
            self.teams[match.get_home_team().short_name] = match.get_home_team()
            self.teams[match.get_away_team().short_name] = match.get_away_team()
            self.venues[match.get_venue().city] = match.get_venue()
