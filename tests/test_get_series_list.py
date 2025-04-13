from cricapi_ipl.modules import get_series_list, set_api_key, get_hits_info, Series, HitInfo
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