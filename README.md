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
The `get_series_map()` will return a list of `Series` objects corresponding to the list of IPL series supported by circapi
```
>>>
>>> series_map = ipl.get_series_map()
>>>
>>>
>>> for year, series in series_map.items():
...     print(series)
...
Indian Premier League 2025     Matches: 74    Start Date: March 22 2025   End Date: May 25 2025
Indian Premier League 2024     Matches: 74    Start Date: March 22 2024   End Date: May 26 2024
Indian Premier League 2023     Matches: 75    Start Date: March 31 2023   End Date: May 28 2023
Indian Premier League 2022     Matches: 74    Start Date: March 26 2022   End Date: May 29 2022
>>>
>>>
>>> series_map[2025]
{
    "id": "d5a498c8-7596-4b93-8ab0-e0efc3345312",
    "name": "Indian Premier League 2025",
    "startDate": "2025-03-22",
    "endDate": "May 25",
    "odi": 0,
    "t20": 74,
    "test": 0,
    "squads": 10,
    "matches": 74
}
```

### Update matches for a series
Each `Series` object will have a list of `Match` objects. Invoking `update_matches()` function of the `Series` object will fetch all the basic match details for that series
```
>>>
>>>
>>> series_map[2025].update_matches()
>>>
>>>
>>> series_map[2025].matches[0]
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

After running update matches you can also get the set of teams and venues of that series
```
>>> for c, v in series_map[2025].venues.items():
...     print(v)
...
Barsapara Cricket Stadium, Guwahati
Narendra Modi Stadium, Ahmedabad
Arun Jaitley Stadium, Delhi
MA Chidambaram Stadium, Chennai
Eden Gardens, Kolkata
Rajiv Gandhi International Stadium, Hyderabad
Dr. Y.S. Rajasekhara Reddy ACA-VDCA Cricket Stadium, Visakhapatnam
M.Chinnaswamy Stadium, Bengaluru
Sawai Mansingh Stadium, Jaipur
Himachal Pradesh Cricket Association Stadium, Dharamsala
Wankhede Stadium, Mumbai
Maharaja Yadavindra Singh International Cricket Stadium, Mullanpur, Chandigarh
Bharat Ratna Shri Atal Bihari Vajpayee Ekana Cricket Stadium, Lucknow
>>>
>>>
>>> for k, t in series_map[2025].teams.items():
...     print(t)
...
GT    - Gujarat Titans
SRH   - Sunrisers Hyderabad
LSG   - Lucknow Super Giants
CSK   - Chennai Super Kings
MI    - Mumbai Indians
KKR   - Kolkata Knight Riders
RR    - Rajasthan Royals
DC    - Delhi Capitals
PBKS  - Punjab Kings
RCB   - Royal Challengers Bengaluru
>>>
```

### Get more details about the match
The `Match` object has `update_match_info()` function which will fetch scores for a completed match
```
>>> series_map[2025].matches[0].update_match_info()
>>> series_map[2025].matches[0]
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
>>> print(series_map[2025].matches[0])
March 23 2025   Chennai Super Kings vs Mumbai Indians, 3rd Match Chennai Super Kings won by 4 wkts
	Innings 1   : MI    - score: 155/9  Overs: 20
	Innings 2   : CSK   - score: 158/6  Overs: 19.1
>>>
```

### Get all the matches for a team
```
>>> series_map[2024].update_matches()
>>>
>>>
>>> rcb_match_list = series_map[2024].get_matches_for_team('RCB')
>>>
>>>
>>> import time
>>> for match in rcb_match_list:
...     match.update_match_info()
...     time.sleep(2)
...     print(match)
...
April 06 2024   Rajasthan Royals vs Royal Challengers Bengaluru, 19th Match Rajasthan Royals won by 6 wkts
	Innings 1   : RCB   - score: 183/3  Overs: 20
	Innings 2   : RR    - score: 189/4  Overs: 19.1
April 28 2024   Gujarat Titans vs Royal Challengers Bengaluru, 45th Match Royal Challengers Bengaluru won by 9 wkts
	Innings 1   : GT    - score: 200/3  Overs: 20
	Innings 2   : RCB   - score: 206/1  Overs: 16
May 12 2024     Royal Challengers Bengaluru vs Delhi Capitals, 62nd Match Royal Challengers Bengaluru won by 47 runs
	Innings 1   : RCB   - score: 187/9  Overs: 20
	Innings 2   : DC    - score: 140/10 Overs: 19.1
May 04 2024     Royal Challengers Bengaluru vs Gujarat Titans, 52nd Match Royal Challengers Bengaluru won by 4 wkts
	Innings 1   : GT    - score: 147/10 Overs: 19.3
	Innings 2   : RCB   - score: 152/6  Overs: 13.4
May 09 2024     Punjab Kings vs Royal Challengers Bengaluru, 58th Match Royal Challengers Bengaluru won by 60 runs
	Innings 1   : RCB   - score: 241/7  Overs: 20
	Innings 2   : PBKS  - score: 181/10 Overs: 17
May 18 2024     Royal Challengers Bengaluru vs Chennai Super Kings, 68th Match Royal Challengers Bengaluru won by 27 runs
	Innings 1   : RCB   - score: 218/5  Overs: 20
	Innings 2   : CSK   - score: 191/7  Overs: 20
April 11 2024   Mumbai Indians vs Royal Challengers Bengaluru, 25th Match Mumbai Indians won by 7 wkts
	Innings 1   : RCB   - score: 196/8  Overs: 20
	Innings 2   : MI    - score: 199/3  Overs: 15.3
April 15 2024   Royal Challengers Bengaluru vs Sunrisers Hyderabad, 30th Match Sunrisers Hyderabad won by 25 runs
	Innings 1   : SRH   - score: 287/3  Overs: 20
	Innings 2   : RCB   - score: 262/7  Overs: 20
March 25 2024   Royal Challengers Bengaluru vs Punjab Kings, 6th Match Royal Challengers Bengaluru won by 4 wkts
	Innings 1   : PBKS  - score: 176/6  Overs: 20
	Innings 2   : RCB   - score: 178/6  Overs: 19.2
March 22 2024   Chennai Super Kings vs Royal Challengers Bengaluru, 1st Match Chennai Super Kings won by 6 wkts
	Innings 1   : RCB   - score: 173/6  Overs: 20
	Innings 2   : CSK   - score: 176/4  Overs: 18.4
April 21 2024   Kolkata Knight Riders vs Royal Challengers Bengaluru, 36th Match Kolkata Knight Riders won by 1 run
	Innings 1   : KKR   - score: 222/6  Overs: 20
	Innings 2   : RCB   - score: 221/10 Overs: 20
April 25 2024   Sunrisers Hyderabad vs Royal Challengers Bengaluru, 41st Match Royal Challengers Bengaluru won by 35 runs
	Innings 1   : RCB   - score: 206/7  Overs: 20
	Innings 2   : SHCB  - score: 171/8  Overs: 20
March 29 2024   Royal Challengers Bengaluru vs Kolkata Knight Riders, 10th Match Kolkata Knight Riders won by 7 wkts
	Innings 1   : RCB   - score: 182/6  Overs: 20
	Innings 2   : KKR   - score: 186/3  Overs: 16.5
May 22 2024     Rajasthan Royals vs Royal Challengers Bengaluru, Eliminator Rajasthan Royals won by 4 wkts
	Innings 1   : RCB   - score: 172/8  Overs: 20
	Innings 2   : RR    - score: 174/6  Overs: 19
April 02 2024   Royal Challengers Bengaluru vs Lucknow Super Giants, 15th Match Lucknow Super Giants won by 28 runs
	Innings 1   : LSG   - score: 181/5  Overs: 20
	Innings 2   : RCB   - score: 153/10 Overs: 19.4
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
