import { BrowserRouter, Routes, Route } from "react-router-dom";

import Login from "./pages/login";
import Dashboard from "./pages/dashboard";
import Register from "./pages/register";

import Contests from "./pages/contests";
import DailyActivity from "./pages/daily_activity";
import Tags from "./pages/tags";
import Recommendations from "./pages/recommendations";
import Sync from "./pages/sync";



function App() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/login" element={<Login />} />
                <Route path="/sync" element={<Sync />} />
                <Route path="/register" element={<Register />} />

                <Route path="/" element={<Dashboard />} />
                <Route path="/contests" element={<Contests />} />
                <Route path="/daily-activity" element={<DailyActivity />} />
                <Route path="/tags" element={<Tags />} />
                <Route path="/recommendations" element={<Recommendations />} />
            </Routes>
        </BrowserRouter>
    );
}

export default App;