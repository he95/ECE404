#Guanshi He
#ECE 404
#Hw 02
#Full DES implementation

### hw2_starter.py

import sys
from BitVector import *

################################   Initial setup  ################################

# Expansion permutation (See Section 3.3.1):
expansion_permutation = [31, 0, 1, 2, 3, 4, 3, 4, 5, 6, 7, 8, 7, 8, 
9, 10, 11, 12, 11, 12, 13, 14, 15, 16, 15, 16, 17, 18, 19, 20, 19, 
20, 21, 22, 23, 24, 23, 24, 25, 26, 27, 28, 27, 28, 29, 30, 31, 0]

# P-Box permutation (the last step of the Feistel function in Figure 4):
p_box_permutation = [15,6,19,20,28,11,27,16,0,14,22,25,4,17,30,9,
1,7,23,13,31,26,2,8,18,12,29,5,21,10,3,24]

# Initial permutation of the key (See Section 3.3.6):
key_permutation_1 = [56,48,40,32,24,16,8,0,57,49,41,33,25,17,9,1,58,
50,42,34,26,18,10,2,59,51,43,35,62,54,46,38,30,22,14,6,61,53,45,37,
29,21,13,5,60,52,44,36,28,20,12,4,27,19,11,3]

# Contraction permutation of the key (See Section 3.3.7):
key_permutation_2 = [13,16,10,23,0,4,2,27,14,5,20,9,22,18,11,3,25,
7,15,6,26,19,12,1,40,51,30,36,46,54,29,39,50,44,32,47,43,48,38,55,
33,52,45,41,49,35,28,31]

# Each integer here is the how much left-circular shift is applied
# to each half of the 56-bit key in each round (See Section 3.3.5):
shifts_key_halvs = [1,1,2,2,2,2,2,2,1,2,2,2,2,2,2,1] 




###################################   S-boxes  ##################################

# Now create your s-boxes as an array of arrays by reading the contents
# of the file s-box-tables.txt:
with open('s-box-tables.txt') as f:
    s_box = []
    sboxline = f.readline()
    while sboxline:
            #print sboxline
        if len(sboxline.split()) == 16:
            s_box.append([int(x) for x in sboxline.split()])    
        sboxline = f.readline()
            

#######################  Get encryptin key from user  ###########################

def get_encryption_key(): # key                                                              
    ## ask user for input
    while 1:
        encrypt_key = raw_input("Enter an encryption key of at least 8 printable ASCII characters:")
    ## make sure it satisfies any constraints on the key
        if len(encrypt_key) == 8:
            break
        else:
            print("Invalid input for encryption key")
            print("Encryption key should consist of at least 8 printable ASCII characters")
    

    ## next, construct a BitVector from the key    
    user_key_bv = BitVector(textstring = encrypt_key)  
    #print user_key_bv

    key_bv = user_key_bv.permute(key_permutation_1)        ## permute() is a BitVector function
    #print key_bv
    return key_bv


################################# Generatubg round keys  ########################
def extract_round_key( nkey,i ): # round key                                                   
   
    [left,right] = nkey.divide_into_two()   ## divide_into_two() is a BitVector function
    left  << shifts_key_halvs[i]
    right << shifts_key_halvs[i]
    nkey = left + right
    round_key = nkey.permute(key_permutation_2)
         ## 
         ##  the rest of the code
         ##
    #print round_key
    return (nkey,round_key)



########################## encryption and decryption #############################

def des(encrypt_or_decrypt, key ,bitvec): 
    '''bv = BitVector( filename = input_file ) 
    FILEOUT = open( output_file, 'wb' ) 
    #bv = BitVector( filename = input_file )

    bitvec = bv.read_bits_from_file( 64 )   ## assumes that your file has an integral
                                            ## multiple of 8 bytes. If not, you must pad it.
                                            '''

    #print bitvec
    #[LE, RE] = bitvec.divide_into_two()      
    #round_key = extract_round_key(key)
    #if(encrypt_or_decrypt == 'encrypt'):

    round_key = [0]*16
    for i in range(16):
        key,round_key[i] = extract_round_key(key,i)
        #print round_key[i]
    for i in range(16):        
    ## write code to carry out 16 rounds of processing
        #round_key = extract_round_key(key)
        #perform the expansion permutation 32 bits to 48 bits
        [LE, RE] = bitvec.divide_into_two()  
        #key,round_key = extract_round_key(key,i)
        RE_new = RE.permute(expansion_permutation)
        #print("round key = {}".format(round_key))
        #perform the xor calculation 
        if(encrypt_or_decrypt == 'encrypt'):
            xor_result = RE_new ^ round_key[i]  #perform XOR when choice is encrypt
        elif(encrypt_or_decrypt == 'decrypt'):
            xor_result = RE_new ^ round_key[15 - i]  #perform XOR when choice is decrypt

        #print("xor_result = {}".format(xor_result))
        #substitution with 8 s-boxes
        RE_new2 = BitVector(size = 0)
        for j in range(8):
            #row_index = xor_result[j * 6] + xor_result[j * 6 + 5]
            row_index = BitVector(size = 2)
            row_index[0] = xor_result[j * 6]
            row_index[1] = xor_result[j * 6 + 5]
            column_index = xor_result[j*6+1:j*6+5]
            RE_new2 = RE_new2 + BitVector(intVal = (s_box[int(int(row_index) + 4*j)][int(column_index)]),size = 4)
        #permutation with p box            
        RE_final = RE_new2.permute(p_box_permutation)
        #xor with left half
        RE_final2 = RE_final ^ LE
        #cat the left side with the new right side  
        if i == 15:
            bitvec = RE_final2 + RE
        else:
            bitvec = RE + RE_final2
        
    #cat the encrypted text
    cipher_text = ''
    cipher_text = cipher_text + (str(bitvec))
    #print cipher_text
    #print bitvec.get_text_from_bitvector()
    cipher = bitvec.get_text_from_bitvector()
    '''fo = open(output_file,"wb")
    fo.writelines(cipher + '\n')  #write the cipher text to the output file
    fo.close()
    '''
    return bitvec



#################################### main #######################################
def main():
        
    ## write code that prompts the user for the key
    key = get_encryption_key()
    ## and then invokes the functionality of your implementation
    while 1:
        choice = raw_input("Please choose encrypt or decrypt: ")
        if (choice == 'encrypt') or (choice == 'decrypt'):
            break
        else:
            print("Please type in 'encrypt' or 'decrypt'")
    #implement the function DES
    fileinput = open("o11.txt")
    file_plaintext = fileinput.readline()
    input_text = ''
    while file_plaintext:
        print file_plaintext
        input_text += file_plaintext
        file_plaintext = fileinput.readline()
    #print output.get_text_from_bitvector()
    # print "length",len(input_text)
    
    if len(input_text) % 8 == 0: 
        output = BitVector(size = 0)
        for i in range(len(input_text) / 8):
            block = input_text[i*8:8+i*8]
            bitvec = BitVector(textstring = block)
            output += des(choice,key,bitvec)
            
        print output.get_text_from_bitvector()
    elif len(input_text) % 8 != 0:
        output = BitVector(size = 0)
        blocksize = len(input_text) / 8
        for i in range(blocksize - 1):
            block = input_text[i*8:8+i*8]
            bitvec = BitVector(textstring = block)
            output += des(choice,key,bitvec)
        block = input_text[(blocksize - 1) * 8:]
        bv1 = BitVector(textstring = block)
        temp = bv1.get_hex_string_from_bitvector()
        while len(temp) < 16:
            temp = temp + "00"
        bitvec = BitVector(hexstring = temp)
        output += des(choice,key,bitvec)
        print output.get_text_from_bitvector()
    fo = open("o12.txt","wb")
    fo.writelines(output.get_text_from_bitvector() + "\n")  #write the cipher text to the output file
    fo.close()
    '''
    else:
        if len(input_text) % 8 == 0: 
            output = BitVector(size = 0)
            for i in range(len(input_text) / 8):
                block = input_text[i*8:8+i*8]
                bitvec = BitVector(textstring = block)
                output += des(choice,key,bitvec)
                
            print output.get_text_from_bitvector()
        else:
            output = BitVector(size = 0)
            blocksize = len(input_text) / 8
            for i in range(blocksize - 1):
                block = input_text[i*8:8+i*8]
                bitvec = BitVector(textstring = block)
                output += des(choice,key,bitvec)
    '''
            
    
if __name__ == "__main__":
    main()




















