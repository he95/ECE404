# Guanshi He
# ECE 404
# Hw 07
# SHA-512 implementation

from BitVector import *
import sys


def main():
	
	#initialization
	h0 = BitVector(hexstring='6a09e667f3bcc908')
	h1 = BitVector(hexstring='bb67ae8584caa73b')
	h2 = BitVector(hexstring='3c6ef372fe94f82b')
	h3 = BitVector(hexstring='a54ff53a5f1d36f1')
	h4 = BitVector(hexstring='510e527fade682d1')
	h5 = BitVector(hexstring='9b05688c2b3e6c1f')
	h6 = BitVector(hexstring='1f83d9abfb41bd6b')
	h7 = BitVector(hexstring='5be0cd19137e2179')
	K = [BitVector(hexstring='428a2f98d728ae22'), BitVector(hexstring='7137449123ef65cd'), BitVector(hexstring='b5c0fbcfec4d3b2f'), BitVector(hexstring='e9b5dba58189dbbc'), BitVector(hexstring='3956c25bf348b538'), BitVector(hexstring='59f111f1b605d019'), BitVector(hexstring='923f82a4af194f9b'), BitVector(hexstring='ab1c5ed5da6d8118'), BitVector(hexstring='d807aa98a3030242'), BitVector(hexstring='12835b0145706fbe'), BitVector(hexstring='243185be4ee4b28c'), BitVector(hexstring='550c7dc3d5ffb4e2'), BitVector(hexstring='72be5d74f27b896f'), BitVector(hexstring='80deb1fe3b1696b1'), BitVector(hexstring='9bdc06a725c71235'), BitVector(hexstring='c19bf174cf692694'), BitVector(hexstring='e49b69c19ef14ad2'), BitVector(hexstring='efbe4786384f25e3'), BitVector(hexstring='0fc19dc68b8cd5b5'), BitVector(hexstring='240ca1cc77ac9c65'), BitVector(hexstring='2de92c6f592b0275'), BitVector(hexstring='4a7484aa6ea6e483'), BitVector(hexstring='5cb0a9dcbd41fbd4'), BitVector(hexstring='76f988da831153b5'), BitVector(hexstring='983e5152ee66dfab'), BitVector(hexstring='a831c66d2db43210'), BitVector(hexstring='b00327c898fb213f'), BitVector(hexstring='bf597fc7beef0ee4'), BitVector(hexstring='c6e00bf33da88fc2'), BitVector(hexstring='d5a79147930aa725'), BitVector(hexstring='06ca6351e003826f'), BitVector(hexstring='142929670a0e6e70'), BitVector(hexstring='27b70a8546d22ffc'), BitVector(hexstring='2e1b21385c26c926'), BitVector(hexstring='4d2c6dfc5ac42aed'), BitVector(hexstring='53380d139d95b3df'), BitVector(hexstring='650a73548baf63de'), BitVector(hexstring='766a0abb3c77b2a8'), BitVector(hexstring='81c2c92e47edaee6'), BitVector(hexstring='92722c851482353b'), BitVector(hexstring='a2bfe8a14cf10364'), BitVector(hexstring='a81a664bbc423001'), BitVector(hexstring='c24b8b70d0f89791'), BitVector(hexstring='c76c51a30654be30'), BitVector(hexstring='d192e819d6ef5218'), BitVector(hexstring='d69906245565a910'), BitVector(hexstring='f40e35855771202a'), BitVector(hexstring='106aa07032bbd1b8'), BitVector(hexstring='19a4c116b8d2d0c8'), BitVector(hexstring='1e376c085141ab53'), BitVector(hexstring='2748774cdf8eeb99'), BitVector(hexstring='34b0bcb5e19b48a8'), BitVector(hexstring='391c0cb3c5c95a63'), BitVector(hexstring='4ed8aa4ae3418acb'), BitVector(hexstring='5b9cca4f7763e373'), BitVector(hexstring='682e6ff3d6b2b8a3'), BitVector(hexstring='748f82ee5defb2fc'), BitVector(hexstring='78a5636f43172f60'), BitVector(hexstring='84c87814a1f0ab72'), BitVector(hexstring='8cc702081a6439ec'), BitVector(hexstring='90befffa23631e28'), BitVector(hexstring='a4506cebde82bde9'), BitVector(hexstring='bef9a3f7b2c67915'), BitVector(hexstring='c67178f2e372532b'), BitVector(hexstring='ca273eceea26619c'), BitVector(hexstring='d186b8c721c0c207'), BitVector(hexstring='eada7dd6cde0eb1e'), BitVector(hexstring='f57d4f7fee6ed178'), BitVector(hexstring='06f067aa72176fba'), BitVector(hexstring='0a637dc5a2c898a6'), BitVector(hexstring='113f9804bef90dae'), BitVector(hexstring='1b710b35131c471b'), BitVector(hexstring='28db77f523047d84'), BitVector(hexstring='32caab7b40c72493'), BitVector(hexstring='3c9ebe0a15c9bebc'), BitVector(hexstring='431d67c49c100d4c'), BitVector(hexstring='4cc5d4becb3e42b6'), BitVector(hexstring='597f299cfc657e2a'), BitVector(hexstring='5fcb6fab3ad6faec'), BitVector(hexstring='6c44198c4a475817')]

	
	if len(sys.argv) != 2:
		sys.stderr.write("Usage : %s <input file to be hashed> \n" % sys.argv[0])
		sys.exit(1)

	filename = sys.argv[1]
	input_file = open(filename,'r')
	text = input_file.read()
	input_file.close()
	'''
	for item in K:
		print item.get_hex_string_from_bitvector()
	'''

	bv = BitVector(textstring = text)
	length = bv.length()
	bv1 = bv + BitVector(bitstring = '1')
	length1 = bv1.length()
	howmanyzeros = (896 - length1) % 1024
	zerolist = [0] * howmanyzeros

	bv4 = bv1 + BitVector(bitlist = zerolist) + BitVector(intVal = length, size = 128)
	#print bv4.get_hex_string_from_bitvector()
	words = [None] * 80

	for n in range(0,bv4.length(),1024):
		block = bv4[n:n+1024]
		words[0:16] = [block[i:i+64] for i in range (0,1024,64)]
		for i in range(16,80):
			# circular right shift of the 64 bits arg by n bits
			arg1 = words[i - 15]
			arg2 = words[i - 2]
			theta0 = ((arg1.deep_copy() >> 1) ^ (arg1.deep_copy() >> 8) ^ (arg1.deep_copy().shift_right(7)))
			theta1 = ((arg2.deep_copy() >> 19) ^ (arg2.deep_copy() >> 61) ^ (arg2.deep_copy().shift_right(6)))
			words[i] = BitVector(intVal = (int(words[i-16]) + int(theta0) + int(words[i - 7]) + int(theta1)) % (2 ** 64),size = 64)

			a,b,c,d,e,f,g,h = h0,h1,h2,h3,h4,h5,h6,h7

		for i in range(80):
			sum_a = ((a.deep_copy()) >> 28) ^ ((a.deep_copy()) >> 34) ^ ((a.deep_copy()) >> 39)
			sum_e = ((e.deep_copy()) >> 14) ^ ((e.deep_copy()) >> 18) ^ ((e.deep_copy()) >> 41)
			ch = (e & f) ^ ((~e) & g)
			maj = (a & b) ^ (a & c) ^ (b & c)
			T_1 = BitVector(intVal = (int(h) + int(ch) + int(sum_e) + int(words[i]) + int(K[i])) % (2**64),size = 64)
			T_2 = BitVector(intVal = (int(sum_a) + int(maj)) % (2**64),size = 64)

			h = g
			g = f
			f = e
			e = BitVector(intVal = (int(d) + int(T_1)) % (2**64),size = 64)
			d = c
			c = b
			b = a
			a = BitVector(intVal = (int(T_1) + int(T_2)) % (2**64),size = 64)

		h0 = BitVector( intVal = (int(h0) + int(a)) % (2**64), size=64 )
		h1 = BitVector( intVal = (int(h1) + int(b)) % (2**64), size=64 )
		h2 = BitVector( intVal = (int(h2) + int(c)) % (2**64), size=64 )
		h3 = BitVector( intVal = (int(h3) + int(d)) % (2**64), size=64 )
		h4 = BitVector( intVal = (int(h4) + int(e)) % (2**64), size=64 )
		h5 = BitVector( intVal = (int(h5) + int(f)) % (2**64), size=64 )
		h6 = BitVector( intVal = (int(h6) + int(g)) % (2**64), size=64 )
		h7 = BitVector( intVal = (int(h7) + int(h)) % (2**64), size=64 )

	message_hash = h0+h1+h2+h3+h4+h5+h6+h7
	hash_hex_string = message_hash.get_hex_string_from_bitvector()
	fo = open("output.txt","w+")
	fo.write(hash_hex_string)
	fo.close()


if __name__ == "__main__":
	main()


# Test of code
# Text message of my choice
# A hungry brown fox jumped over a lazy dog
# Hash value
# d9755131b3c9c9f2903c51c62800ce320dde74035875265bc9311e11ff24a615f7bb890691ed34539b9cec80d57406fed608bf3d36044f3823c49adbcc175944
