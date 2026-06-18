import axios from "axios";
import { useEffect, useState } from "react";
import ContestsCard from "../components/ContestsCard";
import Navbar from "../components/Navbar";

function Contests() {
    const [data, setData] = useState(null);

    useEffect(() => {
        const fetchData = async () => {
            const token = localStorage.getItem("token");
            const response = await axios.get(
                "http://localhost:8000/users/contests",
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

    return (
        <>
        <Navbar />
        <ContestsCard contests={data} />;
        </>
    )
}

export default Contests;