import React, { useState } from 'react';

import './style.css';
import Card from '../Card/Card';

const Recomendations = () => {


  return (
    <>
     <div className='text'>
        <h3>Recomendações - Destinos populares</h3>
     </div>
     <div className='cards'>
        <Card></Card>
        <Card></Card>
        <Card></Card>
     </div>
      
    </>
  );
};

export default Recomendations;