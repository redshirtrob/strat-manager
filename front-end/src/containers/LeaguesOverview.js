import React, {Component, PropTypes} from 'react';
import {connect} from 'react-redux';
import {Button, Col, Panel, Row} from 'react-bootstrap';
import LeaguesSummary from './LeaguesSummary';
import AddLeague from './AddLeague';
import {createLeague} from '../actions/leaguesActions';

class LeaguesOverview extends Component {
  constructor(props) {
    super(props);
    this.state = {
      addingNewLeague: false
    };
  }
  
  onClick() {
    this.setState({
      addingNewLeague: true
    });
  }

  render() {
    let bottom;
    if (this.state.addingNewLeague === true) {
      bottom = (
        <AddLeague onAddLeagueClick={this.props.onAddLeagueClick.bind(this)} />
      );
    } else {
      bottom = (
        <Button bsStyle="primary" bsSize="small" onClick={this.onClick.bind(this)}>Add League</Button>
      );
    }
    
    return (
      <div>
        <Panel>
          <LeaguesSummary leagues={this.props.leagues} />
        </Panel>
        {bottom}
      </div>
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
    onAddLeagueClick: function(name, abbreviation) {
      dispatch(createLeague(name, abbreviation));
      this.setState({
        addingNewLeague: false
      });
    }
  };
}

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(LeaguesOverview);
