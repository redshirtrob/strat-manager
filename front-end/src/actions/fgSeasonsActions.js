import fetch from 'isomorphic-fetch';
import * as types from '../constants/actionTypes';

function requestFgSeasons() {
  return {
    type: types.REQUEST_FG_SEASONS
  };
}

function receiveFgSeasons(json) {
  return {
    type: types.RECEIVE_FG_SEASONS,
    seasons: json,
    receivedAt: Date.now()
  };
}

export function fetchFgSeasons() {
  return function(dispatch) {
    dispatch(requestFgSeasons);
    return fetch("http://localhost:9191/fg/seasons/")
      .then(response => response.json())
      .then(json =>
        dispatch(receiveFgSeasons(json))
      );
  }
}
