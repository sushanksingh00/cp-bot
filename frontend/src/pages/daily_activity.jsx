import axios from "axios";
import { useEffect, useState } from "react";
import DailyActivityCard from "../components/DailyActivityCard";
import Navbar from "../components/Sidebar";
import Layout from "../components/Layout";
import { useNavigate } from "react-router-dom";
import api from "../api/api";


function DailyActivity() {
    const [data, setData] = useState(null);
    const navigate = useNavigate();

    useEffect(() => {
        const fetchData = async () => {

            try{
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
                if(error.response?.status == 401){
                    localStorage.removeItem("token");
                    navigate("/login");
                }
            }
        };

        fetchData();
    }, []);

    if (!data) return <h1>Loading...</h1>;

    return(
        <Layout>
            <div className="p-7 col-span-2">
            <div className="p-6">
                <DailyActivityCard dailyActivity={data} />
            </div>
            </div>
     
       </Layout>
    )
}

export default DailyActivity;