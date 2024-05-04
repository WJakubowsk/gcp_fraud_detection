import {useState, useEffect, useRef} from "react";
import api from "../api";
import Transaction from "../components/Transaction";
import "../styles/Home.css";
import Chart from "chart.js/auto";
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';

function Home() {
    const [transactions, setTransactions] = useState([]);
    const [amount, setAmount] = useState("");
    const [description, setDescription] = useState("");
    const [chartData, setChartData] = useState(null);
    const [totalAmount, setTotalAmount] = useState(0);
    const [showTransactions, setShowTransactions] = useState(false);

    useEffect(() => {
        getTransactions();
        updateChartData(transactions);
        calculateTotalAmount(transactions);
    }, []);

    useEffect(() => {
        if (transactions.length > 0) {
            updateChartData(transactions);
            calculateTotalAmount(transactions);
        }
    }, [transactions]);

    const getTransactions = () => {
        api.get("/transactions/").then((response) => response.data).then((data) => {
            setTransactions(data);
            updateChartData(data);
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

    const updateChartData = (transactions) => {
        const dates = transactions.map((transaction) => {
            const transactionDate = new Date(transaction.date);
            const year = transactionDate.getFullYear();
            const month = String(transactionDate.getMonth() + 1).padStart(2, '0');
            const day = String(transactionDate.getDate()).padStart(2, '0');
            const hours = String(transactionDate.getHours()).padStart(2, '0');
            const minutes = String(transactionDate.getMinutes()).padStart(2, '0');
            return `${year}-${month}-${day} ${hours}:${minutes}`;
        });
        const totalAmounts = calculateTotalAmountAtTheTime(transactions);

        setChartData({
          labels: dates,datasets: [
              {
                data: totalAmounts,
                backgroundColor: "rgba(192, 75, 192, 0.2)",
                borderColor: "rgba(192, 75, 192, 1)",
                borderWidth: 1,
            },
          ],
        });

        if (chartRef.current) {
          chartRef.current.destroy();
        }

        const ctx = document.getElementById("myChart").getContext("2d");
        chartRef.current = new Chart(ctx, {
          type: "line",
          data: chartData,
          options: {
              scales: {
                  y: {
                      beginAtZero: true,
                  },
              },
              plugins: {
                  legend: {
                      display: false,
                  },
                  tooltip: {
                    callbacks: {
                        label: function (context) {
                            const label = context.dataset.label || '';
                            if (context.parsed.y !== null) {
                                const transaction = transactions[context.dataIndex]; // Get the transaction at the current index
                                const totalAmount = totalAmounts[context.dataIndex]; // Get the total amount at the current index
                                const labelText = [
                                    `Total Amount: ${totalAmount}`,
                                    `Transaction Amount: ${transaction.amount}`,
                                    `Description: ${transaction.description}`
                                ];
                                return labelText.join('\n');
                            } else {
                                return null;
                            }
                        }
                    }
                  }
              }
          },
      });
    };

    const chartRef = useRef(null);
    const calculateTotalAmount = (transactions) => {
        const total = transactions.reduce((acc, curr) => acc + parseInt(curr.amount), 0);
        setTotalAmount(total);
    };
    const calculateTotalAmountAtTheTime = (transactions) => {
        let totals = [];
        let total = 0;
        transactions.forEach( num => {
          total += parseInt(num.amount);
          totals.push(total);
        });
        console.log(totals);
        return totals;
    };

    return (
        <div>
            {/* <div>
                <h2>Transactions</h2>
                {transactions.map((transaction) => (
                    <Transaction transaction={transaction} onDelete={deleteTransaction} key={transaction.id}/>
                    ))}
            </div> */}
            <h2>Total Amount in Transactions: {totalAmount}</h2>
            <button onClick={() => setShowTransactions(!showTransactions)}>Expand History</button>
            {showTransactions && (
                <TableContainer>
                <Table>
                    <TableHead>
                        <TableRow>
                            <TableCell>Date</TableCell>
                            <TableCell>Amount</TableCell>
                            <TableCell>Description</TableCell>
                            <TableCell>Licit/Illicit</TableCell>
                            <TableCell>Action</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {transactions.map((transaction) => (
                            <TableRow key={transaction.id}>
                                <TableCell>{transaction.date}</TableCell>
                                <TableCell>{transaction.amount}</TableCell>
                                <TableCell>{transaction.description}</TableCell>
                                <TableCell>Licit</TableCell>
                                <TableCell>
                                    <button onClick={() => deleteTransaction(transaction.id)}>Delete</button>
                                </TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </TableContainer>
            )}
            <h2>Create a Transaction</h2>
            <form onSubmit={createTransaction}>
                <label htmlFor="amount">Amount:</label>
                <br/>
                <input type="number" id="amount" name="amount" value={amount} onChange={(e) => setAmount(e.target.value)} required/>
                <label htmlFor="description">Description:</label>
                <br/>
                <textarea id="description" name="description" value={description} onChange={(e) => setDescription(e.target.value)} required></textarea>
                <br/>
                <input type="submit" value="Submit"/>
            </form>
            <h2></h2>
            <canvas id="myChart"  width= "20%" height= "10%"></canvas>
        </div>
    )
}

export default Home