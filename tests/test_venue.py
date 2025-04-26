from cricapi_ipl.venue import Venue
import pytest

def test_venue_initialization():
    venue = Venue("Wankhede Stadium, Mumbai")
    assert venue.name == "Wankhede Stadium"
    assert venue.city == "Mumbai"
    assert str(venue) == "Wankhede Stadium, Mumbai"
    assert repr(venue) == "Wankhede Stadium, Mumbai"

def test_venue_equality():
    venue1 = Venue("Wankhede Stadium, Mumbai")
    venue2 = Venue("Wankhede Stadium, Mumbai")
    venue3 = Venue("Eden Gardens, Kolkata")

    assert venue1 == venue2
    assert venue1 != venue3
    assert hash(venue1) == hash(venue2)
    assert hash(venue1) != hash(venue3)
