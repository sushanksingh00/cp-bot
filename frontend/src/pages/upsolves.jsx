import axios from "axios";
import { useEffect, useState } from "react";
import UpsolvesCard from "../components/UpsolvesCard";
import Navbar from "../components/Navbar";

function Upsolves() {
    const [data, setData] = useState(null);

    useEffect(() => {
        const fetchData = async () => {
            const token = localStorage.getItem("token");
            const response = await axios.get(
                "http://localhost:8000/users/upsolve",
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
        <Navbar/>
     <UpsolvesCard upsolves={data} />;
    </>
    )
}

export default Upsolves;