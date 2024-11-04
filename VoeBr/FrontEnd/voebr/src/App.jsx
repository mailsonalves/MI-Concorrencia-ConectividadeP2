import { useState } from 'react'
import CustomNavbar from './components/Navbar/Navbar';
import './App.css'
import './output.css'
import SearchMenu from './components/SearchMenu/SearchMenu';
import { Button } from 'react-bootstrap';
import Recomendations from './components/Recomendations/Recomendations';

function App() {
  const [count, setCount] = useState(0)
  

  return (
    <>
    
    <div className='general'>
      <CustomNavbar />
      <SearchMenu></SearchMenu>  
      <Recomendations></Recomendations>
    </div>
    </>
  )
}

export default App
