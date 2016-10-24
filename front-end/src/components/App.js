import React, {PropTypes, Component} from 'react';
import {Grid, Nav, Navbar, NavDropdown, NavItem, MenuItem} from 'react-bootstrap';
import {LinkContainer} from 'react-router-bootstrap';
import {Link} from 'react-router';


export default class App extends Component {

  static propTypes = {
    children: PropTypes.element.isRequired,
  }

  render() {
    return (
      <main>
        <Navbar>
          <Navbar.Header>
            <Navbar.Brand>
              <Link to="#">BLB</Link>
            </Navbar.Brand>
          </Navbar.Header>
          <Nav>
            <LinkContainer to={{pathname: '#teams'}}>
              <NavItem eventKey={1} href="#teams">Teams</NavItem>
            </LinkContainer>
            <LinkContainer to={{pathname: '#leagues'}}>
              <NavItem eventKey={2} href="#leagues">Leagues</NavItem>
            </LinkContainer>
            <NavItem eventKey={3} href="#">Standings</NavItem>
          </Nav>
        </Navbar>
        <Grid>
          {this.props.children}
        </Grid>
      </main>
    );
  }
}
