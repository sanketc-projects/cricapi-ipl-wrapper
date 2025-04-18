from cricapi_ipl.modules import get_series_list, set_api_key, get_hits_info, Series, HitInfo, Match
from datetime import datetime
from unittest.mock import patch, Mock
import pytest


def test_get_series_list_no_api_key():
    with pytest.raises(ValueError):
        get_series_list()  # Should raise ValueError if API key is not set

def test_get_series_list():
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

    with patch('cricapi_ipl.modules.requests.get', return_value=mock_response):
        series_list = get_series_list()
        assert len(series_list) == 2
        assert series_list[0].name == "Indian Premier League 2023"
        assert series_list[0].num_matches == 70
        assert series_list[0].start_date == datetime.strptime("2023-03-31", "%Y-%m-%d")
        assert series_list[0].end_date == datetime.strptime("May 15 2023", "%B %d %Y")
        assert series_list[0].id == "1"

        assert series_list[1].name == "ndian Premier League 2024"
        assert series_list[1].num_matches == 74
        assert series_list[1].start_date == datetime.strptime("2024-06-01", "%Y-%m-%d")
        assert series_list[1].end_date == datetime.strptime("May 25 2024", "%B %d %Y")
        assert series_list[1].id == "2"

        hits = get_hits_info()
        assert hits.hits_today == 1
        assert hits.hits_used == 1
        assert hits.hits_limit == 100

def test_update_match_info():
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

    with patch('cricapi_ipl.modules.requests.get', return_value=mock_response):
        series = Series({
            "id": "1",
            "name": "Indian Premier League 2023",
            "matches": 70,
            "startDate": "2023-03-31",
            "endDate": "May 15"
        })
        series.update_matches()
        assert len(series.matches) == 2
        assert series.matches[0].name == "Chennai Super Kings vs Mumbai Indians, 3rd Match"
        assert series.matches[0].status == "Chennai Super Kings won by 4 wkts"
        assert series.matches[0].venue == "MA Chidambaram Stadium, Chennai"
        assert series.matches[0].date == datetime.strptime("2025-03-23", "%Y-%m-%d")
        assert series.matches[0].home_team == "Chennai Super Kings"
        assert series.matches[0].away_team == "Mumbai Indians"
        assert series.matches[0].id == "208d68e5-3fab-4f3b-88e9-29ec4a02d3e2"

        assert series.matches[1].name == "Gujarat Titans vs Punjab Kings, 5th Match"
        assert series.matches[1].status == "Punjab Kings won by 11 runs"
        assert series.matches[1].venue == "Narendra Modi Stadium, Ahmedabad"
        assert series.matches[1].date == datetime.strptime("2025-03-25", "%Y-%m-%d")
        assert series.matches[1].home_team == "Gujarat Titans"
        assert series.matches[1].away_team == "Punjab Kings"
        assert series.matches[1].id == "83d70527-5fc4-4fad-8dd2-b88b385f379e"

        hits = get_hits_info()
        assert hits.hits_today == 2
        assert hits.hits_used == 2
        assert hits.hits_limit == 100

def test_update_match_info():
    mock_response = Mock()
    mock_response.json.return_value = {
        "data": {
            "id": "b13f129b-2596-429d-ad49-a1b0d102809b",
            "name": "Sunrisers Hyderabad vs Punjab Kings, 27th Match",
            "matchType": "t20",
            "status": "Sunrisers Hyderabad won by 8 wkts",
            "venue": "Rajiv Gandhi International Stadium, Hyderabad",
            "date": "2025-04-12",
            "dateTimeGMT": "2025-04-12T14:00:00",
            "teams": [
                "Sunrisers Hyderabad",
                "Punjab Kings"
            ],
            "score": [
                {
                    "r": 245,
                    "w": 6,
                    "o": 20,
                    "inning": "Punjab Kings Inning 1"
                },
                {
                    "r": 247,
                    "w": 2,
                    "o": 18.3,
                    "inning": "Sunrisers Hyderabad Inning 1"
                }
            ],
            "tossWinner": "Punjab Kings",
            "tossChoice": "bat",
            "matchWinner": "Sunrisers Hyderabad",
            "series_id": "d5a498c8-7596-4b93-8ab0-e0efc3345312",
            "matchStarted": 'true',
            "matchEnded": 'true'
        },
        "status": "success",
        "info": {
           "hitsToday": 9,
           "hitsUsed": 1,
           "hitsLimit": 100,
           "credits": 0,
           "server": 4,
           "queryTime": 13.7922,
           "s": 0,
           "cache": 0
        }
    }
    mock_response.raise_for_status = Mock()
    mock_response.status_code = 200

    with patch('cricapi_ipl.modules.requests.get', return_value=mock_response):
        match = Match({
            "id": "b13f129b-2596-429d-ad49-a1b0d102809b",
            "name": "Sunrisers Hyderabad vs Punjab Kings, 27th Match",
            "matchType": "t20",
            "status": "Sunrisers Hyderabad won by 8 wkts",
            "venue": "Rajiv Gandhi International Stadium, Hyderabad",
            "date": "2025-04-12",
            "teams": [
                "Sunrisers Hyderabad",
                "Punjab Kings"
            ]
        })
        match.update_match_info()
        assert match.toss_winner == "Punjab Kings"
        assert match.toss_result == "bat"
        assert match.match_winner == "Sunrisers Hyderabad"
        assert match.innings[0].num == 1
        assert match.innings[0].team == "Punjab Kings"
        assert match.innings[0].runs == 245
        assert match.innings[0].overs == 20
        assert match.innings[0].wickets == 6
        assert match.innings[1].num == 2
        assert match.innings[1].team == "Sunrisers Hyderabad"
        assert match.innings[1].runs == 247
        assert match.innings[1].overs == 18.3
        assert match.innings[1].wickets == 2
        hits = get_hits_info()
        assert hits.hits_today == 9
        assert hits.hits_used == 1
        assert hits.hits_limit == 100