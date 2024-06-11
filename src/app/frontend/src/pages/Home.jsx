import {useState, useEffect} from "react";
import {useNavigate} from "react-router-dom";
import api from "../api";
import Transaction from "../components/Transaction";
import BTCTracker from "../components/BTCTracker";
import "../styles/Home.css";
import "../styles/Header.css";

import { Button } from "@mui/material";
import btcLogo from '../assets/Bitcoin.png';

function Home() {
    const [transactions, setTransactions] = useState([]);
    const [amount, setAmount] = useState("");
    const [description, setDescription] = useState("");
    const [totalAmount, setTotalAmount] = useState(0);
    const navigate = useNavigate();
    const [selectedPeriod, setSelectedPeriod] = useState('12h');
    const date = new Date();
    const formattedDate = date.toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });

    useEffect(() => {
        getTransactions();
        calculateTotalAmount(transactions);
    }, []);

    useEffect(() => {
        if (transactions.length > 0) {
            calculateTotalAmount(transactions);
        }
    }, [transactions]);

    const getTransactions = () => {
        api.get("/transactions/").then((response) => response).then((response) => {
            console.log('Fetched transactions:', response.data);
            setTransactions(response.data);
            calculateTotalAmount(response.data);
        }).catch((error) => { 
            if (error.response.status === 401) {
                navigate("/login");
                alert("Please login again, your session expired.");
            } else {
                alert(error);
            }
        });
    }

    // const deleteTransaction = (id) => {
    //     api.delete(`/transactions/delete/${id}/`).then((response) => {
    //         if (response.status === 401) {
    //             navigate("/login");
    //         } else {
    //             if (response.status === 204) alert("Transaction deleted!")
    //             else alert("Failed to delete transaction.")
    //             getTransactions();
    //         }
    //     }).catch((error) => { alert(error); });
    // }

    const createTransaction = (e) => {
        e.preventDefault();
        api.post("/transactions/", {amount, description}).then((response) => {
            if (response.status === 201) {
                alert("Transaction created!")
            } else {
                alert("Failed to create transaction.")
                getTransactions();
            }
        }).catch((error) => { 
            if (error.response.status === 401) {
                navigate("/login");
                alert("Please login again, your session expired.");
            } else {
                alert(error);
            }
        });
        setAmount("");
        setDescription("");
    }

    const calculateTotalAmount = (transactions) => {
        const total = transactions.reduce((acc, curr) => acc + parseInt(curr.amount), 0);
        setTotalAmount(total);
    };
    
    const handleLogout = () => {
        navigate("/logout");
    };

    return (
    <div className="container">
      <header className="header">
            <div className="title">
                <h1>BTC Tracker</h1>
                <h3>{formattedDate}</h3>
            </div>
            <div className="user-info">
            <Button className="settings" onClick={handleLogout}>Logout</Button>
            </div>
        </header>
      <div className="grid">
        <div className="block block1">
          <h5>Current Balance: </h5>
          <h1>${totalAmount}</h1>
        </div>
        <div className="block block2">
            <div className="logo">
                <img src={btcLogo} width={'50%'}/> {/* replace with the path to the BTC logo */}
            </div>
            <div className="summary">
                <BTCTracker plot={false} selectedPeriod={selectedPeriod}/>
            </div>
        </div>
        <div className="block block3">
          <h2>Buy / Sell</h2>

          <form onSubmit={createTransaction}>
            <input type="text" id="description" name="description" value={description} onChange={(e) => setDescription(e.target.value)} placeholder="Title" required/>
            <input type="number" id="amount" name="amount" value={amount} placeholder="Amount" onChange={(e) => setAmount(e.target.value)} required />
            <input type="submit" value="Submit" />
          </form>
        </div>
        <div className="block block4">
            <BTCTracker plot={true} selectedPeriod={selectedPeriod}/>
            <div className="button-group">
                <button className={selectedPeriod === '12h' ? 'selected' : ''} onClick={() => setSelectedPeriod('12h')}>12h</button>
                <button className={selectedPeriod === '1w' ? 'selected' : ''} onClick={() => setSelectedPeriod('1w')}>1w</button>
                <button className={selectedPeriod === '3M' ? 'selected' : ''} onClick={() => setSelectedPeriod('3M')}>3M</button>
            </div>
        </div>
        <div className="block block5">
        <h2>Transactions</h2>
                {transactions.sort((a, b) => new Date(b.date) - new Date(a.date)).slice(0, 6).map((transaction) => (
                    <Transaction transaction={transaction} key={transaction.id} history={false}/>
                    ))}
        <div className="link-container">
            <a href="/transactions">View All Transactions</a>
        </div>
        </div>
      </div>
    </div>
    )
}

export default Home