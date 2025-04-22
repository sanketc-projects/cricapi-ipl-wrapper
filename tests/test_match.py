from cricapi_ipl.modules import Innings, Team, Match, get_hits_info
import pytest
from unittest.mock import patch, Mock
from datetime import datetime

def test_match_initialization():
    match_init_json = {
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
    }
    match = Match(match_init_json)
    assert match.get_id() == "b13f129b-2596-429d-ad49-a1b0d102809b"
    assert match.get_name() == "Sunrisers Hyderabad vs Punjab Kings, 27th Match"
    assert match.get_date_str() == "April 12 2025"
    assert match.get_status() == "Sunrisers Hyderabad won by 8 wkts"
    assert match.get_venue() == "Rajiv Gandhi International Stadium, Hyderabad"
    assert match.get_home_team().name == "Sunrisers Hyderabad"
    assert match.get_home_team().short_name == "SH"
    assert match.get_away_team().name == "Punjab Kings"
    assert match.get_away_team().short_name == "PK"
    assert match.get_date() == datetime.strptime("2025-04-12", "%Y-%m-%d")
    assert match.get_match_innings_summary(1) == "Innings 0   :       - score: 000/0  Overs: 0.0"
    assert match.get_match_innings_summary(2) == "Innings 0   :       - score: 000/0  Overs: 0.0"



def test_update_match_info():
    match_init_json = {
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
    }
    match = Match(match_init_json)

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
        match.update_match_info()

    assert match.get_id() == "b13f129b-2596-429d-ad49-a1b0d102809b"
    assert match.get_name() == "Sunrisers Hyderabad vs Punjab Kings, 27th Match"
    assert match.get_date_str() == "April 12 2025"
    assert match.get_status() == "Sunrisers Hyderabad won by 8 wkts"
    assert match.get_venue() == "Rajiv Gandhi International Stadium, Hyderabad"
    assert match.get_home_team().name == "Sunrisers Hyderabad"
    assert match.get_home_team().short_name == "SH"
    assert match.get_away_team().name == "Punjab Kings"
    assert match.get_away_team().short_name == "PK"
    assert match.get_date() == datetime.strptime("2025-04-12", "%Y-%m-%d")
    assert match.get_match_innings(1).num == 1
    assert match.get_match_innings(1).team.name == "Punjab Kings"
    assert match.get_match_innings(1).team.short_name == "PK"
    assert match.get_match_innings(1).runs == 245
    assert match.get_match_innings(1).overs == 20
    assert match.get_match_innings(1).wickets == 6
    assert match.get_match_innings(2).num == 2
    assert match.get_match_innings(2).team.name == "Sunrisers Hyderabad"
    assert match.get_match_innings(2).team.short_name == "SH"
    assert match.get_match_innings(2).runs == 247
    assert match.get_match_innings(2).overs == 18.3
    assert match.get_match_innings(2).wickets == 2
    assert match.get_toss_winner().name == "Punjab Kings"
    assert match.get_toss_result() == "bat"
    assert match.get_match_winner().name == "Sunrisers Hyderabad"
    assert match.get_match_innings_summary(1) == "Innings 1   : PK    - score: 245/6  Overs: 20"
    assert match.get_match_innings_summary(2) == "Innings 2   : SH    - score: 247/2  Overs: 18.3"

    #check incorrect inning number raises error
    with pytest.raises(ValueError):
        match.get_match_innings(3)
    with pytest.raises(ValueError):
        match.get_match_innings_summary(3)
    with pytest.raises(ValueError):
        match.get_match_innings(0)
    with pytest.raises(ValueError):
        match.get_match_innings_summary(0)
    with pytest.raises(ValueError):
        match.get_match_innings(-1)
    with pytest.raises(ValueError):
        match.get_match_innings_summary(-1)

    hit_info = get_hits_info()
    assert hit_info.hits_today == 9
    assert hit_info.hits_used == 1
    assert hit_info.hits_limit == 100


