import React, { useState } from 'react';

import './style.css';


const SearchMenu = () => {


  return (
    <>
     <div className='SearchMenu'>
        <div className='titulo'>
            <p>Passagens Aéreas</p>
           
        </div>
        <div className='searchBox'>
            <div className='label1'>
                <div className='TextLabel1'>Origem</div>
                <input className='input1'></input>

            </div>
            <div className='label2'>
            <div className='TextLabel2'>Destino</div>
                <input className='input2'></input>

            </div>
            <div className='buttonSpace'>
            <button className="btn">Buscar</button>
            </div>
        </div>
        
     </div>
      
    </>
  );
};

export default SearchMenu;