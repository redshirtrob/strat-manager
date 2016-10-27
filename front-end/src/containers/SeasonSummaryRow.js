import React, {Component, PropTypes} from 'react';
import { browserHistory } from 'react-router'

class SeasonSummaryRow extends Component {
  constructor(props) {
    super(props);
  }

  onClick(event) {
    console.log(`Event: /leagues/seasons/${this.props.season.id}`);
    browserHistory.push(`/leagues/season/${this.props.season.id}`);
  }
  
  render() {
    return (
      <tr onClick={(e) => this.onClick(e)}>
        <td>{this.props.season.name}</td>
        <td>Completed</td>
      </tr>
    );
  }
};

export default SeasonSummaryRow;
