import axios from "axios";
import { useEffect, useState } from "react";
import TagsCard from "../components/TagsCard";
import Navbar from "../components/Navbar";

function Tags() {
    const [data, setData] = useState(null);

    useEffect(() => {
        const fetchData = async () => {
            const token = localStorage.getItem("token");
            const response = await axios.get(
                "http://localhost:8000/users/tags",
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
        
        <TagsCard tags={data} />;
        </>
    )
}

export default Tags;