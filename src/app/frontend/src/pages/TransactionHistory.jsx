// import "../styles/Home.css";
import {useState, useEffect} from "react";
import Transaction from "../components/Transaction";
import {useNavigate} from "react-router-dom";
import api from "../api";
import { Button } from "@mui/material";
import "../styles/TransactionHistory.css";

function History() {
    const [transactions, setTransactions] = useState([])
    const navigate = useNavigate();
    const date = new Date();
    const formattedDate = date.toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });

    useEffect(() => {
        getTransactions();
    }, []);

    const predictAll = async () => {
        console.log('Before prediction:', transactions[3]);
        try {
            document.body.style.cursor = 'wait';
            const response = await api.post(`/transactions/predict-all/`);
            await getTransactions();
        } catch (error) {
            if (error.response.status === 401) {
                navigate("/login");
                alert("Please login again, your session expired.");
            } else {
                alert(error);
            }
        } finally {
            document.body.style.cursor = 'default';
        }
    };

    const getTransactions = async () => {
        try{
            const response = await api.get("/transactions/");
            setTransactions(response.data);
        } catch (error) {
            if (error.response.status === 401) {
                navigate("/login");
                alert("Please login again, your session expired.");
            } else {
                alert(error);
            }
        }
    }

    const handleLogout = () => {
        navigate("/logout");
    };

    return (
        <div className="container">
      <header className="header">
            <div className="title">
                <h1><a href='/' style={{color: 'inherit', textDecoration: 'none'}}>BTC Tracker</a></h1>
                <h3>{formattedDate}</h3>
            </div>
            <div className="user-info">
            <Button className="settings" onClick={handleLogout}>Logout</Button>
            </div>
        </header>


        <div className="block block-history">
            <div>
            <div className="columns">
                    <div className="column-item"><p>Date</p></div>
                    <div className="column-item"><p>Title</p></div>
                    <div className="column-item"><p>Transaction Amount</p></div>
                    <div className="column-item"><p>Licit / Illicit</p></div>
                    <div className="column-item predict"><button className="transaction-predict predict-all" onClick={predictAll}>Predict All</button></div>
            </div>
            </div>
            <div>
                {transactions.sort((a, b) => new Date(b.date) - new Date(a.date)).map((transaction) => (
                    <Transaction transaction={transaction} key={transaction.id} history={true}/>
                ))}
            </div>
        </div>
      </div>
    );
}

export default History;