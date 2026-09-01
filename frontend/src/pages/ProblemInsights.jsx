import React, { useState } from 'react';
import Layout from '../components/Layout';
import api from '../api/api';

const ProblemInsights = () => {
    const [problemId, setProblemId] = useState('');
    const [insights, setInsights] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const handleSearch = async () => {
        if (!problemId.trim()) return;

        setLoading(true);
        setError(null);
        setInsights(null);

        try {
            const token = localStorage.getItem("token");
            const response = await api.get(`/users/personalized/${problemId.trim()}/insights`, {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            });
            setInsights(response.data);
        } catch (err) {
            console.error("Failed to fetch insights", err);
            if (err.response && err.response.status === 404) {
                setError("Problem not found. Please check the problem ID.");
            } else if (err.response && err.response.status === 400) {
                setError("Invalid problem ID format. (e.g. 1537C)");
            } else if (err.response && err.response.status === 401) {
                setError("Authentication failed. Please log in again.");
            } else {
                setError("An error occurred while fetching insights. Please try again.");
            }
        } finally {
            setLoading(false);
        }
    };

    const handleKeyDown = (e) => {
        if (e.key === 'Enter') {
            handleSearch();
        }
    };

    const getStatusColor = (status) => {
        switch (status) {
            case 'weak': return 'bg-pink-100 text-pink-800';
            case 'strong': return 'bg-green-100 text-green-800';
            case 'untested': return 'bg-gray-100 text-gray-800';
            default: return 'bg-blue-100 text-blue-800';
        }
    };

    return (
        <Layout>
            <div className="max-w-7xl mx-auto p-4 md:p-6">
                
                <div className="mb-8">
                    <h1 className="text-4xl font-bold">
                        AI Problem Insights
                    </h1>
                    <p className="text-gray-500 mt-2">
                        Enter a problem number to get personalized insights based on your solving history.
                    </p>
                </div>

                <div className="space-y-6">
                    
                    {/* Search Card */}
                    <div className="bg-blue-100 rounded-2xl p-6 shadow-sm">
                        <div className="flex flex-col sm:flex-row gap-4">
                            <input
                                type="text"
                                value={problemId}
                                onChange={(e) => setProblemId(e.target.value)}
                                onKeyDown={handleKeyDown}
                                placeholder="Enter problem number (e.g. 1537C, B1)"
                                className="flex-1 bg-white rounded-xl px-4 py-3 text-lg focus:outline-none focus:ring-2 focus:ring-blue-400"
                            />
                            <button
                                onClick={handleSearch}
                                disabled={loading || !problemId.trim()}
                                className={`px-8 py-3 rounded-xl text-white font-semibold transition-colors whitespace-nowrap ${
                                    loading || !problemId.trim() ? 'bg-blue-300 cursor-not-allowed' : 'bg-blue-600 hover:bg-blue-700'
                                }`}
                            >
                                {loading ? 'Analyzing...' : 'Analyze'}
                            </button>
                        </div>
                    </div>

                    {error && (
                        <div className="bg-red-50 text-red-700 border border-red-200 p-4 rounded-2xl shadow-sm">
                            {error}
                        </div>
                    )}

                    {loading && !error && (
                        <div className="flex justify-center items-center py-20">
                            <div className="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-blue-600"></div>
                        </div>
                    )}

                    {insights && !loading && (
                        <div className="space-y-6">
                            
                            {/* Problem Overview */}
                            <div className="bg-blue-100 rounded-2xl p-6 shadow-sm flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
                                <div>
                                    <h3 className="text-3xl font-bold text-gray-900">
                                        {insights.problem.name}
                                    </h3>
                                    <div className="text-xl text-gray-700 font-medium mt-1">
                                        {insights.problem.problem_id}
                                    </div>
                                    <p className="text-md text-gray-600 mt-3 font-semibold">
                                        Rating: {insights.problem.rating || 'N/A'}
                                    </p>
                                    <div className="flex flex-wrap gap-2 mt-4">
                                        {insights.problem.tags.map(tag => (
                                            <span key={tag} className="px-3 py-1 bg-white text-gray-700 text-sm font-medium rounded-full shadow-sm">
                                                {tag}
                                            </span>
                                        ))}
                                    </div>
                                </div>
                                <a 
                                    href={insights.problem.url}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    className="bg-blue-600 hover:bg-blue-700 text-white font-medium py-3 px-8 rounded-xl transition-colors whitespace-nowrap shadow-sm mt-4 md:mt-0"
                                >
                                    Open Problem
                                </a>
                            </div>

                            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                {/* Prediction */}
                                <div className="bg-blue-100 rounded-2xl p-6 shadow-sm flex flex-col justify-center">
                                    <h4 className="font-bold text-gray-900 text-xl mb-6">
                                        Prediction
                                    </h4>
                                    <div className="space-y-4">
                                        <div className="bg-white rounded-xl p-4 flex justify-between items-center shadow-sm">
                                            <span className="text-gray-600 font-medium">Solve Probability</span>
                                            <span className="font-bold text-2xl text-blue-600">
                                                {(insights.prediction.solve_probability * 100).toFixed(1)}%
                                            </span>
                                        </div>
                                        <div className="bg-white rounded-xl p-4 flex justify-between items-center shadow-sm">
                                            <span className="text-gray-600 font-medium">Difficulty Band</span>
                                            <span className="font-bold text-lg text-gray-900">
                                                {insights.prediction.difficulty_band}
                                            </span>
                                        </div>
                                    </div>
                                </div>

                                {/* User Performance */}
                                <div className="bg-blue-100 rounded-2xl p-6 shadow-sm flex flex-col justify-center">
                                    <h4 className="font-bold text-gray-900 text-xl mb-6">
                                        Your Performance
                                    </h4>
                                    <div className="bg-white rounded-xl p-5 shadow-sm space-y-4">
                                        <div className="flex justify-between items-center text-gray-600">
                                            <span className="font-medium">Overall Solve Rate</span>
                                            <span className="font-bold text-lg text-gray-900">{(insights.user_performance.overall_solve_rate * 100).toFixed(1)}%</span>
                                        </div>
                                        <div className="flex justify-between items-center text-gray-600">
                                            <span className="font-medium">Recent 7D Rate</span>
                                            <span className="font-bold text-lg text-gray-900">{(insights.user_performance.recent_7d_solve_rate * 100).toFixed(1)}%</span>
                                        </div>
                                        <div className="flex justify-between items-center text-gray-600">
                                            <span className="font-medium">Recent 30D Rate</span>
                                            <span className="font-bold text-lg text-gray-900">{(insights.user_performance.recent_30d_solve_rate * 100).toFixed(1)}%</span>
                                        </div>
                                        <div className="flex justify-between items-center text-gray-600 pt-3 border-t">
                                            <span className="font-medium">Total Solved / Attempts</span>
                                            <span className="font-bold text-lg text-gray-900">{insights.user_performance.total_solved} / {insights.user_performance.total_attempts}</span>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            {/* Why this problem & Model Signals */}
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                {/* Why This Problem (PINK) */}
                                <div className="bg-pink-100 rounded-2xl p-6 shadow-sm flex flex-col">
                                    <h4 className="font-bold text-gray-900 text-xl mb-4">
                                        Why This Problem?
                                    </h4>
                                    <div className="bg-white rounded-xl p-5 text-gray-800 leading-relaxed shadow-sm font-medium flex-1">
                                        {insights.recommendation.reason}
                                    </div>
                                </div>
                                
                                {/* Model Signals (BLUE) */}
                                <div className="bg-blue-100 rounded-2xl p-6 shadow-sm flex flex-col">
                                    <h4 className="font-bold text-gray-900 text-xl mb-4">
                                        Model Signals
                                    </h4>
                                    <div className="bg-white rounded-xl p-5 shadow-sm space-y-4 flex-1">
                                        <div className="flex justify-between items-center text-gray-600">
                                            <span className="font-medium">Relative Difficulty</span>
                                            <span className="font-bold text-gray-900">{insights.model_signals.difficulty_relative_to_user > 0 ? "+" : ""}{insights.model_signals.difficulty_relative_to_user}</span>
                                        </div>
                                        <div className="flex justify-between items-center text-gray-600">
                                            <span className="font-medium">Topic Familiarity</span>
                                            <span className="font-bold text-gray-900">{insights.model_signals.topic_familiarity.toFixed(2)}</span>
                                        </div>
                                        <div className="flex justify-between items-center text-gray-600">
                                            <span className="font-medium">Avg Topic Success</span>
                                            <span className="font-bold text-gray-900">{(insights.model_signals.topic_performance * 100).toFixed(1)}%</span>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            {/* Topic Analysis Table (WHITE) */}
                            <div className="bg-white rounded-2xl p-6 shadow-sm">
                                <h4 className="font-bold text-gray-900 text-xl mb-6">
                                    Topic Analysis
                                </h4>
                                <div className="overflow-x-auto">
                                    <table className="w-full text-left text-sm border-collapse">
                                        <thead className="bg-gray-50 text-gray-500 rounded-t-xl border-b">
                                            <tr>
                                                <th className="p-4 font-semibold">Tag</th>
                                                <th className="p-4 font-semibold">Attempts</th>
                                                <th className="p-4 font-semibold">Solved</th>
                                                <th className="p-4 font-semibold">Solve Rate</th>
                                                <th className="p-4 font-semibold">Status</th>
                                            </tr>
                                        </thead>
                                        <tbody className="divide-y divide-gray-100">
                                            {insights.topic_analysis.map((topic, i) => (
                                                <tr key={i} className="hover:bg-gray-50 transition-colors">
                                                    <td className="p-4 font-semibold text-gray-900">{topic.tag}</td>
                                                    <td className="p-4 text-gray-600 font-medium">{topic.attempts}</td>
                                                    <td className="p-4 text-gray-600 font-medium">{topic.solved}</td>
                                                    <td className="p-4 text-gray-600 font-medium">
                                                        {topic.attempts > 0 ? (topic.solve_rate * 100).toFixed(1) + '%' : 'N/A'}
                                                    </td>
                                                    <td className="p-4">
                                                        <span className={`px-3 py-1 rounded-full font-semibold text-xs uppercase tracking-wider ${getStatusColor(topic.status)}`}>
                                                            {topic.status}
                                                        </span>
                                                    </td>
                                                </tr>
                                            ))}
                                        </tbody>
                                    </table>
                                </div>
                            </div>

                            {/* AI Text Insights (PINK) */}
                            <div className="bg-pink-100 rounded-2xl p-6 shadow-sm">
                                <h4 className="font-bold text-gray-900 text-xl mb-6">
                                    AI Insights
                                </h4>
                                <div className="grid grid-cols-1 gap-4">
                                    {insights.insights.map((insight, idx) => (
                                        <div key={idx} className="bg-white rounded-xl p-5 shadow-sm text-gray-800 leading-relaxed font-medium">
                                            {insight}
                                        </div>
                                    ))}
                                </div>
                            </div>

                        </div>
                    )}
                </div>
            </div>
        </Layout>
    );
};

export default ProblemInsights;
