import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import TagsCard from "../components/TagsCard";
import Layout from "../components/Layout";
import LoadingScreen from "../components/LoadingScreen";
import api from "../api/api";

function Tags() {

    const [data, setData] = useState(null);
    const navigate = useNavigate();

    useEffect(() => {

        const fetchData = async () => {

            try {

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

            } catch (error) {

                if (error.response?.status === 401) {
                    localStorage.removeItem("token");
                    navigate("/login");
                }

                console.error(error);

            }

        };

        fetchData();

    }, []);

    if (!data) {
        return (
            <Layout>
                <LoadingScreen text="Loading tag analytics..." />
            </Layout>
        );
    }

    return (
        <Layout>

            <div className="max-w-7xl mx-auto p-4 md:p-6">

                <div className="mb-8">

                    <h1 className="text-4xl font-bold">
                        Tag Analytics
                    </h1>

                    <p className="text-gray-500 mt-2">
                        Analyze your performance across different problem-solving
                        topics, identify weak areas, and monitor your progress
                        over time.
                    </p>

                </div>

                <TagsCard tags={data} />

            </div>

        </Layout>
    );
}

export default Tags;