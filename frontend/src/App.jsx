import { BrowserRouter, Routes, Route } from "react-router-dom";

import Login from "./pages/login";
import Dashboard from "./pages/dashboard";
import Register from "./pages/register";
import Index from "./pages/index";
import Contests from "./pages/contests";
import DailyActivity from "./pages/daily_activity";
import Tags from "./pages/tags";
import TagsWeakest from "./pages/tag_weakest";
import Recommendations from "./pages/recommendations";
import Upsolves from "./pages/upsolves";


function App() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/login" element={<Login />} />
                <Route path="/register" element={<Register />} />

                <Route path="/" element={<Index />} />
                <Route path="/dashboard" element={<Dashboard />} />
                <Route path="/contests" element={<Contests />} />
                <Route path="/daily-activity" element={<DailyActivity />} />
                <Route path="/tags" element={<Tags />} />
                <Route path="/tags/weakest" element={<TagsWeakest />} />
                <Route path="/recommendations" element={<Recommendations />} />
                <Route path="/upsolve" element={<Upsolves />} />
            </Routes>
        </BrowserRouter>
    );
}

export default App;