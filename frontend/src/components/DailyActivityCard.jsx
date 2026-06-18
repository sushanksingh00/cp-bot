import React from "react";

const DailyActivityCard = ({ dailyActivity = [] }) => {
    return (
        <div className='max-w-mb border shadow-lg p-6 rounded-xl bg-white'>
            <h2>Daily Activity</h2>
            {dailyActivity.map((day, index) => (
                <div key={index}>
                    <p>Date: {day.date}</p>
                    <p>Attempted: {day.problems_attempted}</p>
                    <p>Solved: {day.problems_solved}</p>
                </div>
            ))}
        </div>
    );
};

export default DailyActivityCard;