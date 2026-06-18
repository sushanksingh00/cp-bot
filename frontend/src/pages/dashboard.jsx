import axios from "axios"
import { useEffect } from "react";
import { useState } from "react";
import UserCard from "../components/UserCard";
import RecentActivityCard from "../components/RecentActivityCard";
import RecommendationsCard from "../components/RecommendationsCard";
import WeakTagCard from "../components/WeakTagCard";
import { Link } from "react-router-dom";
import Navbar from "../components/Navbar";

function Dashboard() {

    const [data, setData] = useState(null);
    
    useEffect(() => {
        const fetchData = async() => {
            const token = localStorage.getItem("token");
            const response = await axios.get(
                "http://localhost:8000/users/dashboard",
                {
                    headers : {
                        Authorization : `Bearer ${token}`
                    }
                }
            );
            
            setData(response.data);
            console.log(response.data);
        };
        fetchData();
    }, []);
    if (!data) return <h1>Loading...</h1>;
    return (
        <div>

            <Navbar />
            <div className="flex">
                <UserCard user={data.user} />
                <WeakTagCard weakest_tags={data.weakest_tags} />
                <RecommendationsCard recommendations={data.recommendations} />
                <RecentActivityCard recent_activity={data.recent_activity} />
            </div>
        </div>
    );
}

export default Dashboard;