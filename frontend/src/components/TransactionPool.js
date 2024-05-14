import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Button } from 'react-bootstrap';
import Transaction from './Transaction';
import { API_BASE_URL, SECONDS_JS } from '../config';
import history from '../history';

const POLL_INTERVAL = 10 * SECONDS_JS

function TransactionPool() {

	const [transactions, setTransactions] = useState([]);

	const fetchTransactions = () => {
		fetch(`${API_BASE_URL}/transactions`)  //here we introduce "polling logic"" to re-fetch the list of transactions every 10 seconds so that the application owner always has an accurate history of transactions 
			.then(response => response.json())
			.then(json => {
				console.log('transactions json', json);
				setTransactions(json);
			});
	} 

	useEffect(() => {
		fetchTransactions();

		const intervalId = setInterval(fetchTransactions, POLL_INTERVAL);

		return () => clearInterval(intervalId); //here we return a callback function where we input the code we want to run the component "unmounts from the document" i.e. when user navigates away from the transaction-pool page 
	}, []);										// we run the clear interval line which halts  fetchTransactions from running every 10 seconds

	const fetchMineBlock = () => {
		fetch(`${API_BASE_URL}/blockchain/mine`)
			.then(() => {
				alert('Success!');

				history.push('/blockchain');
			});
	}

	return (
		<div className="TransactionPool">
			<Link to="/">Home</Link>
			<hr />
			<h3>Transaction Pool</h3>
			<div>
				{
					transactions.map(transaction => (
						<div key={transaction.id}>
							<hr />
							<Transaction transaction={transaction} />
						</div>
					))
				}
			</div>
			<hr />
			<Button
				variant="danger"
				onClick={fetchMineBlock}
			>
				Mine a block of these trasactions
			</Button>
		</div>
	)

}



export default TransactionPool