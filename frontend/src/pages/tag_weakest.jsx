import axios from "axios";
import { useEffect, useState } from "react";
import WeakestTagsCard from "../components/WeakestTagsCard";
import Navbar from "../components/Navbar";

function TagsWeakest() {
    const [data, setData] = useState(null);

    useEffect(() => {
        const fetchData = async () => {
            const token = localStorage.getItem("token");
            const response = await axios.get(
                "http://localhost:8000/users/tags/weakest",
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
         <WeakestTagsCard weakestTags={data} />
         </>
    )
}

export default TagsWeakest;