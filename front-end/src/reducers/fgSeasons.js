import * as types from '../constants/actionTypes';

const initialState = {
  isFetching: false,
  didInvalidate: false,
  seasons: []
};

export default function fgSeasons(state = initialState, action) {
  switch (action.type) {
    case types.REQUEST_FG_SEASONS:
      return Object.assign({}, state, {
        isFetching: true,
        didInvalidate: false
      });
    case types.RECEIVE_FG_SEASONS:
      return Object.assign({}, state, {
        isFetching: false,
        didInvalidate: false,
        fgSeasons: action.seasons,
        lastUpdated: action.receivedAt
      });
    default:
      return state;
  }
}
