import React, {Component, PropTypes} from 'react';
import {Table} from 'react-bootstrap';
import SeasonSummaryRow from './SeasonSummaryRow';


export default (props) => {
  const seasonRows = props.seasons.map((season, index) => (
    <SeasonSummaryRow key={index} season={season} />
  ));

  return (
    <Table responsive striped hover>
      <thead>
        <tr>
          <th>Season</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody>
        {seasonRows}
      </tbody>
    </Table>
  );
}
