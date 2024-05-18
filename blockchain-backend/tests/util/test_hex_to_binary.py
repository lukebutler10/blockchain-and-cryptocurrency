from backend.util.hex_to_binary import hex_to_binary

def test_hex_tto_binary():
	original_number = 789
	hex_number = hex(original_number)[2:] #slice from pos'n 2 because Python adds a "0x" at start of hexadecimal no's
	binary_number = hex_to_binary(hex_number)

	assert int(binary_number, 2) == original_number
	