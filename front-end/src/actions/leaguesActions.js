import fetch from 'isomorphic-fetch';
import * as types from '../constants/actionTypes';

function requestLeagues() {
  return {
    type: types.REQUEST_LEAGUES
  };
}

function receiveLeagues(json) {
  return {
    type: types.RECEIVE_LEAGUES,
    leagues: json,
    receivedAt: Date.now()
  };
}

function addLeague(league) {
  return {
    type: types.ADD_LEAGUE,
    league: league,
    receivedAt: Date.now()
  };
}

export function fetchLeagues() {
  return function(dispatch) {
    dispatch(requestLeagues);
    return fetch("http://localhost:9191/blb/leagues/")
      .then(response => response.json())
      .then(json =>
        dispatch(receiveLeagues(json))
      );
  }
}

export function createLeague(name, abbreviation) {
  const body = {
    name,
    abbreviation
  };
  
  return function(dispatch) {
    return fetch(
      "http://localhost:9191/blb/leagues/", {
        method: "POST",
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(body)
      }).then(response =>
        fetchLeagues()(dispatch)
      );
  }
}
