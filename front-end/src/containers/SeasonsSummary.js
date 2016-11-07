import React, {Component, PropTypes} from 'react';
import {Table} from 'react-bootstrap';
import SeasonSummaryRow from './SeasonSummaryRow';

export default (props) => {
  const seasonRows = props.seasons.map((season, index) => {
    const fgSeason = props.fgSeasons.find((fgSeason) => {
      return fgSeason.id === season.fg_season_id
    });
    
    return (
      <SeasonSummaryRow key={index} season={season} fgSeason={fgSeason}/>
    );
  });

  return (
    <Table responsive striped hover>
      <thead>
        <tr>
          <th>Season</th>
          <th>MLB Season</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody>
        {seasonRows}
      </tbody>
    </Table>
  );
}
