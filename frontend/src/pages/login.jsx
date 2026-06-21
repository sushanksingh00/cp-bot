import { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { Link } from "react-router-dom";

function Login() {

    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const navigate = useNavigate();

    const handleLogin = async () => {

        try {

            const response = await axios.post(
                "http://localhost:8000/auth/login",
                {
                    username,
                    password
                }
            );

            localStorage.setItem(
                "token",
                response.data.token
            );
            console.log(localStorage.getItem("token"));

            navigate("/");


            console.log("saved");

        } catch (error) {
            console.log(error);
        }
    };

    return (
        <div className="min-h-screen flex flex-col items-center justify-center bg-gray-100">
            {/* <h1 className="text-4xl font-bold mb-10">CP Analytics</h1> */}
            <div className="w-full max-w-md bg-blue-100 rounded-2xl shadow-xl p-8">
                <h1 className="text-4xl font-bold text-center mb-2 ">
                    Welcome back
                </h1>
                <h1 className="mb-15 text-gray-500 text-center">Enter your username and password to access your account</h1>

                <div className="flex flex-col gap-4">
                    <input
                        type="text"
                        placeholder="Username"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        className="p-3 rounded-2xl shadow-lg bg-white"
                    />

                    <input
                        type="password"
                        placeholder="Password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        className="p-3 rounded-2xl shadow-lg bg-white"
                    />

                    <button
                        onClick={handleLogin}
                        className="bg-blue-500 text-white py-3 rounded-2xl font-semibold shadow-lg hover:bg-blue-700 "
                    >
                        Login
                    </button>
                    <Link to="/register">Register?</Link>
                </div>
            </div>
        </div>
    );
}

export default Login;