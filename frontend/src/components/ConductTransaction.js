import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { FormGroup, FormControl, Button } from 'react-bootstrap';
import { API_BASE_URL} from '../config';
import history from '../history';

function ConductTransaction() {
	const [amount, setAmount] = useState(0);
	const [recipient, setRecipient] = useState('');
	const [knownAddresses, setKnownAddresses] = useState([]);

	useEffect(() => { //here we use the UseEffect hook to fetch the known addresses
		fetch(`${API_BASE_URL}/known-addresses`)
			.then(response => response.json())
			.then(json => setKnownAddresses(json));
	}, []);
	

	const updateRecipient = event => {
		setRecipient(event.target.value);  //event.target.value represents what the user's typed so far & this is what we want to set as the recipient
	}	
	const updateAmount = event => {
		setAmount(Number(event.target.value)); //Number converts event.target.value from a string to a number
	}

	const submitTransaction = () => {
		fetch(`${API_BASE_URL}/wallet/transact`, {  //here we make a request to the url http://localhost:5000/wallet/transact
			method: 'POST',                                // the default request type for fetch is POST but you can optionally add a second argument to
			headers: { 'Content-Type': 'application/json'}, // specify the request type, as we do here
			body: JSON.stringify({ recipient, amount })
		}).then(response => response.json())  // this line gets the response from the whole submitTransaction const, then returns the .json() method of that
			.then(json => {
				console.log('submit Transaction json', json);

				alert('Success!');

				history.push('/transaction-pool'); //this method will automatically take the user to the the Transaction Pool page after they submit a transaction
			});
	} 	 


// For below: we have 2 FormGroups here, one for the amount and one for the recipient
//  The FormControl component allows us to specify attributes to customize the input

	return (
		<div className="ConductTransaction">
			<Link to='/'>Home</Link>
				<hr />
				<h3>Conduct a Transaction</h3>
				<br />   
				<FormGroup>  
					<FormControl 
						input="text"
						placeholder="recipient"
						value={recipient}
						onChange={updateRecipient}  //every time this input is interacted with, React will pass in an event object when it calls updateRecipient within its engine (see above where we defined the updateRecipient const)
					/>
			</FormGroup>   
			<FormGroup>
				<FormControl 
				input="number"
				placeholder="amount"
				value={amount}
				onChange={updateAmount}
				/>
			</FormGroup>
			<div>
				<Button
					variant="danger"
					onClick={submitTransaction}
				>
					Submit
				</Button>
			</div>
			<br />
			<h4>Known Addresses</h4>
			<div>
				{
					knownAddresses.map((knownAddress, i) => (
						<span key={knownAddress}>
							<u>{knownAddress}</u>{i !== knownAddresses.length - 1 ? ', ' : ''}  
						</span>
					))
				}
			</div>
  
		</div> 
	)
}




export default ConductTransaction;