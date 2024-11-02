import React, { useState } from 'react';
import { Navbar, Nav, Button } from 'react-bootstrap';
import Modal from '../Modal/Modal';

import './style.css';


const CustomNavbar = () => {
const [openModal, setOpenModal] = useState(false)

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
          <button className="btn" onClick={() => setOpenModal(true)}>Login</button>
          <p href ="">Cadastre-se</p>
          </div>
        </Nav>
        <Modal isOpen={openModal} setModalOpen={() => setOpenModal(!openModal)}>
        <div className='conteudoModal'>

        </div>
      </Modal>
      </Navbar>
      
    </>
  );
};

export default CustomNavbar;