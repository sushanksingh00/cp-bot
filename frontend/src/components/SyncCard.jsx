import { useState, useEffect } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

function SyncCard({handle}) {

    // const [handle, setHandle] = useState("");
    const [taskId, setTaskId] = useState(null);
    const [status, setStatus] = useState("");
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const startSync = async () => {

        try {

            const token = localStorage.getItem("token");

            setLoading(true);

            const response = await axios.post(
                "http://localhost:8000/sync/codeforces",
                {
                    handle: handle,
                    platform: "codeforces"
                },
                {
                    headers: {
                        Authorization: `Bearer ${token}`
                    }
                }
            );

            setTaskId(response.data.task_id);
            setStatus(response.data.status);

        } catch (error) {

            console.log(error);
            setLoading(false);

        }
    };

    useEffect(() => {

        if (!taskId) return;

        const interval = setInterval(async () => {

            try {

                const response = await axios.get(
                    `http://localhost:8000/sync/status/${taskId}`
                );

                setStatus(response.data.state);

                if (
                    response.data.state === "SUCCESS" ||
                    response.data.state === "FAILURE"
                ) {
                    clearInterval(interval);
                    setLoading(false);
                }

                if (response.data.state === "SUCCESS") {
                    navigate("/");
                }


            } catch (error) {

                console.log(error);
                clearInterval(interval);
                setLoading(false);

            }

        }, 2000); //every 2 seconds

        return () => clearInterval(interval);

    }, [taskId]);

    return (
        <div className="mt-6 border-t pt-4">
            <h3 className="font-semibold mb-2">
                Data Sync
            </h3>


            <button
                onClick={startSync}
                disabled={loading}
                className="w-full px-4 py-2 rounded-lg bg-blue-500 text-white"
            >
                {loading ? "Syncing..." : "Sync Codeforces"}
            </button>

            {status && (
                <p className="text-sm text-gray-600 mt-2">
                    Status: {status}
                </p>
            )}
        </div>
    );
}

export default SyncCard;