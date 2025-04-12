from cricapi_ipl.modules import get_series_list, Series, set_api_key
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
                "endDate": "2023-05-29"
            },
            {
                "id": "2",
                "name": "Some Other Series",
                "matches": 50,
                "startDate": "2023-06-01",
                "endDate": "2023-07-01"
            }
        ]
    }
    mock_response.raise_for_status = Mock()
    mock_response.status_code = 200

    with patch('cricapi_ipl.modules.requests.get', return_value=mock_response):
        series_list = get_series_list()
        assert len(series_list) == 1
        assert series_list[0].name == "Indian Premier League 2023"
        assert series_list[0].num_matches == 70
        assert series_list[0].start_date == "2023-03-31"
        assert series_list[0].end_date == "2023-05-29"
        assert series_list[0].id == "1"