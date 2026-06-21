import axios from "axios"
import { useEffect } from "react";
import { useState } from "react";
import UserCard from "../components/UserCard";
import RecentActivityCard from "../components/RecentActivityCard";
import DailyActivityHeatMap from "../components/DailyActivityHeatMap";
import RecommendationsCard from "../components/RecommendationsCard";
import WeakTagCard from "../components/WeakTagCard";
import StatsCard from "../components/StatsCard";
import { Link, useNavigate } from "react-router-dom";
import Layout from "../components/Layout";
import ContestStatsCard from "../components/ContestStatCard";
import TagPerformanceGraph from "../components/TagPerfomanceChart";

function Dashboard() {

    const [data, setData] = useState(null);
    const navigate = useNavigate();
    
    
    useEffect(() => {
        const fetchData = async () => {
            try {
                const token = localStorage.getItem("token");

                const response = await axios.get(
                    "http://localhost:8000/users/dashboard",
                    {
                        headers: {
                            Authorization: `Bearer ${token}`
                        }
                    }
                );


                setData(response.data);
                console.log(response.data.user.handle);
                localStorage.setItem("handle", response.data.user.handle);

            } catch (error) {
                console.log(error);

                if (error.response?.status === 401) {
                    localStorage.removeItem("token");
                    navigate("/login");
                }

                if(error.response?.status === 404){
                    navigate("/sync");
                }
            }
        };

        fetchData();
    }, []);
    if (!data) return <h1>Loading...</h1>;
    const lastActiveDate = new Date(data.recent_activity[0].date);
    const today = new Date();

    const diffTime = today - lastActiveDate;
    let diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));
    if (diffDays == 0) diffDays = "Today";
    else diffDays = `${diffDays} Days ago`;

    return (
        <Layout>
                <div className="grid grid-cols-5 gap-4 items-stretch">
                    <div className="col-span-4 mb-4">
                        <UserCard user={data.user} last_active={diffDays} />
                    </div>

                    <div className="col-span-1 mb-4">
                        <ContestStatsCard total_contests={data.total_contests} />
                    </div>
                </div>
                <div className="grid grid-cols-3 gap-4">
                    <div className="col-span-2">
                        <RecommendationsCard recommendations={data.recommendations} />
                    </div>
                    <div className="col-span-1">
                            <StatsCard total_contests={data.total_contests} 
                            total_questions = {data.total_questions} 
                            total_days_active={data.total_days_active} />
                        <DailyActivityHeatMap activity={data.recent_activity} />
                    </div>
                </div>
                <div>
                    
                </div>
        </Layout>
    );
}

export default Dashboard;