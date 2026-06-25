import { useState } from "react";
import SyncCard from "../components/SyncCard";
import api from "../api/api";


function Sync() {
    const [handle, setHandle] = useState("");



    return (
        <div className="p-6">
            <input
                type="text"
                placeholder="Enter Codeforces Handle"
                value={handle}
                onChange={(e) => {
                    setHandle(e.target.value);
                    localStorage.setItem("handle", e.target.value);
                    }
                }
                className="border p-2 rounded mr-2"
            />

            <SyncCard handle={handle} />
        </div>
    );
}

export default Sync;