import React, {Component, PropTypes} from 'react';
import { browserHistory } from 'react-router'

class LeagueSummaryRow extends Component {
  constructor(props) {
    super(props);
  }

  onClick(event) {
    console.log(`Event: /leagues/${this.props.league.id}`);
    browserHistory.push(`/leagues/${this.props.league.id}`);
  }
  
  render() {
    return (
      <tr onClick={(e) => this.onClick(e)}>
        <td>{this.props.number}</td>
        <td>{this.props.league.name}</td>
        <td>{this.props.league.abbreviation}</td>
        <td>{this.props.league.seasons.length}</td>
        <td>Vacant</td>
      </tr>
    );
  }
};

export default LeagueSummaryRow;
