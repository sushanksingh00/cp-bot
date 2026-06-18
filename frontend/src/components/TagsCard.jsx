import React from "react";

const TagsCard = ({ tags = [] }) => {
    return (
        <div className='max-w-mb border shadow-lg p-6 rounded-xl bg-white'>
            <h2>Tags</h2>
            {tags.map((tag, index) => (
                <div key={index}>
                    <p>Tag: {tag.tag_name}</p>
                    <p>Success Rate: {tag.success_rate}</p>
                    <p>Weakness Score: {tag.weakness_score}</p>
                </div>
            ))}
        </div>
    );
};

export default TagsCard;