# Guanshi He
# ECE 404
# Hw04
# AES encryption

import sys
from BitVector import *

file_input = "plain.txt"
fo1 = "encryptedtext.txt"
fo2 = "decryptedtext.txt"
colmix_Encrpytion_table = [[2,3,1,1],[1,2,3,1],[1,1,2,3],[3,1,1,2]]
colmix_Decryption_table = [[14,11,13,9],[9,14,11,13],[13,9,14,11],[11,13,9,14]]
#round_constant = [1,2,4,8,16,32,64]


## gen_tables.py
## Avi Kak (February 15, 2015)
## This is the Python implementation of the explanation in Section 8.5.1 of Lecture
## 8. The goal here is to construct two 16x16 lookup tables for byte substitution,
## one for the SubBytes step of the AES algorithm, and the other for the InvSubBytes
## step.

AES_modulus = BitVector(bitstring='100011011')
subBytesTable = [] # SBox for encryption
invSubBytesTable = [] # SBox for decryption
def genTables():
	c = BitVector(bitstring='01100011')
	d = BitVector(bitstring='00000101')
	for i in range(0, 256):
	# For the encryption SBox
		a = BitVector(intVal = i, size=8).gf_MI(AES_modulus, 8) if i != 0 else BitVector(intVal=0)
		# For bit scrambling for the encryption SBox entries:
		a1,a2,a3,a4 = [a.deep_copy() for x in range(4)]
		a ^= (a1 >> 4) ^ (a2 >> 5) ^ (a3 >> 6) ^ (a4 >> 7) ^ c
		subBytesTable.append(int(a))
		# For the decryption Sbox:
		b = BitVector(intVal = i, size=8)
		# For bit scrambling for the decryption SBox entries:
		b1,b2,b3 = [b.deep_copy() for x in range(3)]
		b = (b1 >> 2) ^ (b2 >> 5) ^ (b3 >> 7) ^ d
		check = b.gf_MI(AES_modulus, 8)
		b = check if isinstance(check, BitVector) else 0
		invSubBytesTable.append(int(b))

####################################################################################

round_constant = [0] * 10
def find_RC():
	two = BitVector(intVal = 2,size = 8)
	#round_constant = [0] * 10
	round_constant[0] = BitVector(intVal = 1,size = 8)
	zerosbits = BitVector(intVal = 0, size = 24)
	
	for i in range(1,10):
		round_constant[i] = round_constant[i-1].gf_multiply_modular(two,AES_modulus,8)
		#round_constant[i] += zerosbits
		#print round_constant[i]
	for i in range(10):
		round_constant[i] = round_constant[i] + zerosbits
		#print round_constant[i]

def g_function(key,rc):
	key = key << 8
	new_key = BitVector(size = 0)
	for i in range(4):
		byte = key[i*8:i*8+8]
		left_bit = byte[0:4]
		right_bit = byte[4:8]
		row = int(left_bit)
		col = int(right_bit)
		# print "row",row
		# print "col",col
		
		newbyte = BitVector(intVal = subBytesTable[row*16+col], size = 8)
		new_key += newbyte
	#print new_key
	#print round_constant[rc]
	return new_key ^ round_constant[rc]



def key_expand(key_bv):

	w0 = key_bv[0:32]
	w1 = key_bv[32:64]
	w2 = key_bv[64:96]
	w3 = key_bv[96:128]
	#word_origin = [w0,w1,w2,w3]  #128 bits 16bytes
	keylist = [BitVector(size = 32) for x in range(44)]
	keylist[0:4] = [w0,w1,w2,w3]

	#temp = BitVector(size = 0)

	#print "========= schedule =========="
	#print (keylist[0] + keylist[1] +keylist[2]+keylist[3]).getHexStringFromBitVector()
	for i in range(1,11):
		temp0 = BitVector(size = 32)
		temp1 = BitVector(size = 32)
		temp2 = BitVector(size = 32)
		temp3 = BitVector(size = 32)

		g_value = g_function(w3,i-1)
		temp0 = g_value ^ w0
		temp1 = temp0 ^ w1
		temp2 = temp1 ^ w2
		temp3 = temp2 ^ w3

		w0 = temp0
		w1 = temp1
		w2 = temp2
		w3 = temp3

		keylist[i*4:i*8] = [w0,w1,w2,w3]

		#word_origin = temp
		#print (keylist[i*4]+keylist[i*4+1]+keylist[i*4+2]+keylist[i*4+3]).getHexStringFromBitVector()
	return keylist

def encrypt(keylist):
	#print keylist
	fout = open(fo1,'wb+')
	fi = open(file_input,'wb+')
	bv = BitVector(filename = file_input)
	a = 1
	print "input",bv
	while(a):#bv.more_to_read):
		a = 0
		block = BitVector(textstring = "abcdefghabcdefgh")#bv.read_bits_from_file(128)
		print "block = "
		if len(block) != 128:
			block.pad_from_right(128 - len(block))
		if len(block) == 128:
			block = block ^ (keylist[0]+keylist[1]+keylist[2]+keylist[3])
			for i in range(10):  # 10 rounds
				print "round = ",i
				# #SubBytes
				# print "before SubBytes"
				# print block

				for j in range(16):
					byte = block[j*8:j*8+8]
					left_bit = byte[0:4]
					right_bit = byte[4:8]
					row = int(left_bit)
					col = int(right_bit)
					#print "row",row
					#print "col",col
					value = subBytesTable[row*16+col]
					block[j*8:j*8+8] = BitVector(intVal = value, size = 8)

				print "=========after SubBytes=========="
				print block.getHexStringFromBitVector()

				#shift rows
				for m in range(3):
					for fan in range(m+1):
						temp = BitVector( bitstring=str(block[8*(m+1):(8*(m+2))]) )
						for j in range(3):
							block[(32*j+8*(m+1)):(32*j+8*(m+2))] = block[(32*(j+1)+8*(m+1)):(32*(j+1)+8*(m+2))] 
						block[(32*3+8*(m+1)):(32*3+8*(m+2))] = temp

				print "=========after shift rows=========="
				print block.getHexStringFromBitVector()
				#Column mix
				if i != 9:
					tempout = BitVector(size=128)
					for k in range(4):
						for j in range(4):
							tempbyte = BitVector( size=8 )
							for l in range(4):
								tempmultiply2 = block[(32*j+l*8):(32*j+(l+1)*8)] 
								tempmultiply1 = BitVector( intVal= colmix_Encrpytion_table[k][l], size=8)
								tempbyte = tempbyte ^ (tempmultiply1.gf_multiply_modular(tempmultiply2, AES_modulus, 8))                
							tempout[(32*j+8*k):(32*j+8*(k+1))] = BitVector(bitstring=str(tempbyte))

							print "====== after mix ====="
							print tempout.getHexStringFromBitVector()
					block = BitVector(bitstring=str(tempout))
				#print "====== after mix ====="
				#print block.getHexStringFromBitVector
				#add round key
				block = block ^ (keylist[i*4+4]+keylist[i*4+5]+keylist[i*4+6]+keylist[i*4+7])
				#print block
		fout.write(block.getTextFromBitVector())
	fout.close()

def decrypt(keylist):
	fout = open(fo2,"wb+")
	bv = BitVector(filename = fo1)
	while(bv.more_to_read):
		block = bv.read_bits_from_file(128)
		if len(block) != 128:
			block.pad_from_right(128 - len(block))
		if len(block) == 128:
			block = block^keylist[10]
			for i in range(10):
				#shift rows
				for m in range(3):
					for fan in range(m+1):
						temp = BitVector(bitstring = str(block[(32*3+8*(m+1)):(32*3+(8*(m+2)))]))
						for j in range(3):
							j = 3 - j
							block[(32*j+8*(m+1)):(32*j+8*(m+2))] = block[(32*(j-1)+8*(m+1)):(32*(j-1)+8*(m+2))] 
							block[(8*(m+1)):(8*(m+2))] = temp
				#look up the table
				for j in range(16):
					byte = block[j*8:j*8+8]
					left_bit = byte[0:4]
					right_bit = byte[4:8]
					row = int(left_bit)
					col = int(right_bit)
					#print "row",row
					#print "col",col
					value = subBytesTable[row*16+col]
					block[j*8:j*8+8] = BitVector(intVal = value, size = 8)
				#add round key
				block = block ^ keylist[10-i]
				#mix columns
				if i != 13:
					tempout = BitVector(size = 128)
					for k in range(4):
						for j in range(4):
							tempbyte = BitVector( size=8 )
							for l in range(4):
								tempmultiply2 = block[(32*j+l*8):(32*j+(l+1)*8)] 
								tempmultiply1 = BitVector( intVal= colmix_Encrpytion_table[k][l], size=8)
								tempbyte = tempbyte ^ (tempmultiply1.gf_multiply_modular(tempmultiply2, AES_modulus, 8))
							tempout[(32*j+8*k):(32*j+8*(k+1))] = BitVector(bitstring=str(tempbyte))
						block = BitVector(bitstring=str(tempout))
		fout.write(block.getTextFromBitVector())
	fout.close()



def main():
	encryption_key = 'lukeimyourfather'
	key_bv = BitVector(textstring = encryption_key)
	genTables()
	find_RC()
	keylist = key_expand(key_bv)
	#find_RC()
	#print keylist
	encrypt(keylist)
	decrypt(keylist)

if __name__ == '__main__':
	main()