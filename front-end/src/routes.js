import React from 'react';
import {Route, IndexRoute, Redirect} from 'react-router';

import App from './components/App';
import LeaguesOverview from './containers/LeaguesOverview';
import TeamsOverview from './containers/TeamsOverview';
import LeagueDetails from './containers/LeagueDetails';


export default (
  <Route path="/" component={App}>
    <IndexRoute component={TeamsOverview} />
    <Route path="teams" component={TeamsOverview} />
    <Route path="leagues" component={LeaguesOverview} />
    <Route path="leagues/:leagueId" component={LeagueDetails} />
    <Redirect from="*" to="/" />
  </Route>
);
