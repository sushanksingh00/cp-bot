import { useState, useEffect } from "react";
import axios from "axios";

function SyncCard() {

    const [handle, setHandle] = useState("");
    const [taskId, setTaskId] = useState(null);
    const [status, setStatus] = useState("");
    const [loading, setLoading] = useState(false);

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

            } catch (error) {

                console.log(error);
                clearInterval(interval);
                setLoading(false);

            }

        }, 2000); //every 2 seconds

        return () => clearInterval(interval);

    }, [taskId]);

    return (
        <div className="min-w-1/3 max-w-md p-6 rounded-xl shadow-lg bg-white border">

            <h2 className="font-bold text-2xl mb-2">Sync Codeforces</h2>

            <input
                type="text"
                placeholder="Codeforces Handle"
                value={handle}
                onChange={(e) => setHandle(e.target.value)}
                className="border p-2 rounded mb-2"
            />

            <button
                onClick={startSync}
                disabled={loading}
                className="px-4 py-2 rounded bg-blue-500 border mb-2"
            >
                {loading ? "Syncing..." : "Sync"}
            </button>

            <p><span className="font-semibold">Status: </span>{status}</p>

        </div>
    );
}

export default SyncCard;