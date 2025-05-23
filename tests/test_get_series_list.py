from cricapi_ipl.series import Series
from cricapi_ipl.hitinfo import get_hits_info
from cricapi_ipl.apis import get_series_map, set_api_key
from cricapi_ipl.venue import Venue
from cricapi_ipl.team import Team
from datetime import datetime
from unittest.mock import patch, Mock
import pytest


def test_get_series_map_no_api_key():
    with pytest.raises(ValueError):
        get_series_map()  # Should raise ValueError if API key is not set

def test_get_series_map():
    # Mock API key
    set_api_key("12345678-1234-1234-1234-123456789012")

    mock_response = Mock()
    mock_response.json.return_value = {
        "data": [
            {
                "id": "1",
                "name": "Indian Premier League 2023",
                "matches": 70,
                "startDate": "2023-03-31",
                "endDate": "May 15"
            },
            {
                "id": "2",
                "name": "ndian Premier League 2024",
                "matches": 74,
                "startDate": "2024-06-01",
                "endDate": "May 25"
            }
        ],
        "info": {
            "hitsToday": 1,
            "hitsUsed": 1,
            "hitsLimit": 100,
            "credits": 0,
            "server": 8,
            "offsetRows": 0,
            "totalRows": 4,
            "queryTime": 43.9282,
            "s": 0,
            "cache": 0
        }
    }
    mock_response.raise_for_status = Mock()
    mock_response.status_code = 200

    with patch('cricapi_ipl.series.requests.get', return_value=mock_response):
        series_map = get_series_map()
        assert len(series_map) == 2
        assert series_map[2023].get_name() == "Indian Premier League 2023"
        assert series_map[2023].get_num_matches() == 70
        assert series_map[2023].get_start_date() == datetime.strptime("2023-03-31", "%Y-%m-%d")
        assert series_map[2023].get_end_date() == datetime.strptime("May 15 2023", "%B %d %Y")
        assert series_map[2023].get_id() == "1"

        assert series_map[2024].get_name() == "ndian Premier League 2024"
        assert series_map[2024].get_num_matches() == 74
        assert series_map[2024].get_start_date() == datetime.strptime("2024-06-01", "%Y-%m-%d")
        assert series_map[2024].get_end_date() == datetime.strptime("May 25 2024", "%B %d %Y")
        assert series_map[2024].get_id() == "2"

        hits = get_hits_info()
        assert hits.hits_today == 1
        assert hits.hits_used == 1
        assert hits.hits_limit == 100

def test_update_matches():
    mock_response = Mock()
    mock_response.json.return_value = {
        "data": {
            "info": {
              "id": "d5a498c8-7596-4b93-8ab0-e0efc3345312",
              "name": "Indian Premier League 2025",
              "startdate": "2025-03-22",
              "enddate": "May 25",
              "odi": 0,
              "t20": 74,
              "test": 0,
              "squads": 10,
              "matches": 74
            },
            "matchList": [
                {
                    "id": "208d68e5-3fab-4f3b-88e9-29ec4a02d3e2",
                    "name": "Chennai Super Kings vs Mumbai Indians, 3rd Match",
                    "matchType": "t20",
                    "status": "Chennai Super Kings won by 4 wkts",
                    "venue": "MA Chidambaram Stadium, Chennai",
                    "date": "2025-03-23",
                    "dateTimeGMT": "2025-03-23T14:00:00",
                    "teams": [
                      "Chennai Super Kings",
                      "Mumbai Indians"
                    ]
                },
                {
                    "id": "83d70527-5fc4-4fad-8dd2-b88b385f379e",
                    "name": "Gujarat Titans vs Punjab Kings, 5th Match",
                    "matchType": "t20",
                    "status": "Punjab Kings won by 11 runs",
                    "venue": "Narendra Modi Stadium, Ahmedabad",
                    "date": "2025-03-25",
                    "dateTimeGMT": "2025-03-25T14:00:00",
                    "teams": [
                      "Gujarat Titans",
                      "Punjab Kings"
                    ]
                },
          ]
        },
        "info": {
            "hitsToday": 2,
            "hitsUsed": 2,
            "hitsLimit": 100,
            "credits": 0,
            "server": 8,
            "offsetRows": 0,
            "totalRows": 4,
            "queryTime": 43.9282,
            "s": 0,
            "cache": 0
        }
    }
    mock_response.raise_for_status = Mock()
    mock_response.status_code = 200

    with patch('cricapi_ipl.series.requests.get', return_value=mock_response):
        series = Series({
            "id": "1",
            "name": "Indian Premier League 2023",
            "matches": 70,
            "startDate": "2023-03-31",
            "endDate": "May 15"
        })
        series.update_matches()
        assert len(series.matches) == 2
        assert series.matches[0].get_name() == "Chennai Super Kings vs Mumbai Indians, 3rd Match"
        assert series.matches[0].get_status() == "Chennai Super Kings won by 4 wkts"
        assert series.matches[0].get_venue() == Venue("MA Chidambaram Stadium, Chennai")
        assert series.matches[0].get_date() == datetime.strptime("2025-03-23", "%Y-%m-%d")
        assert series.matches[0].get_home_team() == Team("Chennai Super Kings")
        assert series.matches[0].get_away_team() == Team("Mumbai Indians")
        assert series.matches[0].get_id() == "208d68e5-3fab-4f3b-88e9-29ec4a02d3e2"

        assert series.matches[1].get_name() == "Gujarat Titans vs Punjab Kings, 5th Match"
        assert series.matches[1].get_status() == "Punjab Kings won by 11 runs"
        assert series.matches[1].get_venue() == Venue("Narendra Modi Stadium, Ahmedabad")
        assert series.matches[1].get_date() == datetime.strptime("2025-03-25", "%Y-%m-%d")
        assert series.matches[1].get_home_team() == Team("Gujarat Titans")
        assert series.matches[1].get_away_team() == Team("Punjab Kings")
        assert series.matches[1].get_id() == "83d70527-5fc4-4fad-8dd2-b88b385f379e"

        assert len(series.teams) == 4
        assert len(series.venues) == 2
        assert Team("Chennai Super Kings").short_name in series.teams
        assert Team("Mumbai Indians").short_name in series.teams
        assert Team("Gujarat Titans").short_name in series.teams
        assert Team("Punjab Kings").short_name in series.teams
        assert Venue("MA Chidambaram Stadium, Chennai").city in series.venues
        assert Venue("Narendra Modi Stadium, Ahmedabad").city in series.venues

        team_matches = series.get_matches_for_team("Chennai Super Kings")
        assert len(team_matches) == 1
        assert team_matches[0] == series.matches[0]

        team_matches = series.get_matches_for_team("MI")
        assert len(team_matches) == 1
        assert team_matches[0] == series.matches[0]

        team_matches = series.get_matches_for_team(Team("Gujarat Titans"))
        assert len(team_matches) == 1
        assert team_matches[0] == series.matches[1]

        venue_matches = series.get_matches_for_city("Chennai")
        assert len(venue_matches) == 1
        assert venue_matches[0] == series.matches[0]

        venue_matches = series.get_matches_for_city("Ahmedabad")
        assert len(venue_matches) == 1
        assert venue_matches[0] == series.matches[1]


        hits = get_hits_info()
        assert hits.hits_today == 2
        assert hits.hits_used == 2
        assert hits.hits_limit == 100