import React, {Component, PropTypes} from 'react';
import {connect} from 'react-redux';
import {Button, Panel, Table} from 'react-bootstrap';
import DivisionSummaryRow from './DivisionSummaryRow';
import {createDivision} from '../actions/seasonsActions';
import AddDivision from './AddDivision';

class SeasonDivisions extends Component {
  constructor(props) {
    super(props);
    this.state = {
      addingNewDivision: false
    }
  }

  onClick(event) {
    this.setState({
      addingNewDivision: true
    });
  }

  onCloseAddDivisionClick() {
    this.setState({
      addingNewDivision: false
    });
  }

  render() {
    let bottom;
    if (this.state.addingNewDivision === true) {
      bottom = (
        <AddDivision
            onAddDivisionClick={this.props.onAddDivisionClick.bind(this)}
            onCloseClick={this.onCloseAddDivisionClick.bind(this)}
        />
      );
    } else {
      bottom = (
        <Button bsStyle="primary" bsSize="small" onClick={(e) => this.onClick(e)}>Add Division</Button>
      )
    }
    
    return (
      <div>
      <Panel>
        <Table responsive striped>
          <thead>
            <tr>
              <td>Division Name</td>
              <td># Of Teams</td>
            </tr>
          </thead>
          <tbody>
            {this.props.season && this.props.season.divisions.map((division, index) => (
               <DivisionSummaryRow key={index} division={division} />
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
    onAddDivisionClick: function(name) {
      dispatch(createDivision(name, this.props.season.id));
      this.setState({
        addingNewDivision: false
      });
    }
  }
}

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(SeasonDivisions);
