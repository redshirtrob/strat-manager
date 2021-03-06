import React, {Component, PropTypes} from 'react';
import {connect} from 'react-redux';
import SeasonDivisions from './SeasonDivisions';
import SeasonTeams from './SeasonTeams';

class SeasonDetails extends Component {
  constructor(props) {
    super(props);
  }

  getSeason() {
    if (this.props.leagues !== undefined) {
      const league = this.props.leagues.find((league, index, array) => {
        return league.seasons.find((season, index, array) => {
          return season.id === parseInt(this.props.routeParams.seasonId, 10);
        });
      });
      if (league !== undefined) {
        return league.seasons.find((season, index, array) => {
          return season.id === parseInt(this.props.routeParams.seasonId, 10);
        });
      }
    }
  }

  render() {
    const season = this.getSeason();
    console.log(JSON.stringify(season));
    return (
      <div>
      {season &&
       <div>
         <SeasonDivisions season={season} />
         <div className="form-group">&nbsp;</div>
         <SeasonTeams season={season} />
       </div>
      }
      </div>
    );
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
)(SeasonDetails);
