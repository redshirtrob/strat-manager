import fetch from 'isomorphic-fetch';
import {fetchLeagues} from './leaguesActions';

export function createSeason(referenceSeason, name, seasonToClone, leagueId) {
  const body = {
    fg_season_id: referenceSeason,
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