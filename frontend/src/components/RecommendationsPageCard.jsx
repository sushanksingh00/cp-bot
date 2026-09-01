import React, { useState } from "react";
import InsightsModal from "./InsightsModal";

const RecommendationsCard = ({
    recommendations = [],
    mlRecommendations = [],
    upsolves = [],
    completedUpsolves = [],
}) => {

    const [showCompleted, setShowCompleted] = useState(false);
    const [selectedProblemId, setSelectedProblemId] = useState(null);
    const [isInsightsModalOpen, setIsInsightsModalOpen] = useState(false);

    const handleViewInsights = (problemId) => {
        setSelectedProblemId(problemId);
        setIsInsightsModalOpen(true);
    };

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
    
    const getDifficultyColor = (band) => {
        switch (band) {
            case "Warm-up": return "bg-green-100 text-green-800";
            case "Recommended": return "bg-blue-100 text-blue-800";
            case "Stretch": return "bg-yellow-100 text-yellow-800";
            case "Challenging": return "bg-orange-100 text-orange-800";
            case "Advanced": return "bg-red-100 text-red-800";
            default: return "bg-gray-100 text-gray-800";
        }
    };

    return (
        <div className="shadow-lg p-6 rounded-2xl bg-red-100 space-y-6">

            {mlRecommendations.length > 0 && (
                <div>
                    <h2 className="text-2xl font-bold mb-4">
                        Personalized ML Recommendations
                    </h2>
                    
                    <div className="space-y-4">
                        {mlRecommendations.map((rec, index) => (
                            <div key={index} className="bg-white rounded-lg p-5 shadow">
                                <div className="flex justify-between items-start">
                                    <div>
                                        <h3 className="font-semibold text-xl text-blue-700 hover:underline">
                                            <a 
                                                href={`https://codeforces.com/problemset/problem/${rec.problem_id.replace(/[A-Za-z]+$/, '')}/${rec.problem_id.match(/[A-Za-z]+$/)[0]}`}
                                                target="_blank"
                                                rel="noopener noreferrer"
                                            >
                                                Problem {rec.problem_id}
                                            </a>
                                        </h3>
                                        <p className="text-sm text-gray-600 mt-1">
                                            {rec.tags.join(" · ")} {rec.rating ? `| ${rec.rating} Rating` : ''}
                                        </p>
                                    </div>
                                    <div className="flex flex-col items-end gap-2">
                                        <span className={`px-3 py-1 rounded-full text-sm font-medium ${getDifficultyColor(rec.difficulty_band)}`}>
                                            {rec.difficulty_band}
                                        </span>
                                        <span className="text-sm font-semibold text-gray-700">
                                            {(rec.solve_probability * 100).toFixed(1)}% Solve Prob
                                        </span>
                                    </div>
                                </div>
                                <div className="mt-4 pt-4 border-t flex justify-between items-end">
                                    <div>
                                        <p className="font-medium text-gray-800">Why:</p>
                                        <p className="text-gray-600 mt-1">{rec.reason}</p>
                                    </div>
                                    <button
                                        onClick={() => handleViewInsights(rec.problem_id)}
                                        className="text-sm bg-blue-50 text-blue-700 hover:bg-blue-100 font-medium px-4 py-2 rounded-lg transition-colors whitespace-nowrap ml-4"
                                    >
                                        View Insights
                                    </button>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            )}

            <div>
                <h2 className="text-2xl font-bold mb-4">
                    Analytics Insights
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
            </div>

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

            <InsightsModal 
                isOpen={isInsightsModalOpen}
                onClose={() => setIsInsightsModalOpen(false)}
                problemId={selectedProblemId}
            />
        </div>
    );
};

export default RecommendationsCard;