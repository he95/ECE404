#!/usr/local/bin/python

### Created by Zaiwei Zhang
### This script implements AES encryption algorithm.

import sys
from BitVector import*

filein = "plaintext.txt"
fout1 = "encryptedtext.txt"
fout2 = "decryptedtext.txt"
colmixE = [[2,3,1,1],[1,2,3,1],[1,1,2,3],[3,1,1,2]]
colmixD = [[14,11,13,9],[9,14,11,13],[13,9,14,11],[11,13,9,14]]
modulus = BitVector(bitstring='100011011')
zero = BitVector(bitstring='00000000')
c = BitVector(bitstring='01100011')
d = BitVector(bitstring='00000101')
round_constant = [1, 2, 4, 8, 16, 32, 64]

def g(key_piece, r):
    key_piece = key_piece << 8
    for i in range(4):
        key_piece[i*8:(i*8+8)] = encryptable[int(key_piece[i*8:(i*8+4)])][int(key_piece[(i*8+4):(i*8+8)])]
    constant = BitVector(size=32)
    constant[0:8] = BitVector(intVal=round_constant[r], size=8)
    return key_piece^constant
    
def generatekey(key):
    key_list = [key]
    for i in range(7):
        temp = BitVector(size=256)
        temp[0:32] = (key_list[i][0:32]) ^ (g(key_list[i][224:256], i)) 
        temp[32:64] = (temp[0:32]) ^ (key_list[i][32:64])
        temp[64:96] = (temp[32:64]) ^ (key_list[i][64:96])
        temp[96:128] = (temp[64:96]) ^ (key_list[i][96:128])
        temp1 = temp[96:128]
        temp2 = BitVector(size=32)
        for j in range(4):
            temp2[j*8:(j*8+8)] = encryptable[int(temp1[j*8:(j*8+4)])][int(temp1[(j*8+4):(j*8+8)])]
        temp[128:160] = (temp2) ^ (key_list[i][128:160])
        temp[160:192] = (temp[128:160]) ^ (key_list[i][160:192])
        temp[192:224] = (temp[160:192]) ^ (key_list[i][192:224])
        temp[224:256] = (temp[192:224]) ^ (key_list[i][224:256])
        tempp = BitVector(bitstring=str(temp))
        key_list.append(tempp)
    keylist = []
    for i in range(8):
        temp1,temp2 = key_list[i].divide_into_two()
        keylist.append(temp1)
        keylist.append(temp2)
    return keylist

def generateTableEncrypt():
    table = [[0 for n in range(16)] for m in range(16)]
    temp = BitVector(size=8)
    for i in range(16):
        for j in range(16):
            temp[0:4] = BitVector(intVal=i,size=4)
            temp[4:8] = BitVector(intVal=j,size=4)
            if temp == zero:
                inverse = temp
            else:
                inverse = temp.gf_MI(modulus, 8)
            tempp = BitVector(size=8)
            for k in range(8):
                tempp[k] = inverse[k] ^ inverse[(k-4)%8] ^ inverse[(k-5)%8] ^ inverse[(k-6)%8] ^ inverse[(k-7)%8] ^ c[k]
            table[i][j] = tempp
    return table

def generateTableDecrypt():
    table = [[0 for n in range(16)] for m in range(16)]
    temp = BitVector(size=8)
    for i in range(16):
        for j in range(16):
            temp[0:4] = BitVector(intVal=i,size=4)
            temp[4:8] = BitVector(intVal=j,size=4)
            tempp = BitVector(size=8)
            for k in range(8):
                tempp[k] = temp[(k-2)%8] ^ temp[(k-5)%8] ^ temp[(k-7)%8] ^ d[k]
            if tempp == zero:
                inverse = BitVector(size=8)
            else:
                inverse = tempp.gf_MI(modulus, 8)
            table[i][j] = inverse
    return table

def encrypt(key_list):
    fout = open(fout1, 'wb+')
    bv = BitVector( filename = filein )
    subbyte = encryptable
    while (bv.more_to_read):
        bitvec = bv.read_bits_from_file( 128 )
        if len(bitvec) != 128:
            bitvec.pad_from_right(128 - len(bitvec))
        if len(bitvec) == 128:
            bitvec = bitvec ^ key_list[0]
            for i in range(14):
                #look up the table
                for j in range(16):
                    bitvec[8*j:(8*j+8)] = subbyte[int(bitvec[8*j:(8*j + 4)])][int(bitvec[(8*j + 4):(8*j + 8)])]
                #shift row
                for m in range(3):
                    for fan in range(m+1):
                        temp = BitVector( bitstring=str(bitvec[8*(m+1):(8*(m+2))]) )
                        for j in range(3):
                            bitvec[(32*j+8*(m+1)):(32*j+8*(m+2))] = bitvec[(32*(j+1)+8*(m+1)):(32*(j+1)+8*(m+2))] 
                        bitvec[(32*3+8*(m+1)):(32*3+8*(m+2))] = temp
                #mix columns
                if i != 13:
                    tempout = BitVector(size=128)
                    for k in range(4):
                        for j in range(4):
                            tempbyte = BitVector( size=8 )
                            for l in range(4):
                                tempmultiply2 = bitvec[(32*j+l*8):(32*j+(l+1)*8)] 
                                tempmultiply1 = BitVector( intVal= colmixE[k][l], size=8)
                                tempbyte = tempbyte ^ (tempmultiply1.gf_multiply_modular(tempmultiply2, modulus, 8))                
                            tempout[(32*j+8*k):(32*j+8*(k+1))] = BitVector(bitstring=str(tempbyte))
                    bitvec = BitVector(bitstring=str(tempout))
                #add with round key
                bitvec = bitvec ^ key_list[i+1]
        fout.write(bitvec.getTextFromBitVector())
    fout.close()
        
def decrypt(key_list):
    fout = open(fout2, 'wb+')
    bv = BitVector( filename = fout1 )
    subbyte = decryptable
    while (bv.more_to_read):
        bitvec = bv.read_bits_from_file( 128 )
        if len(bitvec) != 128:
            bitvec.pad_from_right(128 - len(bitvec))
        if len(bitvec) == 128:
            bitvec = bitvec ^ key_list[14]
            for i in range(14):
                #shift row
                for m in range(3):
                    for fan in range(m+1):
                        temp = BitVector( bitstring=str(bitvec[(32*3 + 8*(m+1)):(32*3+(8*(m+2)))]) )
                        for j in range(3):
                            j = 3 - j
                            bitvec[(32*j+8*(m+1)):(32*j+8*(m+2))] = bitvec[(32*(j-1)+8*(m+1)):(32*(j-1)+8*(m+2))] 
                        bitvec[(8*(m+1)):(8*(m+2))] = temp
                #look up the table
                for j in range(16):
                    #print subbyte[int(bitvec[8*j:(8*j + 4)])][int(bitvec[(8*j + 4):(8*j + 8)])]
                    bitvec[8*j:(8*j+8)] = subbyte[int(bitvec[8*j:(8*j + 4)])][int(bitvec[(8*j + 4):(8*j + 8)])]
                #add with round key
                bitvec = bitvec ^ key_list[13 - i]
                #mix columns
                if i != 13:
                    tempout = BitVector(size=128)
                    for k in range(4):
                        for j in range(4):
                            tempbyte = BitVector( size=8 )
                            for l in range(4):
                                tempmultiply2 = bitvec[(32*j+l*8):(32*j+(l+1)*8)] 
                                tempmultiply1 = BitVector( intVal= colmixD[k][l], size=8)
                                tempbyte = tempbyte ^ (tempmultiply1.gf_multiply_modular(tempmultiply2, modulus, 8))                
                                tempout[(32*j+8*k):(32*j+8*(k+1))] = BitVector(bitstring=str(tempbyte))
                    bitvec = BitVector(bitstring=str(tempout))
        fout.write(bitvec.getTextFromBitVector())
    fout.close()

def main():
    raw_key = raw_input("Please Enter the Encryption key: ")
    key = BitVector(textstring = raw_key)
    key_list = generatekey(key)
    encrypt(key_list)
    decrypt(key_list)

encryptable = generateTableEncrypt()
decryptable = generateTableDecrypt()

if __name__ == "__main__":
    main()