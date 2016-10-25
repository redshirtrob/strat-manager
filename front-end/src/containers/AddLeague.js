import React, {Component, PropTypes} from 'react';
import {
  Button,
  ControlLabel,
  Form,
  FormControl,
  FormGroup,
  Panel
} from 'react-bootstrap';

class AddLeague extends Component {
  constructor(props) {
    super(props);
    this.state = {
      leagueName: '',
      leagueAbbreviation: ''
    };
    this.onNameChange = this.onNameChange.bind(this);
    this.onAbbreviationChange = this.onAbbreviationChange.bind(this);
  }
  
  onClick() {
    this.props.onAddLeagueClick(this.state.leagueName, this.state.leagueAbbreviation);
  }

  onNameChange(event) {
    this.setState({
      ...this.state,
      leagueName: event.target.value
    });
  }

  onAbbreviationChange(event) {
    this.setState({
      ...this.state,
      leagueAbbreviation: event.target.value
    });
  }

  render() {
    return (
      <Panel>
        <Form>
          <ControlLabel>New League</ControlLabel>
          <FormGroup controlId="formHorizontalName">
            <FormControl
                type="text"
                value={this.state.leagueName}
                onChange={this.onNameChange}
                placeholder="League Name" />
          </FormGroup>
          <FormGroup controlId="formHorizontalName">
            <FormControl
                type="text"
                value={this.state.leagueAbbreviation}
                onChange={this.onAbbreviationChange}
                placeholder="Abbreviation" />
          </FormGroup>
          <Button onClick={this.onClick.bind(this)}>Create</Button>
        </Form>
      </Panel>
    );
  }
}

export default AddLeague;
