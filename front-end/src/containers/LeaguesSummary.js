import React, {Component, PropTypes} from 'react';
import {Table} from 'react-bootstrap';
import LeagueSummaryRow from './LeagueSummaryRow';

export default (props) => {
  const leagueRows =props.leagues.map((league, index) => (
    <LeagueSummaryRow key={index} number={index+1} league={league} />
  ));

  return (
    <Table responsive striped hover>
      <thead>
        <tr>
          <th>#</th>
          <th>League Name</th>
          <th>Abbreviation</th>
          <th>Seasons</th>
          <th>Commissioner</th>
        </tr>
      </thead>
      <tbody>
        {leagueRows}
      </tbody>
    </Table>
  );
};
