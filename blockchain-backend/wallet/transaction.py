import uuid
import time

from backend.wallet.wallet import Wallet
from backend.config import MINING_REWARD, MINING_REWARD_INPUT

class Transaction:
	'''
	Document of an exchange in currency from a sender to one or more recipients.
	'''
	def __init__(self, sender_wallet=None, recipient=None, amount=None, id=None, output=None, input=None):
		#note below with the "or" statements, the "self" objects = first option if specified by user, if not then automatically = 2nd option

		self.id = id or str(uuid.uuid4())[0:8]  #use same method to get our transaction id as we did to get the wallet address, with uuid
		self.output = output or self.create_output(   #a dictionary with key-value pairs that are the recipients and the amounts they get
			sender_wallet,
			recipient,
			amount
		) 
		self.input = input or self.create_input(sender_wallet, self.output) #a dictionary with several pieces of info about the 
		#transaction (see below in the create_input method)

	def create_output(self, sender_wallet, recipient, amount):
		'''
		Structure the output data for the transaction
		'''

		if amount > sender_wallet.balance:
			raise Exception('Amount exceeds balance')
		output = {}
		output[recipient] = amount
		output[sender_wallet.address] = sender_wallet.balance - amount

		return output

	def create_input(self, sender_wallet, output):
		'''
		Structure the input data for the transaction
		Sign the transaction and include the sender's public key and address
		'''
		return {
			'timestamp': time.time_ns(),
			'amount' : sender_wallet.balance,
			'address' : sender_wallet.address,
			'public_key' : sender_wallet.public_key,
			'signature' : sender_wallet.sign(output) #use output as 'data' parameter in the 'sign' method
		}
		
	def update(self, sender_wallet, recipient, amount):
		'''
		Update the transaction with an existing or new recipient
		'''
		if amount > self.output[sender_wallet.address]:
			raise Exception('Amount exceeds balance')

		if recipient in self.output: #if the recipient has already received an amount in this set of transactions we'll just add to what they have already
			self.output[recipient] = self.output[recipient] + amount
		else:
			self.output[recipient] = amount

		self.output[sender_wallet.address] = \
		self.output[sender_wallet.address] - amount

		self.input = self.create_input(sender_wallet, self.output)


	def to_json(self):
		'''
		Serialize the transaction
		'''
		return self.__dict__


	@staticmethod
	def from_json(transaction_json):
		'''
		Deserialize a transaction's representation back into a Transaction instance
		Own words: When we created this method we added 3 new optional parameters that the user can specify when creating a Transaction object. They
		are id, outout and input i.e. the same parameters that are automatically created in the __init__ method. If user specifies these then they'll
		be used instead of what's done in the __init__ method to create them.
		'''
		return Transaction(**transaction_json) #this ** trick basically pulls the dictionary values from transaction_json

	@staticmethod
	def is_valid_transaction(transaction):
		'''
		Validate a transaction
		Raise an exception for invalid transactions
		'''
		if transaction.input == MINING_REWARD_INPUT:
			if list(transaction.output.values()) != [MINING_REWARD]:
				raise Exception('Invalid mining reward')
			return  #don't want to go through the below code if we're looking at a mining transaction 


		output_total = sum(transaction.output.values())

		if transaction.input["amount"] != output_total:
			raise Exception("Invalid transaction output values")

		if not Wallet.verify(
			transaction.input["public_key"],
			transaction.output,
			transaction.input['signature']
		):
			raise Exception("Invalid signature")

	@staticmethod
	def reward_transaction(miner_wallet):
		'''
		Generate a reward transaction that rewards the miner
		'''
		output = {}
		output[miner_wallet.address] = MINING_REWARD

		return Transaction(input=MINING_REWARD_INPUT, output=output)


def main():
	transaction = Transaction(Wallet(), 'recipient', 25)
	print(f'transaction.__dict__ : {transaction.__dict__}')

	transaction_json = transaction.to_json()
	restored_transaction = Transaction.from_json(transaction_json)
	print(f'restored_transaction.__dict__: {restored_transaction.__dict__}')

if __name__ == '__main__':
	main()