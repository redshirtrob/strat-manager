import React, {Component, PropTypes} from 'react';
import {
  Button,
  ControlLabel,
  Form,
  FormControl,
  FormGroup,
  Panel
} from 'react-bootstrap';

class AddSeason extends Component {
  constructor(props) {
    super(props);
    
    this.state = {
      seasonName: '',
      seasonToClone: '0'
    };

    this.onNameChange = this.onNameChange.bind(this);
    this.onSeasonToCloneChange = this.onSeasonToCloneChange.bind(this);
  }

  onClick() {
    this.props.onAddSeasonClick(this.state.seasonName, this.state.seasonToClone);
  }
  
  onNameChange(event) {
    this.setState({
      seasonName: event.target.value
    });
  }

  onSeasonToCloneChange(event) {
    this.setState({
      seasonToClone: event.target.value
    });
  }
  
  render() {
    return (
      <Panel>
        <Form>
          <ControlLabel>New Season</ControlLabel>
          <FormGroup bsSize="small" controlId="formHorizontalName">
            <FormControl
                type="text"
                value={this.state.seasonName}
                onChange={this.onNameChange}
                placeholder="Season Name"
            />
          </FormGroup>
          <FormGroup bsSize="small" controlId="formControlsSelect">
            <ControlLabel>Season</ControlLabel>
            <FormControl
                componentClass="select"
                onChange={this.onSeasonToCloneChange}
                placeholder="select">
              <option key="0" value="0">Create New Season</option>
              {
                this.props.seasons.map((season, index) => {
                  return (
                    <option key={season.id} value={season.id}>Clone {season.name} Season</option>
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

export default AddSeason;
