import { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

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
        <>
            <h1 className="text-5xl font-bold flex justify-center item-start py-30">LOGIN</h1>

            <div className="text-lg flex flex-col items-center item-start ">
                <input
                    type="text"
                    placeholder="Username"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    className="border p-2 rounded"
                />

                <br />

                <input
                    type="password"
                    placeholder="Password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    className="border p-2 rounded"
                />

                <br />

                <button onClick={handleLogin} className="px-10 py-2 rounded bg-blue-500 text-white">
                    Login
                </button>
            </div>
        </>
    );
}

export default Login;