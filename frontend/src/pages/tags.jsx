import axios from "axios";
import { useEffect, useState } from "react";
import TagsCard from "../components/TagsCard";
import Navbar from "../components/Sidebar";
import Layout from "../components/Layout";
import { useNavigate } from "react-router-dom";
import TagPerformanceGraph from "../components/TagPerfomanceChart";
import api from "../api/api";


function Tags() {
    const [data, setData] = useState(null);
    const navigate = useNavigate();

    useEffect(() => {
        const fetchData = async () => {

            try{
                const token = localStorage.getItem("token");
                const response = await api.get(
                    "/users/tags",
                    {
                        headers: {
                            Authorization: `Bearer ${token}`,
                        },
                    }
                );

                setData(response.data);
            }catch(error){
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

            <div className="p-7">

        
                <div className="p-6">
                    <TagsCard tags={data} />;
                </div>
            </div>

        </Layout>
    )
}

export default Tags;