# cricapi-ipl-wrapper
Python wrapper for getting IPL match details from cricapi. I have no affiliations with cricapi and this project is just a hobby project for me.

## Installation
pip install cricapi_ipl

## Usage
### Setting API key
To get cricket match info from cricapi in json format we will first need to [sign up](https://cricketdata.org/member.aspx) and get an API key. With the free subscription, there are per-day hit limit of around 100. In other words in free subscription you can invoke a total of 100 APIs in a day. Once you get the API key, you will need to set it using `set_api_key()` function as shown below. The key used here is just for representation and is not a real cricapi API key
```
>>> import cricapi_ipl as ipl
>>>
>>>
>>> ipl.set_api_key("abcdef12-3456-789a-bcde-f0123456789a")
```

### Getting the list of IPL series
The `get_series_list()` will return a list of `Series` objects corresponding to the list of IPL series supported by circapi
```
>>>
>>> series_list = ipl.get_series_list()
>>>
>>>
>>> for series in series_list:
...     print(series)
...
Indian Premier League 2025     Matches: 74    Start Date: March 22 2025   End Date: May 25 2025
Indian Premier League 2024     Matches: 74    Start Date: March 22 2024   End Date: May 26 2024
Indian Premier League 2023     Matches: 75    Start Date: March 31 2023   End Date: May 28 2023
Indian Premier League 2022     Matches: 74    Start Date: March 26 2022   End Date: May 29 2022
>>>
>>>
>>> series_list[0]
Indian Premier League 2025     Matches: 74    Start Date: March 22 2025   End Date: May 25 2025
```

### Update matches for a series
Each `Series` object will have a list of `Match` objects. Invoking `update_matches()` function of the `Series` object will fetch all the basic match details for that series
```
>>>
>>>
>>> series_list[0].update_matches()
>>>
>>>
>>> series_list[0].matches[0]
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
    ],
    "fantasyEnabled": true,
    "bbbEnabled": true,
    "hasSquad": true,
    "matchStarted": true,
    "matchEnded": true
}
```

### Get more details about the match
The `Match` object has `update_match_info()` function which will fetch scores for a completed match
```
>>> series_list[0].matches[0].update_match_info()
>>> series_list[0].matches[0]
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
    ],
    "score": [
        {
            "r": 155,
            "w": 9,
            "o": 20,
            "inning": "Mumbai Indians Inning 1"
        },
        {
            "r": 158,
            "w": 6,
            "o": 19.1,
            "inning": "Chennai Super Kings Inning 1"
        }
    ],
    "tossWinner": "Chennai Super Kings",
    "tossChoice": "bowl",
    "matchWinner": "Chennai Super Kings",
    "series_id": "d5a498c8-7596-4b93-8ab0-e0efc3345312",
    "fantasyEnabled": true,
    "bbbEnabled": true,
    "hasSquad": true,
    "matchStarted": true,
    "matchEnded": true
}
>>> print(series_list[0].matches[0])
March 23 2025   Chennai Super Kings vs Mumbai Indians, 3rd Match Chennai Super Kings won by 4 wkts
	Innings 1   : MI    - score: 155/9  Overs: 20
	Innings 2   : CSK   - score: 158/6  Overs: 19.1
>>>
```

### Current hit limits
To see the API hit limits use `get_hits_info()` of the module
```
>>> hit_info = ipl.get_hits_info()
>>> hit_info
Hits Today: 3 Hits Used: 1 Hits Limit: 100
```

## Developer Info
If you are interested in forking this project and adding more enhancements then below steps should get you started

```
python -m venv .venv
source .venv/bin/activate
pip install -e .
pip install -e '.[dev]'
pytest -vv
```
