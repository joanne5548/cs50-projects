import React from 'react'
import trashcan_img from '../assets/trashcan.png'

const Todolist = ({state, itemList, onChange, onClick}) => {
    let checkedList = state.checkedList;

    let todoList = itemList.map((item) => (
        <label className={checkedList[item] ? 'item-checked' : 'item'} key={item}>
            <input type="checkbox" name={item} className='checkbox' onChange={onChange}/>
            <div className='item-content'>{item}</div>
            <input type="image" src={trashcan_img} alt="trashcan" name={item} onClick={onClick} className='trashcan'/>
        </label>
    ));

  return (
    <div>
      {todoList}
    </div>
  )
}

export default Todolist
