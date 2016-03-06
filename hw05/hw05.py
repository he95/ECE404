# ECE 404
# Hw 05
# Guanshi He

from BitVector import *


class RC4:
	def __init__(self,key):
		#initialize the state vector
		S_box = [x for x in range(256)]
		key_bv = BitVector(textstring = key)
		key_length = len(key)
		#print "key_length = ",key_length
		K_vector = []
		i = 0
		
		#initialize the K vector
		while(i < key_length):
			#temp = BitVector(textstring = key[i])
			K_vector.append(ord(key[i]))
			i = i + 1
			#print int(temp)
		T_vector = []

		#initialize the T vector
		for i in range(256):
			T_vector.append(K_vector[i % key_length])
			#print T_vector[i]
		#permutation
		j = 0
		for i in range(256):
			j = (j + S_box[i] + T_vector[i]) % 256
			temp_vector = S_box[i]
			S_box[i] = S_box[j]
			S_box[j] = temp_vector
			#print "s_box[",i,"]=",S_box[i]
		self.S = S_box

	#call the core encrypt function
	def encrypt(self, image):
		self.core(image, 'encrypted.ppm')
	#call the core decrypt function
	def decrypt(self, image):
		self.core(image, 'decrypted.ppm')
	#core function
	def core(self, filein, fileout):
		fi = open(filein,"r")
		output = [fi.readline() for i in range(5)]
		temp = self.S
		i,j = 0,0
		byte = 0
		while(1):
		#	print fi.tell()
			r = fi.read(1)
			if r == '':
				break
			i = (i + 1) % 256
			j = (j + temp[i]) % 256
			temp[i],temp[j] = temp[j],temp[i]
			k = (temp[i] + temp[j]) % 256
			output.append(chr(temp[k] ^ ord(r)))

		#output the image data to the file
		fo = open(fileout,"w")
		fo.writelines(output)

def main():
	rc4Cipher = RC4('keystring')
	rc4Cipher.encrypt('Tiger2.ppm')
	rc4Cipher = RC4('keystring')
	rc4Cipher.decrypt('encrypted.ppm')

if __name__ == "__main__":
    main()
