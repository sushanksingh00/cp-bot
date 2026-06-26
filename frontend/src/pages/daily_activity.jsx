import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import DailyActivityCard from "../components/DailyActivityCard";
import Layout from "../components/Layout";
import LoadingScreen from "../components/LoadingScreen";
import api from "../api/api";

function DailyActivity() {

    const [data, setData] = useState(null);
    const navigate = useNavigate();

    useEffect(() => {

        const fetchData = async () => {

            try {

                const token = localStorage.getItem("token");

                const response = await api.get(
                    "/users/daily-activity",
                    {
                        headers: {
                            Authorization: `Bearer ${token}`,
                        },
                    }
                );

                setData(response.data);

            } catch (error) {

                if (error.response?.status === 401) {
                    localStorage.removeItem("token");
                    navigate("/login");
                }

                console.error(error);

            }

        };

        fetchData();

    }, []);

    if (!data) {
        return (
            <Layout>
                <LoadingScreen text="Loading daily activity analytics..." />
            </Layout>
        );
    }

    return (
        <Layout>

            <div className="max-w-7xl mx-auto p-4 md:p-6">

                <div className="mb-8">

                    <h1 className="text-4xl font-bold">
                        Daily Activity
                    </h1>

                    <p className="text-gray-500 mt-2">
                        Track your daily problem-solving consistency, visualize
                        activity with a yearly heatmap, and monitor your success
                        rate over time.
                    </p>

                </div>

                <DailyActivityCard dailyActivity={data} />

            </div>

        </Layout>
    );
}

export default DailyActivity;