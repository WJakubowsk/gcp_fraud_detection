import React from "react";
import "../styles/Transaction.css";
import "../styles/TransactionHistory.css";


function Transaction({transaction, onDelete}) {
    const formattedDate = new Date(transaction.date).toLocaleDateString();
    const formattedAmount = new Intl.NumberFormat('en-US', {style: 'currency', currency: 'USD'}).format(transaction.amount);

    return (
        <div className="transaction-container">
            <div className="transaction-left">
                <p className="transaction-date">{formattedDate}</p>
                <p className="transaction-description">{transaction.description}</p>
            </div>
            <div className="transaction-right">
                <p className="transaction-amount">{formattedAmount}</p>
            </div>
        </div>
    )
}

export default Transaction