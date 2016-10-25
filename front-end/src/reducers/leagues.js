import * as types from '../constants/actionTypes';

const initialState = {
  isFetching: false,
  didInvalidate: false,
  leagues: []
};

export default function leagues(state = initialState, action) {
  switch (action.type) {
    case types.REQUEST_LEAGUES:
      return Object.assign({}, state, {
        isFetching: true,
        didInvalidate: false
      });
    case types.RECEIVE_LEAGUES:
      return Object.assign({}, state, {
        isFetching: false,
        didInvalidate: false,
        leagues: action.leagues,
        lastUpdated: action.receivedAt
      });
    case types.ADD_LEAGUE:
      return Object.assign({}, state, {
        isFetching: false,
        didInvalidate: false,
        leagues: [...state.leagues, action.league],
        lastUpdated: action.receivedAt
      });
    default:
      return state;
  }
}
