# Guanshi He
# ECE 404
# Hw06 Part 2 BreakRSA
from solve_pRoot import *
from BitVector import *
from He_RSA_hw06 import *

def main():
	e = 3
	key = []
	output = [[],[],[]]

	for i in range(3):
		input_block = []
		bv = BitVector(filename = "message.txt")
		#read the input data
		while bv.more_to_read:
			#read 128 bits data block for encryption each time
			data_block = bv.read_bits_from_file(128)
			while len(data_block) < 128 :
				data_block += BitVector(textstring = "\n")
			data_block.pad_from_left(128)
			input_block.append(int(data_block))

		while 1:
			p = PrimeGenerator(bits = 128, debug = 0).findPrime()
			q = PrimeGenerator(bits = 128, debug = 0).findPrime()
			pvec = BitVector(intVal = p)
			qvec = BitVector(intVal = q)
			if (p != q) and (pvec[0:2] == qvec[0:2] == BitVector(intVal = 3)) and (gcd(p-1,e) == 1) and (gcd(q-1,e) == 1):
				break
		n = p * q
		totient = (p - 1) * (q - 1)
		t_bv = BitVector(intVal = totient)
		e_bv = BitVector(intVal = e)
		d = int(e_bv.multiplicative_inverse(t_bv))

		key.append([e,n,p,q,d])
		print key[i]
		output_block = []
		for blocks in input_block:
			output_block.append(CRT(blocks,e,p,q,n))

		output_name = "encrpted" + str(i) + ".txt"
		fo = open(output_name,'w')
		#output the encrpted to the
		for blocks in output_block:
			tempvec = BitVector(intVal = blocks,size = 256)
			#print tempvec.get_hex_string_from_bitvector()
			output[i].append(tempvec.getTextFromBitVector())
			fo.write(tempvec.getTextFromBitVector())

	print key[0][1]
	print key[1][1]
	print key[2][1]
	N = key[0][1] * key[1][1] * key[2][1]
	N1 = N/key[0][1]
	N2 = N/key[1][1]
	N3 = N/key[2][1]
	d1 =int( BitVector(intVal = N1).multiplicative_inverse(BitVector(intVal = key[0][1])))
	d2 = int(BitVector(intVal = N2).multiplicative_inverse(BitVector(intVal = key[1][1])))
	d3 = int(BitVector(intVal = N3).multiplicative_inverse(BitVector(intVal = key[2][1])))
	
	M = output[0] * N1 * d1 + output[0] * N1 * d1

if __name__ == '__main__':
	main()