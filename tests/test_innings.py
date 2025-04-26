from cricapi_ipl.match import Innings
from cricapi_ipl.team import Team
import pytest

def test_innings_initialization():
    innings = Innings()
    assert innings.num == 0
    assert innings.team.name== ""
    assert innings.runs == 0
    assert innings.overs == 0.0
    assert innings.wickets == 0
    assert str(innings) == "Innings 0   :       - score: 000/0  Overs: 0.0"

def test_team_score_less_than_100():
    innings = Innings()
    innings.num = 1
    innings.team = Team("Delhi Capitals")
    innings.runs = 95
    innings.overs = 10.3
    innings.wickets = 2
    assert str(innings) == "Innings 1   : DC    - score: 095/2  Overs: 10.3"

def test_team_score_greater_than_100():
    innings = Innings()
    innings.num = 2
    innings.team = Team("Mumbai Indians")
    innings.runs = 150
    innings.overs = 18.5
    innings.wickets = 5
    assert str(innings) == "Innings 2   : MI    - score: 150/5  Overs: 18.5"

def test_team_all_out():
    innings = Innings()
    innings.num = 1
    innings.team = Team("Royal Challengers Bangalore")
    innings.runs = 80
    innings.overs = 20.0
    innings.wickets = 10
    assert str(innings) == "Innings 1   : RCB   - score: 080/10 Overs: 20.0"