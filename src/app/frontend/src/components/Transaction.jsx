import React, { useState, useEffect } from "react";
import "../styles/Transaction.css";
import api from "../api";


function Transaction({transaction, history = false}) {
    const [currTransaction, setCurrTransaction] = useState(transaction);
    const formattedDate = new Date(transaction.date).toLocaleDateString();
    const formattedAmount = new Intl.NumberFormat('en-US', {style: 'currency', currency: 'USD'}).format(transaction.amount);
    const [Licit, setLicit] = useState(transaction.isFraud == true ? 'Illicit' : transaction.isFraud == false ? 'Licit' : "Unknown");
    const fraudClass = Licit === 'Licit' ? 'transaction-fraud-licit' : Licit === 'Illicit' ? 'transaction-fraud-illicit' : 'transaction-fraud-default';
    const [isConfirmed, setIsConfirmed] = useState(transaction.isConfirmed);


    useEffect(() => {
        setCurrTransaction(transaction);
        setLicit(transaction.isFraud == true ? 'Illicit' : transaction.isFraud == false ? 'Licit' : "Unknown");
    }, [transaction]);

    useEffect(() => {
        setLicit(currTransaction.isFraud == true ? 'Illicit' : currTransaction.isFraud == false ? 'Licit' : "Unknown");
    });

    const handleConfirm = () => {
        updateTransaction(currTransaction.id, { isConfirmed: true });
        setIsConfirmed(true);
    };

    const updateTransaction = (id, updatedFields) => {
        api.patch(`/transactions/update/${id}/`, updatedFields)
        .then((response) => {
            setCurrTransaction(response.data);
        })
        .catch((error) => { 
            if (error.response.status === 401) {
                navigate("/login");
                alert("Please login again, your session expired.");
            } else {
                alert(error);
            }
        });
    };

    const handleNotConfirm = () => {
        updateTransaction(currTransaction.id, currTransaction.isFraud === true ? { isFraud: false } : { isFraud : true });
    };

    const handleMakePrediction = async () => {
        try {
            document.body.style.cursor = 'wait';
            await api.post(`/transactions/predict/${currTransaction.id}/`);
            const getResponse = await api.get(`/transactions/retrieve/${currTransaction.id}/`);
            console.log(getResponse.data)
            setCurrTransaction(getResponse.data);
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

    if (history) {
        return (
            <div className="transaction-container-history">
                <div className="transaction-item-history">
                    <p className="transaction-date-history">{formattedDate}</p>
                </div>
                <div className="transaction-item-history">
                    <p className="transaction-description-history">{transaction.description}</p>
                </div>
                <div className="transaction-item-history">
                    <p className="transaction-amount-history">{formattedAmount}</p>
                </div>
                <div className={`transaction-item-history ${fraudClass}`}>
                    <p className="transaction-fraud"> {Licit} </p>
                </div>
                <div className="transaction-item-history predict">
                    {isConfirmed ? (
                        <p className="transaction-confirmed">Confirmed</p>
                    ) : (
                        Licit === "Unknown" ? (
                            <div className="buttons pred"><button className="transaction-predict" onClick={handleMakePrediction}>Predict</button></div>
                        ) : (
                            <div className="buttons">
                                <button className="transaction-confirm confirm" onClick={handleConfirm}>Confirm</button>
                                <button className="transaction-not-confirm change" onClick={handleNotConfirm}>Change</button>
                            </div>
                        )
                    )}
                </div>
            </div>
        );
    }

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