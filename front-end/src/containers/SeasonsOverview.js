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

  onCloseAddSeasonClick() {
    this.setState({
      addingNewSeason: false
    });
  }
  
  render() {
    let bottom;
    if (this.state.addingNewSeason === true) {
      bottom = (
        <AddSeason
            fgSeasons={this.props.fgSeasons}
            seasons={this.props.league.seasons}
            onAddSeasonClick={this.props.onAddSeasonClick.bind(this)}
            onCloseClick={this.onCloseAddSeasonClick.bind(this)}
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
          <SeasonsSummary seasons={this.props.league.seasons} fgSeasons={this.props.fgSeasons}/>
        </Panel>
        {bottom}
      </div>
    );
  }
}

function mapStateToProps(state) {
  return {
    fgSeasons: state.fgSeasons.fgSeasons
  };
}

function mapDispatchToProps(dispatch) {
  return {
    onAddSeasonClick: function(referenceSeason, name, seasonToClone) {
      dispatch(createSeason(referenceSeason, name, seasonToClone, this.props.league.id));
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
