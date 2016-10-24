import {combineReducers} from 'redux';

// import all app reducers
import leagues from './leagues';


const rootReducer = combineReducers({
  leagues,
});

export default rootReducer;
