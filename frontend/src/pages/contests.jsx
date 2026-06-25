import axios from "axios";
import { useEffect, useState } from "react";
import ContestsCard from "../components/ContestsCard";
import ContestRatingChart from "../components/ContestRatingChart";
import Layout from "../components/Layout";
import { useNavigate } from "react-router-dom";
import api from "../api/api";



function Contests() {
    const [data, setData] = useState(null);
    const navigate = useNavigate();

    useEffect(() => {
        const fetchData = async () => {
            try{
            
                const token = localStorage.getItem("token");
                const response = await api.get(
                    "/users/contests",
                    {
                        headers: {
                            Authorization: `Bearer ${token}`,
                            },
                        }
                    );

                    setData(response.data);
                }
                catch(error){

                    if(error.response?.status == 401){
                        localStorage.removeItem("token");
                        navigate("/login");
                    }
                } 
        };

        fetchData();
    }, []);

    if (!data) return <h1>Loading...</h1>;

    return (
        <Layout>
            <div className="p-6 ">
                
                    <ContestsCard contests={data} />

            </div>
        </Layout>
    )
}

export default Contests;