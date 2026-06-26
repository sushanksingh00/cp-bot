import React from "react";
import TagPerformanceGraph from "./TagPerfomanceChart";

const TagsCard = ({ tags = [] }) => {

    const sortedTags = [...tags].sort(
        (a, b) => b.weakness_score - a.weakness_score
    );

    return (
        <div className="bg-blue-100 rounded-2xl shadow-lg p-6">

            <h2 className="text-2xl font-bold mb-6">
                Tag Performance
            </h2>

            <div className="bg-white rounded-xl shadow p-6 mb-8">
                <TagPerformanceGraph tags={tags} />
            </div>

            <h3 className="text-xl font-semibold mb-4">
                Tag Statistics
            </h3>

            <div className="space-y-3">

                {sortedTags.map((tag, index) => (

                    <div
                        key={index}
                        className="bg-white rounded-xl shadow p-4 flex flex-col md:flex-row md:justify-between md:items-center"
                    >

                        <div>

                            <h4 className="font-bold text-lg capitalize">
                                {tag.tag_name}
                            </h4>

                            <p className="text-gray-500 text-sm">
                                Topic Performance
                            </p>

                        </div>

                        <div className="grid grid-cols-2 gap-6 mt-4 md:mt-0 text-center">

                            <div>

                                <p className="text-2xl font-bold text-green-600">
                                    {tag.success_rate.toFixed(1)}%
                                </p>

                                <p className="text-gray-500 text-sm">
                                    Success Rate
                                </p>

                            </div>

                            <div>

                                <p
                                    className={`text-2xl font-bold ${
                                        tag.weakness_score > 150
                                            ? "text-red-500"
                                            : tag.weakness_score > 75
                                            ? "text-yellow-500"
                                            : "text-green-500"
                                    }`}
                                >
                                    {tag.weakness_score.toFixed(0)}
                                </p>

                                <p className="text-gray-500 text-sm">
                                    Weakness Score
                                </p>

                            </div>

                        </div>

                    </div>

                ))}

            </div>

        </div>
    );
};

export default TagsCard;