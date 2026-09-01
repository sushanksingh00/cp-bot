import { Link, useNavigate } from "react-router-dom";
import { useState } from "react";

import SyncCard from "./SyncCard";

import dashboard from "../assets/dashboard.svg";
import activity from "../assets/activity.svg";
import contest from "../assets/contest.svg";
import recommendation from "../assets/recommendation.svg";
import aiIcon from "../assets/ai.svg";
import tags from "../assets/tags.svg";
import logoutIcon from "../assets/logout.svg";

const Sidebar = ({}) => {
    const [collapsed, setCollapsed] = useState(true);
    const navigate = useNavigate();

    const logout = () => {
        localStorage.removeItem("token");
        localStorage.removeItem("handle");
        navigate("/login");
    };

    const navClass = "flex items-center px-4 py-3 rounded-lg hover:bg-gray-200 transition";
    const linkClass = `${navClass} ${collapsed ? "justify-center" : ""}`;
    const iconClass = "w-6 h-6";

    const handle = localStorage.getItem("handle");

    return (
        <div className={`${collapsed ? "w-20" : "w-64"} min-h-screen fixed bg-white shadow-lg p-4 flex flex-col transition-all duration-300`}>

            <h1 className="text-2xl font-bold mb-6 text-center">
                {collapsed ? "CP" : "CP Analytics"}
            </h1>

            <button
                onClick={() => setCollapsed(!collapsed)}
                className="mb-6 p-2 rounded-lg hover:bg-gray-200"
            >
                {collapsed ? "→" : "←"}
            </button>

            <div className="flex flex-col gap-2">

                <Link to="/" className={linkClass}>
                    <img src={dashboard} alt="Dashboard" className={iconClass} />
                    {!collapsed && <span className="ml-3">Dashboard</span>}
                </Link>

                <Link to="/contests" className={linkClass}>
                    <img src={contest} alt="Contests" className={iconClass} />
                    {!collapsed && <span className="ml-3">Contests</span>}
                </Link>

                <Link to="/daily-activity" className={linkClass}>
                    <img src={activity} alt="Daily Activity" className={iconClass} />
                    {!collapsed && <span className="ml-3">Daily Activity</span>}
                </Link>

                <Link to="/tags" className={linkClass}>
                    <img src={tags} alt="Tags" className={iconClass} />
                    {!collapsed && <span className="ml-3">Tags</span>}
                </Link>

                <Link to="/recommendations" className={linkClass}>
                    <img src={recommendation} alt="Recommendations" className={iconClass} />
                    {!collapsed && <span className="ml-3">Recommendations</span>}
                </Link>

                <Link to="/insights" className={linkClass}>
                    <img src={aiIcon} alt="AI Problem Insights" className={iconClass} />
                    {!collapsed && <span className="ml-3 text-blue-600 font-semibold">AI Insights</span>}
                </Link>

            </div>

            <div className="mt-auto">

                {!collapsed && (
                    <div className="mb-4">
                        <SyncCard handle={handle}/>
                    </div>
                )}

                <button
                    onClick={logout}
                    className={`w-full flex items-center px-4 py-3 rounded-lg hover:bg-red-100 transition ${collapsed ? "justify-center" : ""}`}
                >
                    <img src={logoutIcon} alt="Logout" className={iconClass} />
                    {!collapsed && <span className="ml-3">Logout</span>}
                </button>

            </div>

        </div>
    );
};

export default Sidebar;