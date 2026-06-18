import React from "react";

const WeakestTagsCard = ({ weakestTags = [] }) => {
    return (
        <div className='max-w-mb border shadow-lg p-6 rounded-xl bg-white'>
            <h2>Weakest Tags</h2>
            {weakestTags.map((tag, index) => (
                <div key={index}>
                    <p>{tag.tag_name || tag}</p>
                </div>
            ))}
        </div>
    );
};

export default WeakestTagsCard;