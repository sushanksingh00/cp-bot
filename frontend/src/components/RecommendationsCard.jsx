import React from "react";

const RecommendationsCard = ({ recommendations }) => {
    return (
        <div className="shadow-lg p-6 rounded-2xl bg-red-100">
            <h2 className="text-xl font-bold mb-4">
                Recommendations
            </h2>

            {recommendations.map((rec, index) => (
                <div
                    key={index}
                    className="bg-white rounded-lg p-4 mb-3 shadow"
                >
                    <p>
                        <span className="font-semibold">
                            {index + 1}. {rec.title}
                        </span>
                    </p>

                    <p className="text-gray-700 mt-1 break-words">
                        {rec.message}
                    </p>
                </div>
            ))}
        </div>
    );
};

export default RecommendationsCard;