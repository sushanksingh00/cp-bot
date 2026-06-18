import axios from "axios"
import { useEffect } from "react";
import { useState } from "react";

import { Link } from "react-router-dom";
import IndexCard from "../components/IndexCard";
import SyncCard from "../components/SyncCard";
import Navbar from "../components/Navbar";

function Index() {

    const [data, setData] = useState(null);
    
    useEffect(() => {
        const fetchData = async() => {
            const token = localStorage.getItem("token");
            const response = await axios.get(
                "http://localhost:8000/users/",
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

            <div className="flex justify-around py-10">
                <SyncCard />

                <IndexCard data={data} />
            </div>
        </div>
    );
}

export default Index;