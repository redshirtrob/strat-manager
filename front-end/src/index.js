import 'babel-polyfill';

import React from 'react';
import ReactDOM from 'react-dom';
import {Router, hashHistory} from 'react-router';
import {Provider} from 'react-redux';

import routes from './routes';
import configureStore from './store/configureStore';
import Bootstrap from 'bootstrap/dist/css/bootstrap-flatly.css';
import {fetchLeagues} from './actions/leaguesActions';


const
  STORE = configureStore(),
  ROOT_ELEMENT = 'main';

let ProjectElement;

if (process.env.NODE_ENV !== 'production') {
  // development
  const DevTools = window.devToolsExtension
    ? () => null
    : require('./containers/DevTools').default;

  ProjectElement = (
    <div>
      <Router history={hashHistory} routes={routes} />
      <DevTools />
    </div>
  );
} else {
  // production
  ProjectElement = <Router history={hashHistory} routes={routes} />;
}

// handle client side rendering
if (typeof document !== 'undefined') {

  ReactDOM.render(
    <Provider store={STORE}>
      {ProjectElement}
    </Provider>,
    document.getElementById(ROOT_ELEMENT)
  );
}

STORE.dispatch(fetchLeagues());
