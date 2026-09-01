import React, { useState, useEffect } from 'react';
import api from '../api/api';

const InsightsModal = ({ isOpen, onClose, problemId }) => {
    const [insights, setInsights] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    useEffect(() => {
        if (!isOpen || !problemId) return;

        const fetchInsights = async () => {
            setLoading(true);
            setError(null);
            try {
                const token = localStorage.getItem("token");
                const response = await api.get(`/users/personalized/${problemId}/insights`, {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                });
                setInsights(response.data);
            } catch (err) {
                console.error("Failed to fetch insights", err);
                setError("Failed to load insights. Please try again later.");
            } finally {
                setLoading(false);
            }
        };

        fetchInsights();
    }, [isOpen, problemId]);

    useEffect(() => {
        const handleKeyDown = (e) => {
            if (e.key === 'Escape') {
                onClose();
            }
        };
        if (isOpen) {
            window.addEventListener('keydown', handleKeyDown);
        }
        return () => window.removeEventListener('keydown', handleKeyDown);
    }, [isOpen, onClose]);

    if (!isOpen) return null;

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black bg-opacity-50">
            <div 
                className="bg-white rounded-xl shadow-2xl w-full max-w-4xl max-h-[90vh] overflow-y-auto flex flex-col"
                onClick={(e) => e.stopPropagation()}
            >
                <div className="sticky top-0 bg-white border-b px-6 py-4 flex justify-between items-center z-10">
                    <h2 className="text-2xl font-bold text-gray-800">
                        {problemId} Insights
                    </h2>
                    <button 
                        onClick={onClose}
                        className="text-gray-500 hover:text-gray-700 text-3xl leading-none"
                    >
                        &times;
                    </button>
                </div>

                <div className="p-6">
                    {loading ? (
                        <div className="flex justify-center items-center h-64">
                            <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
                        </div>
                    ) : error ? (
                        <div className="bg-red-100 text-red-700 p-4 rounded-lg">
                            {error}
                        </div>
                    ) : !insights ? (
                        <div className="text-gray-500 text-center py-10">No data available.</div>
                    ) : (
                        <div className="space-y-8">
                            
                            {/* Problem Header */}
                            <div className="bg-blue-50 p-6 rounded-lg flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
                                <div>
                                    <h3 className="text-xl font-semibold text-blue-900">
                                        {insights.problem.name}
                                    </h3>
                                    <div className="flex flex-wrap gap-2 mt-2">
                                        {insights.problem.tags.map(tag => (
                                            <span key={tag} className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded-full">
                                                {tag}
                                            </span>
                                        ))}
                                    </div>
                                    <p className="text-sm text-gray-600 mt-2 font-medium">
                                        Rating: {insights.problem.rating || 'N/A'}
                                    </p>
                                </div>
                                <a 
                                    href={insights.problem.url}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    className="bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-6 rounded-lg transition-colors whitespace-nowrap"
                                >
                                    Open Problem
                                </a>
                            </div>

                            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                {/* Prediction & Recommendation */}
                                <div className="bg-white border rounded-lg p-5 shadow-sm">
                                    <h4 className="font-bold text-gray-700 mb-4 border-b pb-2">Prediction</h4>
                                    <div className="space-y-3">
                                        <div className="flex justify-between items-center">
                                            <span className="text-gray-600">Solve Probability</span>
                                            <span className="font-bold text-lg text-blue-600">
                                                {(insights.prediction.solve_probability * 100).toFixed(1)}%
                                            </span>
                                        </div>
                                        <div className="flex justify-between items-center">
                                            <span className="text-gray-600">Difficulty Band</span>
                                            <span className="font-semibold bg-gray-100 px-2 py-1 rounded">
                                                {insights.prediction.difficulty_band}
                                            </span>
                                        </div>
                                        <div className="mt-4 pt-4 border-t">
                                            <span className="block text-sm text-gray-500 mb-1">Recommendation Reason</span>
                                            <p className="text-gray-800">{insights.recommendation.reason}</p>
                                        </div>
                                    </div>
                                </div>

                                {/* User Performance */}
                                <div className="bg-white border rounded-lg p-5 shadow-sm">
                                    <h4 className="font-bold text-gray-700 mb-4 border-b pb-2">Your Performance</h4>
                                    <div className="space-y-2">
                                        <div className="flex justify-between">
                                            <span className="text-gray-600">Overall Solve Rate</span>
                                            <span className="font-medium">{(insights.user_performance.overall_solve_rate * 100).toFixed(1)}%</span>
                                        </div>
                                        <div className="flex justify-between">
                                            <span className="text-gray-600">Recent 7D Rate</span>
                                            <span className="font-medium">{(insights.user_performance.recent_7d_solve_rate * 100).toFixed(1)}%</span>
                                        </div>
                                        <div className="flex justify-between">
                                            <span className="text-gray-600">Recent 30D Rate</span>
                                            <span className="font-medium">{(insights.user_performance.recent_30d_solve_rate * 100).toFixed(1)}%</span>
                                        </div>
                                        <div className="flex justify-between pt-2 border-t mt-2">
                                            <span className="text-gray-600">Total Solved / Attempts</span>
                                            <span className="font-medium">{insights.user_performance.total_solved} / {insights.user_performance.total_attempts}</span>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            {/* Topic Analysis */}
                            <div className="bg-white border rounded-lg p-5 shadow-sm">
                                <h4 className="font-bold text-gray-700 mb-4 border-b pb-2">Topic Analysis</h4>
                                <div className="overflow-x-auto">
                                    <table className="w-full text-left text-sm">
                                        <thead className="bg-gray-50 text-gray-600">
                                            <tr>
                                                <th className="p-2 rounded-tl-lg">Tag</th>
                                                <th className="p-2">Attempts</th>
                                                <th className="p-2">Solved</th>
                                                <th className="p-2">Solve Rate</th>
                                                <th className="p-2 rounded-tr-lg">Status</th>
                                            </tr>
                                        </thead>
                                        <tbody className="divide-y">
                                            {insights.topic_analysis.map((topic, i) => (
                                                <tr key={i}>
                                                    <td className="p-2 font-medium text-gray-800">{topic.tag}</td>
                                                    <td className="p-2">{topic.attempts}</td>
                                                    <td className="p-2">{topic.solved}</td>
                                                    <td className="p-2">
                                                        {topic.attempts > 0 ? topic.solve_rate.toFixed(1) + '%' : 'N/A'}
                                                    </td>
                                                    <td className="p-2">
                                                        <span className={`px-2 py-1 text-xs rounded-full font-medium ${
                                                            topic.status === 'weak' ? 'bg-red-100 text-red-800' :
                                                            topic.status === 'strong' ? 'bg-green-100 text-green-800' :
                                                            topic.status === 'untested' ? 'bg-gray-100 text-gray-800' :
                                                            'bg-blue-100 text-blue-800'
                                                        }`}>
                                                            {topic.status}
                                                        </span>
                                                    </td>
                                                </tr>
                                            ))}
                                        </tbody>
                                    </table>
                                </div>
                            </div>

                            {/* Text Insights */}
                            <div className="bg-gradient-to-r from-blue-50 to-indigo-50 border border-blue-100 rounded-lg p-5 shadow-sm">
                                <h4 className="font-bold text-blue-900 mb-4">Key Insights</h4>
                                <ul className="space-y-2 list-disc list-inside text-gray-800">
                                    {insights.insights.map((insight, idx) => (
                                        <li key={idx} className="leading-relaxed">{insight}</li>
                                    ))}
                                </ul>
                            </div>

                        </div>
                    )}
                </div>
            </div>
            {/* Click outside to close */}
            <div className="fixed inset-0 z-[-1]" onClick={onClose}></div>
        </div>
    );
};

export default InsightsModal;
