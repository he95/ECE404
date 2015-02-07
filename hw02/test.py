import sys
from BitVector import *

with open('s-box-tables.txt') as f:
    s_box = []
    sboxline = f.readline()
    while sboxline:
    		#print sboxline
        if len(sboxline.split()) == 16:
        	s_box.append([int(x) for x in sboxline.split()])	
       	sboxline = f.readline()
        	
#split the s box arrays from the text file
#print arrays
print s_box


#def get_encryption_key(): # key                                                              
print s_box[4][1]
