import React, {Component, PropTypes} from 'react';
import {connect} from 'react-redux';
import {bindActionCreators} from 'redux';
import {Table} from 'react-bootstrap';
import LeagueSummaryRow from './LeagueSummaryRow';

class LeaguesOverview extends Component {
  render () {
    const leagueRows =this.props.leagues.map((league, index) => (
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
    )
  }
}

function mapStateToProps(state) {
  return {
    leagues: state.leagues.leagues
  };
}

function mapDispatchToProps(dispatch) {
  return {
  };
}

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(LeaguesOverview);
