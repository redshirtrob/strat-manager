import pytest

from data.sql_store import SQLStore

GOOD_YEAR = '2008'
BAD_YEAR = '2007'

BAD_PLAYER_ID = 10000000 # We should never cross this

@pytest.mark.gen_test
def test_get_seasons():
    """Fetch seasons from data store"""
    store = SQLStore()
    seasons = yield store.get_seasons()
    assert len(seasons) == 8
    
@pytest.mark.gen_test
def test_get_players_by_year():
    """Fetch players from data store"""
    store = SQLStore()
    players = yield store.get_players_by_year(year=GOOD_YEAR)
    assert len(players) > 0

    players = yield store.get_players_by_year(year=BAD_YEAR)
    assert players is None

@pytest.mark.gen_test
def test_get_batting_by_year():
    """Fetch batting statistics by year"""
    store = SQLStore()
    batting = yield store.get_batting_by_year(year=GOOD_YEAR)
    assert len(batting) > 0

    batting = yield store.get_batting_by_year(year=BAD_YEAR)
    assert batting is None

@pytest.mark.gen_test
def test_get_batting_by_player():
    """Fetch batting statistics by player"""
    store = SQLStore()
    batting = yield store.get_batting_by_player(player_id=1) # Known batter
    assert len(batting) == 3

    batting = yield store.get_batting_by_player(player_id=BAD_PLAYER_ID)
    assert batting is None
    
@pytest.mark.gen_test
def test_get_pitching_by_year():
    """Fetch pitching statistics by year"""
    store = SQLStore()
    batting = yield store.get_pitching_by_year(year=GOOD_YEAR)
    assert len(batting) > 0

    batting = yield store.get_pitching_by_year(year=BAD_YEAR)
    assert batting is None

@pytest.mark.gen_test
def test_get_pitching_by_player():
    """Fetch pitching statistics by player"""
    store = SQLStore()
    batting = yield store.get_pitching_by_player(player_id=684) # Known pitcher
    assert len(batting) == 2

    batting = yield store.get_pitching_by_player(player_id=BAD_PLAYER_ID)
    assert batting is None
