import React, { useState } from 'react';

import './style.css';


const Card = () => {


  return (
    <>
    <div className='Card'>  
    
    
    <img className='img'
            src="https://www.zapimoveis.com.br/blog/wp-content/uploads/2023/12/cidade-de-sao-paulo.jpg" 
         
            
            
          />{' '}

    <div className='content'>
    <div className='header'>
     <h2> Voo para {"São Paulo"}</h2>
     <h2> Hoje {"01/11"}</h2>
    </div>

    <div  className='origin'>
      
    </div>
    <div className='button'>
      <button className='btn'>Comprar</button>
    </div>
   
   </div>
    
    
      
    </div>
      
    </>
  );
};

export default Card;