import {useState} from "react";
import api from "../api";
import {useNavigate} from "react-router-dom";
import {ACCESS_TOKEN, REFRESH_TOKEN} from "../constants.js";
import '../styles/Form.css';
import LoadingIndicator from "./LoadingIndicator.jsx";

function Form({route, method}) {
    const[username, setUsername] = useState("");
    const[password, setPassword] = useState("");
    const[loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const name = method === "login" ? "Login" : "Register";

    const handleRegisterClick = (e) => {
        e.preventDefault();
        navigate("/register");
    };

    const handleLoginClick = (e) => {
        e.preventDefault();
        navigate("/login");
    };

    const handleSubmit = async (e) => {
        setLoading(true);
        e.preventDefault();

        try {
            const res = await api.post(route, { username, password });
            if (method === "login") {
                localStorage.setItem(ACCESS_TOKEN, res.data.access);
                localStorage.setItem(REFRESH_TOKEN, res.data.refresh);
                navigate("/");
            } else {
                navigate("/login");
            }
        } catch (error) {
            if (method === "login" && (error.response.status==400 || error.response.status==401 )) {
                alert("Login unsucessfull, please try again");
            } else if (error.response.status==400 || error.response.status==401 ) {
                alert("Registration unsucessfull, please try again");
            }
        } finally {
            setLoading(false);
        }
    }

    return <form onSubmit={handleSubmit} className="form-container">
        <h1>{name}</h1>
        <input className="form-input" type="text" placeholder="Username" value={username} onChange={(e) => setUsername(e.target.value)} />
        <input className="form-input" type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} />
        {loading && <LoadingIndicator />}
        
    <button className="form-button" type="submit">{name}</button>
    {name === 'Login' ? (
        <div>
            <p>New User? <a href="/register" onClick={handleRegisterClick} style={{color: 'white'}}>Register</a></p>
        </div>
    ) : (
        <div>
            <p>Already a user? <a href="/login" onClick={handleLoginClick} style={{color: 'white'}}>Login</a></p>
        </div>
    )}
    </form>
}

export default Form;