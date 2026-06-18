import React from "react";

const ContestsCard = ({ contests = [] }) => {
    return (
        <div className='max-w-mb border shadow-lg p-6 rounded-xl bg-white'>
            <h2>Contests</h2>
            {contests.map((contest, index) => (
                <div key={index}>
                    <p>Contest: {contest.contest_name}</p>
                    <p>Rank: {contest.rank}</p>
                    <p>Old Rating: {contest.old_rating}</p>
                    <p>New Rating: {contest.new_rating}</p>
                </div>
            ))}
        </div>
    );
};

export default ContestsCard;