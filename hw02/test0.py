
import sys
from BitVector import *

bv = BitVector(filename = "input.txt")
 
bv1 = bv.read_bits_from_file(64)
while bv1:

	#print bv1
	#print bv1.size
	temp = bv1.get_hex_string_from_bitvector()
	while len(temp) < 16:
		temp = temp + "00"
	bv1 = BitVector(hexstring = temp)
	print bv1
	print bv1.size
	
	bv1 = bv.read_bits_from_file(64)
