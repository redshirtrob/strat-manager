import React, {Component, PropTypes} from 'react';
import {connect} from 'react-redux';
import {bindActionCreators} from 'redux';
import {Button, Jumbotron} from 'react-bootstrap';

class Profile extends Component {
  render () {
    return (
      <Jumbotron>
        <h1>Hello, Profile!</h1>
        <p>This is a placeholder for the user profile</p>
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
)(Profile);
