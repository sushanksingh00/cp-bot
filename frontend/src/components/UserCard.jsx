import React from 'react'

const UserCard = ({user}) => {
    return(
        <div className='max-w-mb border shadow-lg p-6 rounded-xl bg-white'>
           <h1>{user.handle}</h1>

            <h2>User Info</h2>
            <p>Platform: {user.platform}</p>
            <p>Current Rating: {user.curr_rating}</p>
            <p>Max Rating: {user.max_rating}</p>
            <p>Rank: {user.rank}</p>
        </div>
    )
}

export default UserCard