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
      referenceSeason: '0',
      seasonName: '',
      seasonToClone: '0'
    };

    this.onNameChange = this.onNameChange.bind(this);
    this.onSeasonToCloneChange = this.onSeasonToCloneChange.bind(this);
  }

  onClick() {
    this.props.onAddSeasonClick(this.state.referenceSeason, this.state.seasonName, this.state.seasonToClone);
  }

  onReferenceSeasonChange(event) {
    var name = this.state.seasonName;
    if (name.length === 0 && event.target.value !== '0') {
      var fgSeason = this.props.fgSeasons.find((season) => {
        return season.id === parseInt(event.target.value, 10)
      });
      name = fgSeason.year;
    }

    this.setState({
      referenceSeason: event.target.value,
      seasonName: name
    });
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
          <Button className="close" onClick={(e) => this.props.onCloseClick(e)}>x</Button>
          <FormGroup bsSize="small" controlId="formControlsSelect">
            <ControlLabel>Reference Season</ControlLabel>
            <FormControl
                componentClass="select"
                onChange={(e) => this.onReferenceSeasonChange(e)}
                placeholder="select">
              <option key="0" value="0">Reference Season</option>
              {
                this.props.fgSeasons.map((fgSeason, index) => {
                  return (
                    <option key={fgSeason.id} value={fgSeason.id}>{fgSeason.year}</option>
                  );
                })
              }
            </FormControl>
          </FormGroup>
          
          <FormGroup bsSize="small" controlId="formHorizontalName">
            <ControlLabel>Season Name</ControlLabel>
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
