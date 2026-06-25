import axios from "axios";
import { useEffect, useState } from "react";

import Navbar from "../components/Sidebar";
import RecommendationsPageCard from "../components/RecommendationsPageCard";
import Layout from "../components/Layout";
import { useNavigate } from "react-router-dom";
import api from "../api/api";


function Recommendations() {
    const [recommendations, setRecommendations] = useState([]);
    const [upsolves, setUpsolves] = useState([]);
    const [loading, setLoading] = useState(true);
    const navigate = useNavigate();

    useEffect(() => {
        const fetchData = async () => {
            try {
                const token = localStorage.getItem("token");

                const [recommendationsRes, upsolvesRes] = await Promise.all([
                    api.get(
                        "/users/recommendations",
                        {
                            headers: {
                                Authorization: `Bearer ${token}`,
                            },
                        }
                    ),
                    api.get(
                        "/users/upsolve",
                        {
                            headers: {
                                Authorization: `Bearer ${token}`,
                            },
                        }
                    ),
                ]);

                setRecommendations(recommendationsRes.data);
                setUpsolves(upsolvesRes.data);
            } catch (error) {
                if(error.response?.status == 401){
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

    if (loading) return <h1>Loading...</h1>;

    return (
        <Layout>
            <div className="p-7 col-span-2">

                <div className="p-6">
                    <RecommendationsPageCard
                        recommendations={recommendations}
                        upsolves={upsolves}
                    />
                </div>
            </div>
        </Layout>
    );
}

export default Recommendations;