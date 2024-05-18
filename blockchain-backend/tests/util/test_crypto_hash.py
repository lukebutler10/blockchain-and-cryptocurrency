from backend.util.crypto_hash import crypto_hash

def test_crypto_hash():
	assert crypto_hash(1,[2],"three") == crypto_hash("three",1,[2])
	#it should create the same hash with arguments of different data types in any order