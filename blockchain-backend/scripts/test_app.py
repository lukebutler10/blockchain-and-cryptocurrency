import requests
import time

from backend.wallet.wallet import Wallet


BASE_URL = 'http://localhost:5000/'

'''
NOTE:
The requests.get method makes a request to a web page, and return the status code
The requests.posts method makes a POST request to a web page, and return the response text:
'''

def get_blockchain():
	return requests.get(f'{BASE_URL}/blockchain').json()
#this is pulling the data from the location of that link, which you can see coded in init.py file in the route_blockchain method

def get_blockchain_mine():
	return requests.get(f'{BASE_URL}/blockchain/mine').json()


def post_wallet_transact(recipient, amount):  
	return requests.post(
			f'{BASE_URL}/wallet/transact',
			json = {'recipient':recipient, 'amount':amount}
		).json()

def get_wallet_info():
	return requests.get(
			f'{BASE_URL}/wallet/info').json()



start_blockchain =get_blockchain()
print(f'start_blockchain: {start_blockchain}')

recipient = Wallet().address

post_wallet_transact_1 = post_wallet_transact(recipient, 21)
print(f'\npost_wallet_transact_1: {post_wallet_transact_1}')

time.sleep(1)

post_wallet_transact_2 = post_wallet_transact(recipient, 13)
print(f'\npost_wallet_transact_2: {post_wallet_transact_2}')

time.sleep(1)
#We pause our script for 1 sec here because the 2 transactions above need to be received by the transaction so that they appear in the node's 
#transaction pool. This is done by a network request which takes an unknown amount of time so we pause to allow the mined block below to
#to consist of the previous 2 transactions

mined_block = get_blockchain_mine()
print(f'\nmined_block: {mined_block}')

wallet_info = get_wallet_info()
print(f'\nwallet_info: {wallet_info}')