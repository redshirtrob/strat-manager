import React, {Component, PropTypes} from 'react';

class DivisionSummaryRow extends Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <tr>
        <td>{this.props.division.name}</td>
        <td>{this.props.division.teams.length}</td>
      </tr>
    );
  }
};

export default DivisionSummaryRow;
