import { useState } from "react";
import SyncCard from "../components/SyncCard";

function Sync() {
    const [handle, setHandle] = useState("");

    return (
        <div className="min-h-[80vh] flex items-center justify-center px-6">
            <div className="w-full max-w-xl bg-blue-100 rounded-2xl shadow-lg p-8">

                <h1 className="text-3xl font-bold text-center mb-2">
                    Sync Codeforces Profile
                </h1>

                <p className="text-gray-500 text-center mb-8">
                    Enter your Codeforces handle to import your contests,
                    submissions and generate analytics.
                </p>

                <div className="space-y-4">
                    <label className="font-medium text-gray-700">
                        Codeforces Handle
                    </label>

                    <input
                        type="text"
                        placeholder="tourist"
                        value={handle}
                        onChange={(e) => {
                            setHandle(e.target.value);
                            localStorage.setItem("handle", e.target.value);
                        }}
                        className="w-full bg-white rounded-2xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />

                    <SyncCard handle={handle} />
                </div>

            </div>
        </div>
    );
}

export default Sync;