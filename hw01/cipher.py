#Guanshi He
#ECE404 Hw01
#cipher.py

letter_list = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'  
#get the list of litters for future use

keyfo = open("key.txt","r+")  #open the key text file
keystring = keyfo.readline()  #read the key test
key_length = len(keystring) - 1  #get the length of the key

key_list = []  #declaration for the key list
for ch in keystring:
	if ch == "\n" :
		break
	key_list.append(ord(ch.upper()) - 65)
	#convert the key letters to number index
keyfo.close()  

plaintextfo = open("input.txt","r+")  #open the plaintext file
ciphertext = ""	#declaration for the cipher text
line = plaintextfo.readline() #read the plaintext
while line:
	i = 0  #index for looping
	for ch in line:
		if ch == "\n":
			break

		if i % key_length == 0:
			i = 0  #reset the loop index

		if ch.isupper():
			ciphertext += letter_list[(ord(ch) - 65 + key_list[i]) % 26]  
			#calculate the ciphertext letter for upper letter plaintext
			i = i + 1 #update the loop index
			#print ciphertext
		else:
			
			ciphertext += letter_list[(ord(ch) - 97 + key_list[i]) % 26].upper()
			#calculate the ciphertext letter for lowert case plaintext
			i = i + 1 #update the loop index
			#print ciphertext
	
	line = plaintextfo.readline()
	#read the next line of plaintext

plaintextfo.close()

outputfo = open("output.txt","w")  #open the output file
outputfo.writelines(ciphertext)  #write the cipher text to the output file
outputfo.close()
	#print "ciphertext",ciphertext


# Sample #1
# plaintext canyoumeetmeatmidnightihavethegoods
# key abracadabra
# ciphertext CBEYQUPEFKMEBKMKDQIHYTIIRVGTKEHFODT

# Sample #2
# plaintext AaZzAa
# key aaazzz
# ciphertext AAZYZZ

# Sample #3
# plaintext nowyouseeme
# key abcdef
# ciphertext NPYBSZSFGPI
#original output for abcdabcd
#111100001011111000100110001010111111001101010110
#Cӻf???





























