import React, {Component, PropTypes} from 'react';
import {connect} from 'react-redux';
import {Button, Panel} from 'react-bootstrap';
import SeasonsSummary from './SeasonsSummary';
import AddSeason from './AddSeason';
import {createSeason} from '../actions/seasonsActions';

class SeasonsOverview extends Component {
  constructor(props) {
    super(props);
    this.state = {
      addingNewSeason: false
    };
  }

  onClick(event) {
    this.setState({
      addingNewSeason: true
    });
  }

  render() {
    let bottom;
    if (this.state.addingNewSeason === true) {
      bottom = (
        <AddSeason
            seasons={this.props.league.seasons}
            onAddSeasonClick={this.props.onAddSeasonClick.bind(this)}
        />
      );
    } else {
      bottom = (
        <Button bsStyle="primary" bsSize="small" onClick={(e) => this.onClick(e)}>Add Season</Button>
      );
    }
    
    return (
      <div>
        <Panel>
          <SeasonsSummary seasons={this.props.league.seasons} />
        </Panel>
        {bottom}
      </div>
    );
  }
}

function mapStateToProps(state) {
  return {
  };
}

function mapDispatchToProps(dispatch) {
  return {
    onAddSeasonClick: function(name, seasonToClone) {
      dispatch(createSeason(name, seasonToClone, this.props.league.id));
      this.setState({
        addingNewSeason: false
      });
    }
  };
}

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(SeasonsOverview);
