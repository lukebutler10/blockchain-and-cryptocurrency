import pytest
import time

from backend.blockchain.block import Block, GENESIS_DATA
from backend.util.hex_to_binary import hex_to_binary
from backend.config import MINE_RATE, SECONDS

def test_min_block():
	last_block = Block.genesis()
	data = "test-data"
	block = Block.mine_block(last_block,data)

	assert isinstance(block,Block)
	assert block.data == data
	assert block.last_hash == last_block.hash
	assert hex_to_binary(block.hash)[:block.difficulty] == "0" * block.difficulty	

def test_genesis():
	genesis = Block.genesis()
 
	assert isinstance(genesis,Block) 
	for key, value in GENESIS_DATA.items():
		getattr(genesis,key) == value
		#this getattr function takes as its first parameter the object that you want to get the parameter from, and then the key here is the 
		#name of the attribute that we want the value of. If you look at the GENESIS_DATA dictionary in block.py you'll see how that works. 
		#And then we compare the output of this getattr function to the 'value' object to make sure it matches 


def test_quickly_mined_block():
	last_block = Block.mine_block(Block.genesis(), "foo")
	mined_block = Block.mine_block(last_block, "bar")
	#this block^ should be created in a short time, less than the MINE_RATE

	assert mined_block.difficulty == last_block.difficulty	+ 1 

def test_slowly_mined_block():
	last_block	= Block.mine_block(Block.genesis(), "foo")

	time.sleep(MINE_RATE/SECONDS) #note time.sleep takes its input in seconds
	mined_block	= Block.mine_block(last_block, "bar")

	assert mined_block.difficulty == last_block.difficulty	- 1
	

def test_mined_block_difficulty_limits_at_1():
	last_block = Block(
		time.time_ns(),
		"test_last_hash",
		"test_hash",
		"test_data",
		1, #setting the difficulty to 1
		0 #and nonce to 0

		)

	time.sleep(MINE_RATE/SECONDS)
	mined_block = Block.mine_block(last_block,"bar")

	assert mined_block.difficulty == 1



#these below are methods that we mark as fixtures. We use them when we will be calling the same thing multiple times when testing.
#We can then just call last_block and block in our test_is_valid_block tests a bit further down instead of repeatedly defining them

@pytest.fixture
def last_block():
	return Block.genesis()

@pytest.fixture
def block(last_block):
	return Block.mine_block(last_block, 'test_data') 


def test_is_valid_block(last_block, block):
	#this  test will ensure that a regular block that hasn't had any of it's fields tampered with is vaildated properly
	Block.is_valid_block(last_block, block)


#now we'll write 4 more tests, one to test each case of possible tampering with a block that we tackled in the is_valid_block method:

def test_is_valid_block_bad_last_hash(last_block, block):
	block.last_hash = 'evil_last_hash'

	#Next, this pytest method allows us to catch the errors in our code. The "match" argument takes a spcefic string which we will need to see in the exception message
	with pytest.raises(Exception, match= 'last_hash must be correct'):
		Block.is_valid_block(last_block, block)

def test_is_valid_bad_proof_of_work(last_block, block):
	block.hash = 'fff'

	with pytest.raises(Exception, match= 'proof of work requirement was not met'):
		Block.is_valid_block(last_block, block)

def test_is_valid_block_jumped_difficulty(last_block,block):
	jumped_difficulty = 10
	block.difficulty = jumped_difficulty
	block.hash = f'{"0" * jumped_difficulty}111abc'  

	with pytest.raises(Exception, match = 'difficulty must only adjust by 1'):
		Block.is_valid_block(last_block, block)
	#here we will trigger the part of the is_valid_block function that checks that the difficulty has not changed by > 1 compared to prev block
	#this is because the difficulty of genesis block is 3, and here thats the last_block. We've altered the difficulty of current block to
	#make it = 10. And we also change the hash value so that it matches the difficulty requirement. Then when is_valid_block checks that the 
	#difficulty hasnt changed by more than 1, it will see it's actually changed by 7. This would trigger an exception but we catch this with the
	#"with" statement. Thus no exception is raised. If you change the jumped_difficulty to 4 instead you will see that this test function fails
	#as the "match" string was not found in the message that we got, which was 'The block hash must be correct'
	#We use the "with" statement in our tests when we expect an Exception to be raised.

def test_is_valid_block_bad_block_hash(last_block,block):
	block.hash = '0000000000000000000000bbacd'  
	with pytest.raises(Exception, match = 'block hash must be correct'):
		Block.is_valid_block(last_block, block)

	#this block.hash should theoretically get passed the POW requirement as it has the neccessary amount of 0's. However it doesn't exactly 
	#match the hash value that would be outputted from our hash function when we input the fields that are in the "block" object.
