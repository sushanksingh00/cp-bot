import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import api from "../api/api";

function Register() {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [email, setEmail] = useState("");
    const [error, setError] = useState("");

    const navigate = useNavigate();


    const hasLength = password.length >= 8;
    const hasUpper = /[A-Z]/.test(password);
    const hasLower = /[a-z]/.test(password);
    const hasNumber = /\d/.test(password);

    const validPassword =
        hasLength &&
        hasUpper &&
        hasLower &&
        hasNumber;

    const handleRegister = async () => {
        setError("");

        try {
            const response = await api.post("/auth/register", {
                username,
                email,
                password,
            });

            localStorage.setItem(
                "token",
                response.data.token
            );

            navigate("/login");
        } catch (error) {
            setError(
                error.response?.data?.detail ||
                "Registration failed."
            );

            console.log(error);
        }
    };

    return (
        <div className="min-h-screen flex items-center justify-center bg-white px-4">
            <div className="w-full max-w-md bg-blue-100 rounded-2xl shadow-xl p-8">

                <h1 className="text-4xl font-bold text-center mb-2">
                    Register
                </h1>

                <p className="text-gray-500 text-center mb-8">
                    Create your account to start tracking your
                    competitive programming journey.
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
                        type="email"
                        placeholder="Email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        className="p-3 rounded-2xl shadow-lg bg-white outline-none focus:ring-2 focus:ring-blue-500"
                    />

                    <input
                        type="password"
                        placeholder="Password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        className="p-3 rounded-2xl shadow-lg bg-white outline-none focus:ring-2 focus:ring-blue-500"
                    />

                    {/* Password Requirements */}

                    <div className="bg-white rounded-xl p-4 text-sm shadow">

                        <p className="font-semibold mb-2 text-gray-700">
                            Password Requirements
                        </p>

                        <p className={hasLength ? "text-green-600" : "text-gray-500"}>
                            {hasLength ? "✓" : "○"} At least 8 characters
                        </p>

                        <p className={hasUpper ? "text-green-600" : "text-gray-500"}>
                            {hasUpper ? "✓" : "○"} One uppercase letter
                        </p>

                        <p className={hasLower ? "text-green-600" : "text-gray-500"}>
                            {hasLower ? "✓" : "○"} One lowercase letter
                        </p>

                        <p className={hasNumber ? "text-green-600" : "text-gray-500"}>
                            {hasNumber ? "✓" : "○"} One number
                        </p>

                    </div>

                    {error && (
                        <div className="bg-red-100 border border-red-300 rounded-lg p-3">
                            <p className="text-red-600 text-sm text-center">
                                {error}
                            </p>
                        </div>
                    )}

                    <button
                        onClick={handleRegister}
                        disabled={!validPassword}
                        className={`px-6 py-3 rounded-2xl shadow-lg font-semibold text-white transition ${
                            validPassword
                                ? "bg-blue-500 hover:bg-blue-700"
                                : "bg-gray-400 cursor-not-allowed"
                        }`}
                    >
                        Register
                    </button>

                    <p className="text-center text-gray-600">
                        Already have an account?{" "}
                        <Link
                            to="/login"
                            className="text-blue-600 font-semibold hover:underline"
                        >
                            Login
                        </Link>
                    </p>

                </div>
            </div>
        </div>
    );
}

export default Register;