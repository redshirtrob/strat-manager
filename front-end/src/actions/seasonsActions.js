import fetch from 'isomorphic-fetch';
import {fetchLeagues} from './leaguesActions';

export function createSeason(name, seasonToClone, leagueId) {
  const body = {
    year: name,
    name: name,
    league_id: leagueId
  };

  return function(dispatch) {
    return fetch(
      "http://localhost:9191/blb/seasons/", {
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

export function createDivision(name, seasonId) {
  const body = {
    name: name,
    season_id: seasonId
  }

  console.log(JSON.stringify(body));

  return function(dispatch) {
    return fetch(
      "http://localhost:9191/blb/divisions/", {
        method: "POST",
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(body)
      }
    ).then(response =>
      fetchLeagues()(dispatch)
    );
  }
}
