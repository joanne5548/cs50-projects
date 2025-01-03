import React from 'react'

const DateWidget = () => {
    const d = new Date();
    const weekdays = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];

    let date = d.getDate();
    let month = d.getMonth() + 1;
    let year = d.getFullYear();
    let day = weekdays[d.getDay()];

    if (month < 10) {
        month = "0" + month;
    }

    if (date < 10) {
        date = "0" + date;
    }

    let fulldate = `${month}-${date}-${year}`
    
  return (
    <div className='date-container'>
        <div className='date'>{fulldate}</div>
        <div className='day'>{day}</div>
    </div>
  )
}

export default DateWidget
