from cricapi_ipl.modules import Team
import pytest

def test_team_initialization():
    team = Team("Sunrisers Hyderabad")
    assert team.name == "Sunrisers Hyderabad"
    assert team.short_name == "SH"
    assert str(team) == "SH  - Sunrisers Hyderabad"
    assert repr(team) == "SH  - Sunrisers Hyderabad"

def test_team_equality():
    team1 = Team("Sunrisers Hyderabad")
    team2 = Team("Sunrisers Hyderabad")
    team3 = Team("Punjab Kings")
    assert team1 == team2
    assert team1 != team3
    assert hash(team1) == hash(team2)
    assert hash(team1) != hash(team3)