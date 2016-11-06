import {combineReducers} from 'redux';

// import all app reducers
import leagues from './leagues';
import fgSeasons from './fgSeasons';


const rootReducer = combineReducers({
  leagues,
  fgSeasons
});

export default rootReducer;
