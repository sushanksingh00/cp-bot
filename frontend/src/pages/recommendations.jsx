import axios from "axios";
import { useEffect, useState } from "react";

import Navbar from "../components/Navbar";
import RecommendationsCard from "../components/RecommendationsCard";

function Recommendations() {
    const [data, setData] = useState(null);

    useEffect(() => {
        const fetchData = async () => {
            const token = localStorage.getItem("token");
            const response = await axios.get(
                "http://localhost:8000/users/recommendations",
                {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                }
            );

            setData(response.data);
        };

        fetchData();
    }, []);

    if (!data) return <h1>Loading...</h1>;

    return(
        <>
        <Navbar />
         <RecommendationsCard recommendations={data} />;
        </>
    )
}

export default Recommendations;