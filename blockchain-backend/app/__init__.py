import os
import requests
import random

from flask import Flask, jsonify, request
from flask_cors import CORS
#jsonify can transform a Python object into an instance of Flask's response class which is in JSON format

from backend.blockchain.blockchain import Blockchain
from backend.wallet.wallet import Wallet
from backend.wallet.transaction import Transaction
from backend.wallet.transaction_pool import TransactionPool
from backend.pubsub import PubSub

app = Flask(__name__)  #it is convention in Flask to name the application the same as the module
CORS(app, resources={r'/*': {'origins': 'http://localhost:3000'}})
blockchain = Blockchain()
wallet = Wallet(blockchain)
transaction_pool = TransactionPool()
pubsub = PubSub(blockchain, transaction_pool)

#now we define an endpoint
@app.route('/')
def route_default(): 
	return 'Welcome to the blockchain'

@app.route('/blockchain')
def route_blockchain():
	return jsonify(blockchain.to_json())
	#return jsonify([1])


@app.route('/blockchain/range')
def route_blockchain_range():
	# http://localhost:5000/blockchain/range?start=2&end=5
	start = int(request.args.get('start'))
	end = int(request.args.get('end'))

	return jsonify(blockchain.to_json()[::-1][start:end]) # the [::-1] here ensures we display the blocks in frontend from newest to oldest


@app.route('/blockchain/length')
def route_blockchain_length():
	return jsonify(len(blockchain.chain))


@app.route('/blockchain/mine') 
def route_blockchain_mine():
	transaction_data = transaction_pool.transaction_data()
	transaction_data.append(Transaction.reward_transaction(wallet).to_json())

	blockchain.add_block(transaction_data)

	block = blockchain.chain[-1]
	pubsub.broadcast_block(block)
	transaction_pool.clear_blockchain_transactions(blockchain)

	return jsonify(block.to_json())


@app.route('/wallet/transact', methods=["POST"])
def route_wallet_transact():
	transaction_data = request.get_json()
	transaction = transaction_pool.existing_transaction(wallet.address)

	if transaction: #this will run if transaction != None
		transaction.update(
			wallet, 
			transaction_data["recipient"], 
			transaction_data["amount"]
		)

	else: 
		transaction = Transaction(
			wallet, 
			transaction_data["recipient"], 
			transaction_data["amount"]
		)




	pubsub.broadcast_transaction(transaction)

	return jsonify(transaction.to_json())

@app.route('/wallet/info')
def route_wallet_info():
	return jsonify({'address':wallet.address, 'balance':wallet.balance})

@app.route('/known-addresses')
def route_known_addresses():
	known_addresses = set()

	for block in blockchain.chain:
		for transaction in block.data:
			known_addresses.update(transaction['output'].keys())

	return jsonify(list(known_addresses))

@app.route('/transactions')
def route_transactions():
	return jsonify(transaction_pool.transaction_data())

ROUTE_PORT = 5000
PORT = ROUTE_PORT

if os.environ.get('PEER') == 'True':  #note this 'True' is a string, it's object type isn't Boolean
	PORT = random.randint(5001,6000)

	result = requests.get(f'http://localhost:{ROUTE_PORT}/blockchain')
	result_blockchain = Blockchain.from_json(result.json())
 
	try:
		blockchain.replace_chain(result_blockchain.chain)
		print('\n -- Successfully syncronized the local chain')

	except Exception as e:
		print(f'\n -- Error syncronizing: {e}')	

if os.environ.get('SEED_DATA') == 'True':
	for i in range(10):
		blockchain.add_block([
			Transaction(Wallet(), Wallet().address, random.randint(2,50)).to_json(),
			Transaction(Wallet(), Wallet().address, random.randint(2,50)).to_json()
		])
#above we randomly create 10 blocks and add them to the blockchain.
#this was done when printing the blocks on the web UI page in order to show the use of pagination when larger amounts of blocks are in the chain

	for  i in range(3):
		transaction_pool.set_transaction(
			Transaction(Wallet(), Wallet().address, random.randint(2,50))
		)



app.run(port=PORT) 

