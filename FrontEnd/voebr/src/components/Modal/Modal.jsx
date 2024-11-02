import React from 'react'
import './style.css';



export default function Modal({ isOpen, setModalOpen, children }) {
  if (isOpen) {
    return (
      <div className='background'>
        <div className='estiloModal'>
          
          <div >{children} </div>
          
          <button onClick={setModalOpen}>x</button>
         
        </div>
       

      </div>
    )
  }

  return null
}




  // position: 'fixed',
  // top: 0,
  // left: 0,
  // right: 0,
  // bottom: 0,
  // backgroundColor: 'rgba(0, 0, 0, .7)',
  // zIndex: 1000