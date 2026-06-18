import React from "react";

const WeakTagCard = (({weakest_tags}) => {
    return (
        <div className='max-w-mb border shadow-lg p-6 rounded-xl bg-white'>
            <h2>Weakest Tags</h2>
            {weakest_tags.map((tag, index) => (
                <div key={index}>
                    <p>{tag.tag_name}</p>
                    <p>Success Rate: {tag.success_rate}%</p>
                    <p>Weakness Score: {tag.weakness_score}</p>
                </div>
            ))}
        </div>
    )
})

export default WeakTagCard;