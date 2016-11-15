import React, {Component, PropTypes} from 'react';
import {
  Button,
  ControlLabel,
  Form,
  FormControl,
  FormGroup,
  Panel
} from 'react-bootstrap';

class AddDivision extends Component {
  constructor(props) {
    super(props);
    
    this.state = {
      divisionName: ''
    };

    this.onNameChange = this.onNameChange.bind(this);
  }

  onClick() {
    this.props.onAddDivisionClick(this.state.divisionName);
  }

  onNameChange(event) {
    this.setState({
      divisionName: event.target.value
    });
  }

  render() {
    return (
      <Panel>
        <Form>
          <ControlLabel>New Division</ControlLabel>
          <Button className="close" onClick={(e) => this.props.onCloseClick(e)}>x</Button>
          <FormGroup bsSize="small" controlId="formHorizontalName">
            <FormControl
                type="text"
                value={this.state.divisionName}
                onChange={this.onNameChange}
                placeholder="Division Name"
            />
          </FormGroup>
          <Button onClick={this.onClick.bind(this)}>Add</Button>
        </Form>
      </Panel>
    );
  }
}

export default AddDivision;
