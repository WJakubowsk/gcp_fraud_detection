import React from "react";
import "../styles/Transaction.css";

function Transaction({transaction, onDelete}) {
    const formattedDate = new Date(transaction.date).toLocaleDateString("en-US");

    return (
        <div className="transaction-container">
            <p className="transaction-amount">{transaction.amount}</p>
            <p className="transaction-description">{transaction.description}</p>
            <p className="transaction-date">{formattedDate}</p>
            <button className="delete-button" onClick={() => onDelete(transaction.id)}>
                Delete
            </button>
        </div>
    )
}

export default Transaction