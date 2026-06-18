import axios from "axios";
import { useEffect, useState } from "react";
import DailyActivityCard from "../components/DailyActivityCard";
import Navbar from "../components/Navbar";

function DailyActivity() {
    const [data, setData] = useState(null);

    useEffect(() => {
        const fetchData = async () => {
            const token = localStorage.getItem("token");
            const response = await axios.get(
                "http://localhost:8000/users/daily-activity",
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
     <DailyActivityCard dailyActivity={data} />;
     </>
    )
}

export default DailyActivity;