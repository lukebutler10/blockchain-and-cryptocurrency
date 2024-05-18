import hashlib
import json

def crypto_hash(*args):
	"""
	Return a sha-256 hash opf the given arguments
	"""
	stringified_args = sorted(map(lambda data:json.dumps(data),args))
#we use sorted so that the order of the inputs does affect the outputted hash value

	joined_data = "".join(stringified_args)

	return hashlib.sha256(joined_data.encode("utf-8")).hexdigest()

def main():
	print(f"crypto_hash('one',2,[3]):{crypto_hash('one',2,[3])}")
	print(f"crypto_hash(2,'one',[3]):{crypto_hash(2,'one',[3])}")

if __name__ == '__main__':
	main()

