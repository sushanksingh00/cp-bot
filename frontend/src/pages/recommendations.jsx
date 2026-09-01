import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import RecommendationsPageCard from "../components/RecommendationsPageCard";
import Layout from "../components/Layout";
import LoadingScreen from "../components/LoadingScreen";
import api from "../api/api";

function Recommendations() {
    const [recommendations, setRecommendations] = useState([]);
    const [mlRecommendations, setMlRecommendations] = useState([]);
    const [activeUpsolves, setActiveUpsolves] = useState([]);
    const [completedUpsolves, setCompletedUpsolves] = useState([]);
    const [loading, setLoading] = useState(true);

    const navigate = useNavigate();

    useEffect(() => {

        const fetchData = async () => {

            try {

                const token = localStorage.getItem("token");

                const [recommendationsRes, upsolvesRes, mlRes] = await Promise.all([
                    api.get("/users/recommendations", {
                        headers: {
                            Authorization: `Bearer ${token}`,
                        },
                    }),
                    api.get("/users/upsolve", {
                        headers: {
                            Authorization: `Bearer ${token}`,
                        },
                    }),
                    api.get("/users/personalized", {
                        headers: {
                            Authorization: `Bearer ${token}`,
                        },
                    }),
                ]);

                setRecommendations(recommendationsRes.data);
                setMlRecommendations(mlRes.data);

                setActiveUpsolves(
                    upsolvesRes.data.filter(
                        (problem) => !problem.is_completed
                    )
                );

                setCompletedUpsolves(
                    upsolvesRes.data.filter(
                        (problem) => problem.is_completed
                    )
                );

            } catch (error) {

                if (error.response?.status === 401) {
                    localStorage.removeItem("token");
                    navigate("/login");
                }

                console.error(error);

            } finally {
                setLoading(false);
            }

        };

        fetchData();

    }, []);

    if (loading) {
        return (
            <Layout>
                <LoadingScreen text="Loading recommendation analytics..." />
            </Layout>
        );
    }

    return (
        <Layout>

            <div className="max-w-7xl mx-auto p-4 md:p-6">

                <div className="mb-8">

                    <h1 className="text-4xl font-bold">
                        Recommendations
                    </h1>

                    <p className="text-gray-500 mt-2">
                        Receive personalized ML recommendations, identify weak
                        topics, review suggested upsolves, and track problems
                        you've successfully solved after contests.
                    </p>

                </div>

                <RecommendationsPageCard
                    recommendations={recommendations}
                    mlRecommendations={mlRecommendations}
                    upsolves={activeUpsolves}
                    completedUpsolves={completedUpsolves}
                />

            </div>

        </Layout>
    );
}

export default Recommendations;