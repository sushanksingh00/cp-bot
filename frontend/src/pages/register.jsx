import axios from "axios";
import { useState } from "react";
import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { Link } from "react-router-dom";
import api from "../api/api";



function Register() {

    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [email, setEmail] = useState("");
    const navigate = useNavigate();

    
    const handleRegister = async () => {
        try{
            const response = await api.post(
                "/auth/register", 
                {
                    username, 
                    email,
                    password
                }
            );
            localStorage.setItem(
                "token",
                response.data.token
            );
            console.log("Registered");
            navigate('/login')

        }catch(error){
            if (error.response?.status === 401) {
                alert("User already exists");
            }
            console.log(error);
        }
    }

    return(
        <div className="min-h-screen flex items-center justify-center bg-white">
            <div className="w-full max-w-md bg-blue-100 rounded-2xl shadow-xl p-8">
                <h1 className="text-4xl flex justify-center items-start mb-2 font-bold">Register</h1>
                <h1 className="mb-15 text-gray-500 text-center">Enter your username, email, and password to create your account</h1>

                <div className="flex flex-col gap-4">
                    <input placeholder="Username" value={username} type="text" onChange={(e) => setUsername(e.target.value)}
                    className="p-3 rounded-2xl shadow-lg bg-white"></input>

                    <input placeholder="Email" value={email} type="email" onChange={(e) => setEmail(e.target.value)}
                    className="p-3 rounded-2xl shadow-lg bg-white"></input>

                    <input placeholder="Password" value={password} type="password" onChange={(e) => setPassword(e.target.value)}
                    className="p-3 rounded-2xl shadow-lg bg-white"></input>

                    <button onClick={handleRegister}
                    className="px-6 py-3 bg-blue-500 font-semibold text-white rounded-2xl shadow-lg hover:bg-blue-700">Register</button>
                    <Link to="/login">Login?</Link>
                </div>
            </div>

        </div>
    )
}

export default Register;