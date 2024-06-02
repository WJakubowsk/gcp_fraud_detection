import {useState, useEffect, useRef} from "react";
import {useNavigate} from "react-router-dom";
import api from "../api";
import Transaction from "../components/Transaction";
import BTCTracker from "../components/BTCTracker";
import "../styles/Home.css";
import "../styles/Header.css";

import avatar from '../assets/avatar.png';
import { Button } from "@mui/material";
import btcLogo from '../assets/Bitcoin.png';

function Home() {
    const [transactions, setTransactions] = useState([]);
    const [amount, setAmount] = useState("");
    const [description, setDescription] = useState("");
    // const [chartData, setChartData] = useState(null);
    const [totalAmount, setTotalAmount] = useState(0);
    const navigate = useNavigate();
    const [selectedPeriod, setSelectedPeriod] = useState('12h');
    const date = new Date();
    const formattedDate = date.toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });

    useEffect(() => {
        getTransactions();
        // updateChartData(transactions);
        calculateTotalAmount(transactions);
    }, []);

    useEffect(() => {
        if (transactions.length > 0) {
            // updateChartData(transactions);
            calculateTotalAmount(transactions);
        }
    }, [transactions]);

    const getTransactions = () => {
        api.get("/transactions/").then((response) => response.data).then((data) => {
            setTransactions(data);
            // updateChartData(data);
            calculateTotalAmount(data);
        }).catch((error) => { alert(error); });
    }

    const deleteTransaction = (id) => {
        api.delete(`/transactions/delete/${id}/`).then((response) => {
            if (response.status === 204) alert("Transaction deleted!")
            else alert("Failed to delete transaction.")
            getTransactions();
        }).catch((error) => { alert(error); });
    }

    const createTransaction = (e) => {
        e.preventDefault();
        api.post("/transactions/", {amount, description}).then((response) => {
            if (response.status === 201) alert("Transaction created!")
            else alert("Failed to create transaction.")
            getTransactions();
        }).catch((error) => { alert(error); });
        setAmount("");
        setDescription("");
    }

    // const updateChartData = (transactions) => {
    //     const dates = transactions.map((transaction) => {
    //         const transactionDate = new Date(transaction.date);
    //         const year = transactionDate.getFullYear();
    //         const month = String(transactionDate.getMonth() + 1).padStart(2, '0');
    //         const day = String(transactionDate.getDate()).padStart(2, '0');
    //         const hours = String(transactionDate.getHours()).padStart(2, '0');
    //         const minutes = String(transactionDate.getMinutes()).padStart(2, '0');
    //         return `${year}-${month}-${day} ${hours}:${minutes}`;
    //     });
    //     const totalAmounts = calculateTotalAmountAtTheTime(transactions);

    //     setChartData({
    //       labels: dates,datasets: [
    //           {
    //             data: totalAmounts,
    //             backgroundColor: "rgba(192, 75, 192, 0.2)",
    //             borderColor: "rgba(192, 75, 192, 1)",
    //             borderWidth: 1,
    //         },
    //       ],
    //     });

    //     if (chartRef.current) {
    //       chartRef.current.destroy();
    //     }

    //     const ctx = document.getElementById("myChart").getContext("2d");
    //     chartRef.current = new Chart(ctx, {
    //       type: "line",
    //       data: chartData,
    //       options: {
    //           scales: {
    //               y: {
    //                   beginAtZero: true,
    //               },
    //           },
    //           plugins: {
    //               legend: {
    //                   display: false,
    //               },
    //               tooltip: {
    //                 callbacks: {
    //                     label: function (context) {
    //                         const label = context.dataset.label || '';
    //                         if (context.parsed.y !== null) {
    //                             const transaction = transactions[context.dataIndex]; // Get the transaction at the current index
    //                             const totalAmount = totalAmounts[context.dataIndex]; // Get the total amount at the current index
    //                             const labelText = [
    //                                 `Total Amount: ${totalAmount}`,
    //                                 `Transaction Amount: ${transaction.amount}`,
    //                                 `Description: ${transaction.description}`
    //                             ];
    //                             return labelText.join('\n');
    //                         } else {
    //                             return null;
    //                         }
    //                     }
    //                 }
    //               }
    //           }
    //       },
    //   });
    // };

    // const chartRef = useRef(null);
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
            {/* <img src={avatar} alt="User avatar" width={'20%'}/> */}
            {/* <span>Username</span> */}
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