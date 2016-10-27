import React, {Component, PropTypes} from 'react';
import {connect} from 'react-redux';
import {Panel, Table} from 'react-bootstrap';
import SeasonsOverview from './SeasonsOverview';

class LeagueDetails extends Component {
  constructor(props) {
    super(props);
  }

  getLeague() {
    return this.props.leagues.find((element, index, array) => {
      return element.id === parseInt(this.props.routeParams.leagueId, 10);
    });
  }

  render() {
    const league = this.getLeague();
    return (
      <div>
        <Panel>
          <Table responsive striped>
            <thead>
              <tr>
                <th>League Name</th>
                <th>Abbreviation</th>
                <th>Commissioner</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>{league.name}</td>
                <td>{league.abbreviation}</td>
                <td>Vacant</td>
              </tr>
            </tbody>
          </Table>
        </Panel>
        <SeasonsOverview league={league} />
      </div>
    );
  }
};

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
)(LeagueDetails);
