import axios from "axios";
import { useState } from "react";
import { useEffect } from "react";
import { useNavigate } from "react-router-dom";


function Register() {

    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [email, setEmail] = useState("");
    const navigate = useNavigate();

    
    const handleRegister = async () => {
        try{
            const response = await axios.post(
                "http://localhost:8000/auth/register", 
                {
                    username, 
                    email,
                    password
                }
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
        <>
            <h1 className="text-5xl flex justify-center items-start py-30 font-bold">REGISTER</h1>
            <div className="flex flex-col items-center text-lg gap-4">
                <input placeholder="Username" value={username} type="text" onChange={(e) => setUsername(e.target.value)}
                className="border p-2 rounded"></input>

                <input placeholder="Email" value={email} type="email" onChange={(e) => setEmail(e.target.value)}
                className="border p-2 rounded"></input>

                <input placeholder="Password" value={password} type="password" onChange={(e) => setPassword(e.target.value)}
                className="border p-2 rounded"></input>

                <button onClick={handleRegister}
                className="px-6 py-2 bg-blue-500 text-white rounded">Register</button>
            </div>

        </>
    )
}

export default Register;