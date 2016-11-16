import React, {Component, PropTypes} from 'react';

class TeamSummaryRow extends Component {
  constructor(props) {
    super(props);
  }

  getDivisionName() {
    const division = this.props.divisions.find((division, index, array) => {
      return division.id === this.props.team.division_id;
    });
    return division.name;
  }

  render() {
    return (
      <tr>
        <td>{this.props.team.location}</td>
        <td>{this.props.team.nickname}</td>
        <td>{this.props.team.abbreviation}</td>
        <td>{this.getDivisionName()}</td>
        <td>Vacant</td>
      </tr>
    );
  }
}

export default TeamSummaryRow;
