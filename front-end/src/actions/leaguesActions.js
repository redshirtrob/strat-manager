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

export function fetchLeagues() {
  return function(dispatch) {
    dispatch(requestLeagues);
    return fetch('http://localhost:9191/blb/leagues/')
      .then(response => response.json())
      .then(json =>
        dispatch(receiveLeagues(json))
      )
  }
}
