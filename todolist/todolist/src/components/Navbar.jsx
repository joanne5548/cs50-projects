import React from 'react'
import './Navbar.css'

const Navbar = () => {
  return (
    <div className='navbar'>
        <div className='functionalities'>
            <a>Today</a>
            <a>Past</a>
            <a>Settings</a>
        </div>
      <div className='login'><a>Login</a></div>
    </div>
  )
}

export default Navbar
