import React from 'react'

const Newitem = ({inputRef, onChange}) => {
  return (
    <label className='item'>
        <input className='checkbox' type="checkbox"/>
        <div className='item-content-new'>
            <input ref={inputRef} onKeyDown={onChange} className='new-item-textbox' type='text' />
        </div>
    </label>
  )
}

export default Newitem
