import React, { useState } from "react";

const RecommendationsCard = ({
    recommendations = [],
    upsolves = [],
    completedUpsolves = [],
}) => {

    const [showCompleted, setShowCompleted] = useState(false);

    const getTitle = (type) => {
        switch (type) {
            case "weak_tag_improvement":
                return "Improve Weak Topics";

            case "rating_push":
                return "Push Your Rating";

            case "consistency_boost":
                return "Stay Consistent";

            default:
                return type.replaceAll("_", " ");
        }
    };

    return (
        <div className="shadow-lg p-6 rounded-2xl bg-red-100">

            <h2 className="text-2xl font-bold mb-4">
                Recommendations
            </h2>


            {recommendations.map((rec, index) => (
                <div
                    key={index}
                    className="bg-white rounded-lg p-4 mb-3 shadow"
                >
                    <h3 className="font-semibold text-lg">
                        {index + 1}. {getTitle(rec.recommendation_type)}
                    </h3>

                    <p className="text-gray-700 mt-2 whitespace-pre-line">
                        {rec.reason}
                    </p>
                </div>
            ))}



            {upsolves.length > 0 && (
                <div className="mt-6">

                    <h3 className="text-lg font-semibold mb-3">
                        Suggested Upsolves
                    </h3>

                    <div className="bg-white rounded-lg p-4 shadow">

                        {upsolves.map((problem, index) => (
                            <div
                                key={index}
                                className="py-2 border-b last:border-b-0"
                            >
                                <span className="font-semibold">
                                    Problem:
                                </span>{" "}

                                <a
                                    href={`https://codeforces.com/problemset/problem/${problem.problem_contest_id}/${problem.problem_index}`}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    className="text-blue-600 hover:underline"
                                >
                                    {problem.problem_contest_id}
                                    {problem.problem_index}
                                </a>

                            </div>
                        ))}

                    </div>

                </div>
            )}



            {completedUpsolves.length > 0 && (

                <div className="mt-6">

                    <button
                        onClick={() => setShowCompleted(!showCompleted)}
                        className="w-full flex justify-between items-center bg-white rounded-lg p-4 shadow hover:bg-gray-50"
                    >

                        <span className="font-semibold">
                            Solved After Contest ({completedUpsolves.length})
                        </span>

                        <span>
                            {showCompleted ? "▼" : "▶"}
                        </span>

                    </button>

                    {showCompleted && (

                        <div className="bg-white rounded-lg mt-2 p-4 shadow">

                            {completedUpsolves.map((problem, index) => (

                                <div
                                    key={index}
                                    className="py-2 border-b last:border-b-0"
                                >

                                    <div className="flex items-center gap-2">

                                        <span className="text-green-600">
                                            ✓ Problem:
                                        </span>

                                        <a
                                            href={`https://codeforces.com/problemset/problem/${problem.problem_contest_id}/${problem.problem_index}`}
                                            target="_blank"
                                            rel="noopener noreferrer"
                                            className="text-blue-600 hover:underline"
                                        >
                                            {problem.problem_contest_id}
                                            {problem.problem_index}
                                        </a>

                                    </div>

                                    <p className="text-sm text-gray-500 ml-6">
                                        Solved after the contest.
                                    </p>

                                </div>

                            ))}

                        </div>

                    )}

                </div>

            )}

        </div>
    );
};

export default RecommendationsCard;