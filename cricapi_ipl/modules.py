import requests
import json
import re
from datetime import datetime
from .config import CONFIG, CONSTANTS
from .hitinfo import update_hits_info
from .venue import Venue
from .team import Team

class Innings:
    def __init__(self):
        self.num = 0
        self.team = Team("")
        self.runs = 0
        self.overs = 0.0
        self.wickets = 0

    def __str__(self):
        # 0 padded runs and wickets
        return f"Innings {self.num:<4}: {self.team.short_name:<5} - score: {self.runs:03}/{self.wickets:<2} Overs: {self.overs}"

    def __repr__(self):
        return self.__str__()

class Match:
    def __init__(self, match_json):
        self.__match_json = match_json
        date_str = match_json.get("date")
        try:
            self.__date = datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            self.__date = datetime.now()

        self.__innings = [Innings(), Innings()] # will be updated when update_match_info() is called

    def __str__(self):
        return f"{self.get_date_str():<15} {self.get_name():<40} {self.get_status():<10}\n" \
               f"\t{self.get_match_innings_summary(1)}\n" \
               f"\t{self.get_match_innings_summary(2)}"

    def __repr__(self):
        return json.dumps(self.__match_json, indent=4)

    def get_id(self):
        return self.__match_json.get("id", "N/A")

    def get_name(self):
        return self.__match_json.get("name", "N/A")

    def get_date_str(self):
        return self.__date.strftime("%B %d %Y")

    def get_date(self):
        return self.__date

    def get_status(self):
        return self.__match_json.get("status", "N/A")

    def get_venue(self):
        return Venue(self.__match_json.get("venue", "N/A"))

    def get_home_team(self):
        return Team(self.__match_json.get("teams", ["N/A", "N/A"])[0])

    def get_away_team(self):
        return Team(self.__match_json.get("teams", ["N/A", "N/A"])[1])

    def get_toss_winner(self):
        return Team(self.__match_json.get("tossWinner", "N/A"))

    def get_toss_result(self):
        return self.__match_json.get("tossChoice", "N/A")

    def get_match_winner(self):
        return Team(self.__match_json.get("matchWinner", "N/A"))

    def update_match_info(self):
        if not CONFIG["API_KEY"]:
            raise ValueError("API key is not set. Use set_api_key() to set it.")

        params = {
            "apikey": CONFIG["API_KEY"],
            "id": self.get_id()
        }
        response = requests.get(CONSTANTS["MATCH_INFO_URL"], params=params, timeout=10)
        response.raise_for_status()
        self.__match_json = response.json().get("data", {})

        if not self.__match_json.get("matchEnded", False):
            return

        score = self.__match_json.get("score", [])
        if len(score) != 2:
            return
        self.__innings[0].num = 1
        pattern = re.compile(r"(.*) Inning .*")
        inngs_str = score[0].get("inning", "")
        self.__innings[0].team = Team(pattern.match(inngs_str).group(1) if pattern.match(inngs_str) else inngs_str)
        self.__innings[0].runs = score[0].get("r", 0)
        self.__innings[0].overs = score[0].get("o", 0.0)
        self.__innings[0].wickets = score[0].get("w", 0)

        self.__innings[1].num = 2
        pattern = re.compile(r"(.*) Inning .*")
        inngs_str = score[1].get("inning", "")
        self.__innings[1].team = Team(pattern.match(inngs_str).group(1) if pattern.match(inngs_str) else inngs_str)
        self.__innings[1].runs = score[1].get("r", 0)
        self.__innings[1].overs = score[1].get("o", 0.0)
        self.__innings[1].wickets = score[1].get("w", 0)

        update_hits_info(response.json().get("info", {}))

    def get_match_innings_summary(self, innings):
        if innings != 1 and innings != 2:
            raise ValueError("Innings must be 1 or 2.")
        return f"{self.__innings[innings - 1]}"

    def get_match_innings(self, innings):
        if innings != 1 and innings != 2:
            raise ValueError("Innings must be 1 or 2.")
        return self.__innings[innings - 1]

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
        self.teams = set()
        self.venues = set()

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
            self.teams.add(match.get_home_team())
            self.teams.add(match.get_away_team())
            self.venues.add(match.get_venue())
