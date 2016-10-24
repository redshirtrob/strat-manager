import React from 'react';
import {Route, IndexRoute, Redirect} from 'react-router';

import App from './components/App';
import LeaguesOverview from './containers/LeaguesOverview';
import TeamsOverview from './containers/TeamsOverview';


export default (
  <Route path="/" component={App}>
    <IndexRoute component={TeamsOverview} />
    <Route path="#teams" component={TeamsOverview} />
    <Route path="#leagues" component={LeaguesOverview} />
    <Redirect from="*" to="/" />
  </Route>
);
