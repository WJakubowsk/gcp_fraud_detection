import {useState, useEffect} from "react";
import api from "../api";
import Transaction from "../components/Transaction";
import "../styles/Home.css";

function Home() {
    const [transactions, setTransactions] = useState([]);
    const [amount, setAmount] = useState("");
    const [description, setDescription] = useState("");

    useEffect(() => {
        getTransactions();
    }, []);

    const getTransactions = () => {
        api.get("/transactions/").then((response) => response.data).then((data) => { setTransactions(data); console.log(data) }).catch((error) => { alert(error); });
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
    }

    return (
        <div>
            <div>
                <h2>Transactions</h2>
                {transactions.map((transaction) => (
                    <Transaction transaction={transaction} deleteTransaction={deleteTransaction} key={transaction.id}/>
                    ))}
            </div>
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
        </div>
    )
}

export default Home