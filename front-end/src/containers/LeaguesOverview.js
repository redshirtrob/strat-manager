import React, {Component, PropTypes} from 'react';
import {connect} from 'react-redux';
import {bindActionCreators} from 'redux';
import {Button, Jumbotron} from 'react-bootstrap';

class LeaguesOverview extends Component {
  render () {
    return (
      <Jumbotron>
        <h1>Hello, Leagues!</h1>
        <p>This is a placeholder for the leagues overview</p>
        <p><Button bsStyle="primary">Learn more</Button></p>
      </Jumbotron>
    )
  }
}

function mapStateToProps(state) {
  return {
  };
}

function mapDispatchToProps(dispatch) {
  return {
  };
}

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(LeaguesOverview);
