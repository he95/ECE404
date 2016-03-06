# ECE 404
# Guanshi He
# Hw06

import sys
from BitVector import *
from PrimeGenerator import PrimeGenerator
e = 65537
#gcd function
def gcd(a,b):
	while b:
		a,b = b, a%b
	return a

#CRT function
def CRT(num,exp,p,q,n):
	Vp = pow(num,exp,p)
	Vq = pow(num,exp,q)
	Xp = q * int(BitVector(intVal = q).multiplicative_inverse(BitVector(intVal = p)))
	Xq = p * int(BitVector(intVal = p).multiplicative_inverse(BitVector(intVal = q)))
	return (Vp*Xp+Vq*Xq) % n

#function for encryption
def encrypt(input_name, output_name):
	
	input_block = []
	bv = BitVector(filename = input_name)
	#read the input data
	while bv.more_to_read:
		#read 128 bits data block for encryption each time
		data_block = bv.read_bits_from_file(128)
		while len(data_block) < 128 :
			data_block += BitVector(textstring = "\n")
		data_block.pad_from_left(128)
		input_block.append(int(data_block))

	#encrypt the input data
	#generate p and q values with requirements
	while 1:
		p = PrimeGenerator(bits = 128, debug = 0).findPrime()
		q = PrimeGenerator(bits = 128, debug = 0).findPrime()
		pvec = BitVector(intVal = p)
		qvec = BitVector(intVal = q)
		if (p != q) and (pvec[0:2] == qvec[0:2] == BitVector(intVal = 3)) and (gcd(p-1,e) == 1) and (gcd(q-1,e) == 1):
			break
	#calculate the value of n and its totient
	n = p * q
	totient = (p - 1) * (q - 1)
	file_temp = open("key.txt","w+")
	file_temp.write(str(p) + " " + str(q) + "\n")
	file_temp.close()
	output_block = []
	#encrypt the input blocks
	for blocks in input_block:
		output_block.append(CRT(blocks,e,p,q,n))
	fo = open(output_name,'w')
	#output the encrpted to the
	print "p = ",p
	print "q = ",q
	for blocks in output_block:
		tempvec = BitVector(intVal = blocks,size = 256)
		print tempvec.get_hex_string_from_bitvector()
		fo.write(tempvec.getTextFromBitVector())

	fo.close()

def decrypt(input_name,output_name):
	input_block = []
	bv = BitVector(filename = input_name)
	while bv.more_to_read:
		data_block = bv.read_bits_from_file(256)
		input_block.append(int(data_block))
	output_block = []
	file_temp = open("key.txt","r")
	keyline = file_temp.readline()
	file_temp.close()
	p,q = int(keyline.split()[0]),int(keyline.split()[1])
	n = p * q
	totient = (p - 1) * (q - 1)
	d = int(BitVector(intVal = e).multiplicative_inverse(BitVector(intVal = totient)))
	print "d = ",d
	for blocks in input_block:
		output_block.append(CRT(blocks,d,p,q,n))

	fout = open(output_name,"wb")
	for blocks in output_block:
		tempvec = BitVector(intVal = blocks,size = 128)
		fout.write(tempvec.getTextFromBitVector())
	fout.close()
		


def main():

	if(len(sys.argv) != 4):
		print "Usage: "
		print "Encryption: He_RSA_hw06.py -e message.txt output.txt"
		print "Decryption: He_RSA_hw06.py -d output.txt decrypted.txt"
		sys.exit()

	if sys.argv[1] == '-e':
		encrypt(sys.argv[2],sys.argv[3])
	elif sys.argv[1] == '-d':
		decrypt(sys.argv[2],sys.argv[3])
	else:
		print "Usage: "
		print "Encryption: He_RSA_hw06.py -e message.txt output.txt"
		print "Decryption: He_RSA_hw06.py -d output.txt decrypted.txt"
		sys.exit()

if __name__ == "__main__":
	main()



#################################################
# ##encrpted text
# p =  294714094900571307476996120169764765171
# q =  320192898958842090098127553043547379999
# 3WÍõ UË'šÉö¿ƒÇïÖCOÉéùGi[ò%™aK	„{uÊ^!æç-#/c›éÕò£©Z@çÏo×¿+Å÷å¯’†ü&œ]ªà~ëlàAÊp“1÷äD„·¤bV4jSÜ{w„ab«µæ/Àë@ÀEh[KêÝ0hDƒ}íÓÆcÒÛ@{¶5œ£{;ÃiM}1x}<1âZq«I+¼Ý†7*Ã=ü¤h•é€ªÌ[µ%~UâÕë`úèËj2 ðH€ûírLá7ë]Y)-¼°³7Ñ
# EˆÁš-¬}	si¥ÚºÝ@ÖXƒGâ–ºÜn/¬¤üS]Äp¿cp…’¶.ÓÄKIÄÎaRiË81¡/Øl„wŽ¨ôÇ‹{=«Ù6XÛßÔ÷ÏZkÚ"W.ŒFoÏtA¯r

#  ##decrypted text
# d =  45619691378576980086268624381683192995548793601542636385898405809416684283413
# hex 
# 3357cdf5a055cb279ac9f6bf83c7efd681434fc9e9f947695bf2132599610715
# 4b09847b75ca5e21e6e72d232f08639b0ee9d5819df2a3a95a40e7cf6fd7bf2b
# c50ff7e5af9286fc0c1c269c5daae07eeb6ce041ca7093317ff7e44484b7a462
# 56346a53dc7b77846162abb5e62fc0eb40c045685b4beadd30688144837dedd3
# c663d2db18407bb6359ca37b1d3b0fc3694d147d3106787d3c31e25a71ab492b
# bcdd86371b2ac33dfca41c6895e980aacc5bb5257e5515e2d5eb60fae8cb6a32
# a0f04880fbed724ce137eb5d59292dbcb0b337d10a4590881502c19a2d18ac7d
# 091d7369a5daba0edd1340d6588347e296ba8fdc6e2fac1a1aa4fc535dc470bf
# 8f63708592b62ed3c44b49c4ce61011d5269cb3831a12f07d89d1c6c84778e18
# a8f4c78b7b3dabd93658dbdfd402f7cf5a6bda22572e8c46136fcf7441af0872
#ascii
# The time has come to talk of many things: of shoes and ships and sealing-wax of cabbages and kings and why the sea is boiling hot and whether pigs have wings.

# GUANSHIs-MacBook-Pro:hw06 Rio$ diff decrypted.txt message.txt 


