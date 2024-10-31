import React, { useState } from 'react';
import { Navbar, Nav, Button } from 'react-bootstrap';


import './style.css';


const CustomNavbar = () => {
 

  return (
    <>
      <Navbar className='nav'>
        <Navbar.Brand >
          <img
            src="/../public/VoeBr.png" 
            alt="Logo VoeBr"
            width="90"
            height="90" 
            
          />{' '}
   
        </Navbar.Brand>
        <Nav>
          <div className='options'>
          <button className="btn">Login</button>
          <p href ="">Cadastre-se</p>
          </div>
        </Nav>
      </Navbar>
      
    </>
  );
};

export default CustomNavbar;