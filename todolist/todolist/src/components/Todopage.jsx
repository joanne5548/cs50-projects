import React, { useRef, useState } from 'react'
import './Todopage.css'
import DateWidget from './DateWidget'
import Newitem from './Newitem'
import Todolist from './Todolist'

const Todopage = () => {
    const [state, setState] = useState({
        addingItem: false,
        itemList: ['first', 'second', 'third'],
        checkedList: {
            'first': false,
            'second': false,
            'third': false,
        },
        animate: false,
    })
    const newItemRef = useRef();

    function handleCheckBox(event) {
        let updatedCheckedList = state.checkedList;
        
        updatedCheckedList[event.target.name] = !updatedCheckedList[event.target.name]
        
        setState({
            ...state,
            checkedList: updatedCheckedList
        })
    }

    function handleAddButton() {
        setState({
            ...state,
            addingItem: !state.addingItem
        });
    }

    function addNewItem(event) {
        if (event.key === "Enter") {
            const itemContent = newItemRef.current.value;
            let updatedCheckedList = state.checkedList;

            updatedCheckedList[itemContent] = false;

            setState({
                addingItem: false,
                itemList: [...state.itemList, itemContent],
                checkedList: updatedCheckedList,
            });
            console.log(state.itemList);
        }
    }

    function deleteItem(event) {
        let checkedList = state.checkedList;

        const itemName = event.target.name;
        if (checkedList.hasOwnProperty(itemName)) {
            delete checkedList[itemName]
        }

        const newItemList = state.itemList.filter(item => item !== itemName)

        setState({
            ...state,
            animate: true
        })

        setTimeout(() => {

        }, 2000);

        // setState({
        //     ...state,
        //     checkedList: checkedList,
        //     itemList: newItemList
        // });
    }

  return (
    <div className='todopage'>
        <div className='todo-container'>
            <h1>Joanne's To-Do</h1>
            <DateWidget />

            <div className='add-button-container'>
                <button onClick={handleAddButton} className='add-button'>+</button>
            </div>

            <div className='item-list'>
                <Todolist state={state} itemList={state.itemList} onChange={handleCheckBox} onClick={deleteItem} />
                
                {state.addingItem ? <>
                    <Newitem inputRef={newItemRef} onChange={addNewItem}/>
                </> : <></>}
            </div>
        </div>
    </div>
  )
}

export default Todopage
