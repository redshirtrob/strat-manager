import React, {Component, PropTypes} from 'react';
import {connect} from 'react-redux';
import {Button, Panel, Table} from 'react-bootstrap';
import TeamSummaryRow from './TeamSummaryRow';
import {createTeam} from '../actions/seasonsActions';
import AddTeam from './AddTeam';

class SeasonTeams extends Component {
  constructor(props) {
    super(props);
    this.state = {
      addingNewTeam: false
    }
  }

  onClick(event) {
    this.setState({
      addingNewTeam: true
    });
  }

  onCloseAddTeamClick() {
    this.setState({
      addingNewTeam: false
    });
  }

  render() {
    let bottom;
    if (this.state.addingNewTeam === true) {
      bottom = (
        <AddTeam
            season={this.props.season}
            onAddTeamClick={this.props.onAddTeamClick.bind(this)}
            onCloseClick={this.onCloseAddTeamClick.bind(this)}
        />
      );
    } else {
      bottom = (
        <Button bsStyle="primary" bsSize="small" onClick={(e) => this.onClick(e)}>Add Team</Button>
      );
    }

    return (
      <div>
        <Panel>
          <Table responsive striped>
            <thead>
              <tr>
                <td>Location</td>
                <td>Name</td>
                <td>Abbreviation</td>
                <td>Division</td>
                <td>Owner</td>
              </tr>
            </thead>
            <tbody>
              {this.props.season && this.props.season.teams.map((team, index) => (
                 <TeamSummaryRow key={index} team={team} divisions={this.props.season.divisions}/>
               ))
              }
            </tbody>
          </Table>
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
    onAddTeamClick: function(location, name, abbreviation, division_id, owner_id) {
      dispatch(createTeam(
        location,
        name,
        abbreviation,
        this.props.season.id,
        division_id,
        owner_id)
      );
      this.setState({
        addingNewTeam: false
      });
    }
  }
}

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(SeasonTeams);
