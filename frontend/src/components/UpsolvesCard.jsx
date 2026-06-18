import React from "react";

const UpsolvesCard = ({ upsolves = [] }) => {
    return (
        < div className='max-w-mb border shadow-lg p-6 rounded-xl bg-white'>
            <h2>Upsolves</h2>
            {upsolves.map((problem, index) => (
                <div key={index}>
                    <p>Contest ID: {problem.problem_contest_id}</p>
                    <p>Index: {problem.problem_index}</p>
                </div>
            ))}
        </div>
    );
};

export default UpsolvesCard;