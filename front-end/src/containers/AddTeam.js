import React, {Component, PropTypes} from 'react';
import {
  Button,
  ControlLabel,
  Form,
  FormControl,
  FormGroup,
  Panel
} from 'react-bootstrap';

class AddTeam extends Component {
  constructor(props) {
    super(props);

    this.state = {
      location: '',
      nickname: '',
      abbreviation: '',
      divisionId: 0,
      ownerId: 0
    }

    this.onLocationChange = this.onLocationChange.bind(this);
    this.onNicknameChange = this.onNicknameChange.bind(this);
    this.onAbbreviationChange = this.onAbbreviationChange.bind(this);
    this.onDivisionChange = this.onDivisionChange.bind(this);
    this.onOwnerChange = this.onOwnerChange.bind(this);
  }

  onClick() {
    this.props.onAddTeamClick(
      this.state.location,
      this.state.nickname,
      this.state.abbreviation,
      this.state.divisionId,
      this.state.ownerId
    );
  }

  onLocationChange(event) {
    this.setState({
      location: event.target.value
    });
  }

  onNicknameChange(event) {
    this.setState({
      nickname: event.target.value
    });
  }

  onAbbreviationChange(event) {
    this.setState({
      abbreviation: event.target.value
    });
  }

  onDivisionChange(event) {
    this.setState({
      divisionId: event.target.value
    });
  }

  // TODO: Add UI and update
  onOwnerChange(event) {
  }

  render() {
    return (
      <Panel>
        <Form>
          <ControlLabel>New Team</ControlLabel>
          <Button className="close" onClick={(e) => this.props.onCloseClick(e)}>x</Button>
          <FormGroup bsSize="small" controlId="formHorizontalName">
            <FormControl
                type="text"
                value={this.state.location}
                onChange={this.onLocationChange}
                placeholder="Location"
            />
          </FormGroup>
          
          <FormGroup bsSize="small" controlId="formHorizontalName">
            <FormControl
                type="text"
                value={this.state.nickname}
                onChange={this.onNicknameChange}
                placeholder="Name"
            />
          </FormGroup>
          
          <FormGroup bsSize="small" controlId="formHorizontalName">
            <FormControl
                type="text"
                value={this.state.abbreviation}
                onChange={this.onAbbreviationChange}
                placeholder="Abbreviation"
            />
          </FormGroup>
          
          <FormGroup bsSize="small" controlId="formControlsSelect">
            <ControlLabel>Division</ControlLabel>
            <FormControl
                componentClass="select"
                onChange={this.onDivisionChange}
                placeholder="select">
              <option key="0" value="0">Select Division</option>
              {
                this.props.season.divisions.map((division, index) => {
                  return (
                    <option key={division.id} value={division.id}>{division.name}</option>
                  );
                })
              }
            </FormControl>
          </FormGroup>

          <Button onClick={this.onClick.bind(this)}>Add</Button>
        </Form>
      </Panel>
    );
  }
}

export default AddTeam;
