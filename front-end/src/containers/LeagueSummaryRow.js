import React, {Component, PropTypes} from 'react';

export default (props) => {
  return (
    <tr>
      <td>{props.number}</td>
      <td>{props.league.name}</td>
      <td>{props.league.abbreviation}</td>
      <td>{props.league.seasons.length}</td>
      <td>Vacant</td>
    </tr>
  );
};
