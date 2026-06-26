import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import UserCard from "../components/UserCard";
import RecommendationsCard from "../components/RecommendationsCard";
import DailyActivityHeatMap from "../components/DailyActivityHeatMap";
import StatsCard from "../components/StatsCard";
import ContestStatsCard from "../components/ContestStatCard";
import Layout from "../components/Layout";
import LoadingScreen from "../components/LoadingScreen";
import api from "../api/api";

function Dashboard() {

    const [data, setData] = useState(null);
    const navigate = useNavigate();

    useEffect(() => {

        const fetchData = async () => {

            try {

                const token = localStorage.getItem("token");

                const response = await api.get(
                    "/users/dashboard",
                    {
                        headers: {
                            Authorization: `Bearer ${token}`,
                        },
                    }
                );

                setData(response.data);
                localStorage.setItem(
                    "handle",
                    response.data.user.handle
                );

            } catch (error) {

                console.log(error);

                if (error.response?.status === 401) {
                    localStorage.removeItem("token");
                    navigate("/login");
                }

                if (error.response?.status === 404) {
                    navigate("/sync");
                }

            }

        };

        fetchData();

    }, []);

    if (!data) {
        return (
            <Layout>
                <LoadingScreen text="Loading dashboard..." />
            </Layout>
        );
    }

    const lastActiveDate = new Date(data.recent_activity[0].date);
    const today = new Date();

    const diffTime = today - lastActiveDate;

    let diffDays = Math.floor(
        diffTime / (1000 * 60 * 60 * 24)
    );

    diffDays =
        diffDays === 0
            ? "Today"
            : `${diffDays} Days Ago`;

    return (

        <Layout>

            <div className="max-w-7xl mx-auto p-4 md:p-6">


                <div className="mb-8">

                    <h1 className="text-4xl font-bold">
                        Dashboard
                    </h1>

                    <p className="text-gray-500 mt-2">
                        Overview of your competitive programming journey,
                        recent activity, and personalized insights.
                    </p>

                </div>



                <div className="grid grid-cols-1 xl:grid-cols-5 gap-6">

                    <div className="xl:col-span-4">

                        <UserCard
                            user={data.user}
                            last_active={diffDays}
                        />

                    </div>

                    <div className="xl:col-span-1">

                        <ContestStatsCard
                            total_contests={data.total_contests}
                        />

                    </div>

                </div>



                <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mt-6">

                    <div className="lg:col-span-2">

                        <RecommendationsCard
                            recommendations={data.recommendations}
                        />

                    </div>

                    <div className="space-y-6">

                        <StatsCard
                            total_contests={data.total_contests}
                            total_questions={data.total_questions}
                            total_days_active={data.total_days_active}
                        />

                        <DailyActivityHeatMap
                            activity={data.recent_activity}
                        />

                    </div>

                </div>

            </div>

        </Layout>

    );
}

export default Dashboard;