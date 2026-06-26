import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import api from "../api/api";

function Login() {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);

    const navigate = useNavigate();

    const handleLogin = async () => {
        setError("");
        setLoading(true);

        try {
            const response = await api.post("/auth/login", {
                username,
                password,
            });

            localStorage.setItem("token", response.data.token);

            navigate("/");
        } catch (error) {
            setError(
                error.response?.data?.detail ||
                "Invalid username or password."
            );
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen flex items-center justify-center bg-gray-100 px-4">
            <div className="w-full max-w-md bg-blue-100 rounded-2xl shadow-xl p-8">

                <h1 className="text-4xl font-bold text-center mb-2">
                    Welcome Back
                </h1>

                <p className="text-center text-gray-500 mb-8">
                    Sign in to continue tracking your competitive programming journey.
                </p>

                <div className="flex flex-col gap-4">

                    <input
                        type="text"
                        placeholder="Username"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        className="p-3 rounded-2xl shadow-lg bg-white outline-none focus:ring-2 focus:ring-blue-500"
                    />

                    <input
                        type="password"
                        placeholder="Password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        className="p-3 rounded-2xl shadow-lg bg-white outline-none focus:ring-2 focus:ring-blue-500"
                    />

                    {error && (
                        <div className="bg-red-100 border border-red-300 rounded-lg p-3">
                            <p className="text-red-600 text-sm text-center">
                                {error}
                            </p>
                        </div>
                    )}

                    <button
                        onClick={handleLogin}
                        disabled={loading || !username || !password}
                        className={`py-3 rounded-2xl font-semibold text-white shadow-lg transition ${
                            loading || !username || !password
                                ? "bg-gray-400 cursor-not-allowed"
                                : "bg-blue-500 hover:bg-blue-700"
                        }`}
                    >
                        {loading ? "Signing In..." : "Login"}
                    </button>

                    <p className="text-center text-gray-600">
                        Don't have an account?{" "}
                        <Link
                            to="/register"
                            className="text-blue-600 font-semibold hover:underline"
                        >
                            Register
                        </Link>
                    </p>

                </div>
            </div>
        </div>
    );
}

export default Login;