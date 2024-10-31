import { useState } from 'react'
import CustomNavbar from './components/Navbar/Navbar';
import './App.css'
import SearchMenu from './components/SearchMenu/SearchMenu';
import { Button } from 'react-bootstrap';

function App() {
  const [count, setCount] = useState(0)
  

  return (
    <>
    <div className='general'>
      <CustomNavbar />
      <SearchMenu></SearchMenu>  
    </div>
    </>
  )
}

export default App
