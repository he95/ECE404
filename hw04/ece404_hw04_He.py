# Guanshi He
# ECE 404
# Hw04
# AES encryption

import sys
from BitVector import *

file_input = "plaintext.txt"
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
	key = key << 8  #left shift
	new_key = BitVector(size = 0)
	#subBytes
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
	bv = BitVector(filename = file_input)
	#print "bv = ",bv
	#a = 1
	while(bv.more_to_read):
		block = bv.read_bits_from_file(128)
		#print "block = "
		if len(block) != 128:
			block.pad_from_right(128 - len(block))
		if len(block) == 128:
			block = block ^ (keylist[0]+keylist[1]+keylist[2]+keylist[3])
			for i in range(10):  # 10 rounds
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

				#print "=========after SubBytes=========="
				#print block.getHexStringFromBitVector()

				#shift rows
				for m in range(3):
					for fan in range(m+1):
						temp = BitVector( bitstring=str(block[8*(m+1):(8*(m+2))]) )
						for j in range(3):
							block[(32*j+8*(m+1)):(32*j+8*(m+2))] = block[(32*(j+1)+8*(m+1)):(32*(j+1)+8*(m+2))] 
						block[(32*3+8*(m+1)):(32*3+8*(m+2))] = temp

				#print "=========after shift rows=========="
				#print block.getHexStringFromBitVector()
				#Column mix

				'''if i != 9:
					tempout = BitVector(size=128)
					for k in range(4):
						for j in range(4):
							tempbyte = BitVector( size=8 )
							for l in range(4):
								tempmultiply2 = block[(32*j+l*8):(32*j+(l+1)*8)] 
								tempmultiply1 = BitVector( intVal= colmix_Encrpytion_table[k][l], size=8)
								tempbyte = tempbyte ^ (tempmultiply1.gf_multiply_modular(tempmultiply2, AES_modulus, 8))                
							tempout[(32*j+8*k):(32*j+8*(k+1))] = BitVector(bitstring=str(tempbyte))

							#print "====== after mix ====="
							#print tempout.getHexStringFromBitVector()
					block = BitVector(bitstring=str(tempout))
					'''
				#print "====== after mix ====="
				#print block.getHexStringFromBitVector
				#add round key
				block = block ^ (keylist[i*4+4]+keylist[i*4+5]+keylist[i*4+6]+keylist[i*4+7])
				#print block
		fout.write(block.getHexStringFromBitVector())
	fout.close()

def decrypt(keylist):

	fout = open(fo2,"wb+")
	fo1in = open(fo1,"r")
	print "fo1",fo1
	a = ''
	for line in fo1in:
		a += line
	print "readline", a
	bv = BitVector(hexstring = a)
	print "bv = ",bv
	fo1in.close()
	#convert hex string file to bitvector file

	f = open('encrypted_tmp.txt', 'w')
	f.write(bv.getTextFromBitVector())
	f.close()
	bv = BitVector(filename = 'encrypted_tmp.txt')
	while(bv.more_to_read):
		block = bv.read_bits_from_file(128)
		if len(block) != 128:
			block.pad_from_right(128 - len(block))
		if len(block) == 128:
			block = block^(keylist[40]+keylist[41]+keylist[42]+keylist[43])
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
					value = invSubBytesTable[row*16+col]
					block[j*8:j*8+8] = BitVector(intVal = value, size = 8)
				#add round key
				block = block ^ (keylist[(10-i)*4-4]+keylist[(10-i)*4-3]+keylist[(10-i)*4-2]+keylist[(10-i)*4-1])
				#mix columns
				if i != 9:
					tempout = BitVector(size = 128)
					for k in range(4):
						for j in range(4):
							tempbyte = BitVector( size=8 )
							for l in range(4):
								tempmultiply2 = block[(32*j+l*8):(32*j+(l+1)*8)] 
								tempmultiply1 = BitVector( intVal= colmix_Decryption_table[k][l], size=8)
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





###########################################################################
##plaintext 
#This is an unusual paragraph. I'm curious how quickly you can find out what is so unusual about it? It looks so plain you would think nothing was wrong with it! In fact, nothing is wrong with it? It is unusual though. Study it, and think about it, but you still may not find anything odd. But if you work at it a bit, you might find out! Try to do so without any coaching! You most probably won't, at first, find anothing particularly odd or unusual or in any way dissimilar to any ordianary composition. That is not at all surprising, for it is no strain to accomplish in so short a paragraph a stunt similar to that which an author did throughout all of his book, without spoiling a good writing job, and it was no small book at that.


##output for encryptedtext
# 36a1e63f6eab612e238bea74a8902338814d92c438faf83876ae308dca1d8073814480c79e3b5e79fed4c4b6711c781c518a2b8d4370759f6623a29d0f2d4aa714fb04b3f07ce9717e91557e611663482715cfdff4960593785ac1c5e93eaad8aa9daab34f2441da6257674b5ed013ed3a28a1d7a489ac47bfb1cfe0030f974f85500fd2c25f02d488ac48b74732e0feb5efe95fa8fb4caa7eb506b38c074ceb48ab2fab7be80dbad5b1c621b94d662a71ec24e0d813bad0178b9ca04cb5def74799f3bf8f01558ccf6348a4171d85a34fab4739e1155d27b080bb7fec665a3cfffcbdc16ef769825a05b8dc8ea05242240b8d2273e4a5ce17997ce56754a00554c3e3d0878b514ec269bbcf80d0c2568792fe72fefd7101b5152615a356fcb79a868fb799e6c44b1262902ce5a1a3cb4fdf14aaecce2225a258e660fbd6ecef105a386093c4ff9ca16579a6b626475a3494b59a27bab5840bf663cc849b714bae6cc8616434c7786d1f7cb0968ec7e800df30ae0cb4a0f5c1a1dacbec7f53c00e9401ebcc0e87fb78bd8265a3362322cf7956de957d9362c71030601cf2f5edd981b7e5c9cfecf02a3e6b234f3ddd097fb7294fb99548917a52bedc24a2faf61fdb8c60e9b70323243819f8e1577facf275a3b7322cf7f83fb46fad82cecb17134e4e48f379576107e1adf95ca2354a7aaa3bf611bf31b1cdfd8aeff92f0147761b2b2d618ac0f7dd305e3ee732659a53b2c43f2c09ccfb3ca6cdda74cf253598ab968f7b2e273dd7f4e90de3ec7c5c1144b55f06c0b198ef26db1130f0e525514676c131fad4b58dce546130288753e071b0d20958692ed9aad917d20bd737474672ea115621e437550e25619087227e6629d6cea4887063195d651d2f8e1c43ad80a182d9122ef867e4cd0613daa587b892c1927319a11e7826374644706c0eed12f41f5a527de727a7b18dcf7e8e13256b803c5aeca9045adbf9ee862a24660f8f7fd72242b0b8c7f7d4933d8d61bde3361c154c8296edc2a079efa738e3

##output for decryptedtext
# 