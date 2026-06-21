import React from "react";
import TagPerformanceGraph from "./TagPerfomanceChart";

const TagsCard = ({ tags = [] }) => {
    return (
        <div className="shadow-lg p-6 rounded-xl bg-blue-100">
            <h2 className="text-xl font-bold mb-4">
                Tags
            </h2>
            <TagPerformanceGraph tags={tags} />

            {tags.map((tag, index) => (
                <div
                    key={index}
                    className=" rounded-lg p-4 mb-3 bg-white"
                >
                    <p>
                        <span className="font-semibold">Tag:</span>{" "}
                        {tag.tag_name}
                    </p>

                    <p>
                        <span className="font-semibold">Success Rate:</span>{" "}
                        {tag.success_rate.toFixed(1)}%
                    </p>

                    <p>
                        <span className="font-semibold">Weakness Score:</span>{" "}
                        {tag.weakness_score.toFixed(2)}
                    </p>
                </div>
            ))}
        </div>
    );
};

export default TagsCard;