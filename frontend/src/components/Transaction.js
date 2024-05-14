import React from 'react';

function Transaction({ transaction }) {
	const { input, output } = transaction;
	const recipients = Object.keys(output); //an array of the recipients in the transaction

	return (
		<div className="Transaction">
			<div>From: {input.address}</div>
			{
				recipients.map(recipient => (
					<div key={recipient}>
						To: {recipient} | Sent: {output[recipient]}
					</div>
				))
			}
		</div>		

		)

}

export default Transaction;