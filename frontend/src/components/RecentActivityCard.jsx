import React from 'react';

const RecentActivityCard = (({recent_activity}) => {
    return(
        <div className='max-w-mb border shadow-lg p-6 rounded-xl bg-white'>
            <h2>Recent Activity</h2>
            {recent_activity.map((activity, index) => (
                <div key={index}>
                    <p>Date: {activity.date}</p>
                    <p>Attempted: {activity.problems_attempted}</p>
                    <p>Solved: {activity.problems_solved}</p>
                    <p>Average Rating: {activity.average_rating}</p>
                </div>
            ))}
        </div>
    )
})
export default RecentActivityCard;