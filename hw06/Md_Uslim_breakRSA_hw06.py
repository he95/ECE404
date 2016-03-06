#!usr/bin/env python
"""
Homework Number: 06
Name: Aiman Md Uslim
ECN Login: amduslim
Due Date: 3rd March 2015
"""
import sys
import random
from BitVector import *
# set e as a constant for all three sets of keys
e = 3
# sizes
modsize = 256
Bsize = modsize / 2
textsize = Bsize / 8

""" --------------- based on Professor Avi Kak's code -------------- """""""""
def gcd(a,b):                                                            #(B1)
    while b:                                                             #(B2)
        a, b = b, a%b                                                    #(B3)
    return a                                                             #(B4)

def test_integer_for_prime(p):                                           #(C1)
    probes = [2,3,5,7,11,13,17]                                          #(C2)
    for a in probes:                                                     #(C3)
        if a == p: return 1                                              #(C4)
    if any([p % a == 0 for a in probes]): return 0                       #(C5)
    k, q = 0, p-1                                                        #(C6)
    while not q&1:                                                       #(C7)
        q >>= 1                                                          #(C8)
        k += 1                                                           #(C9)
    for a in probes:                                                    #(C10)
        a_raised_to_q = pow(a, q, p)                                    #(C11)
        if a_raised_to_q == 1 or a_raised_to_q == p-1: continue         #(C12)
        a_raised_to_jq = a_raised_to_q                                  #(C13)
        primeflag = 0                                                   #(C14)
        for j in range(k-1):                                            #(C15)
            a_raised_to_jq = pow(a_raised_to_jq, 2, p)                  #(C16)
            if a_raised_to_jq == p-1:                                   #(C17)
                primeflag = 1                                           #(C18)
                break                                                   #(C19)
        if not primeflag: return 0                                      #(C20)
    probability_of_prime = 1 - 1.0/(4 ** len(probes))                   #(C21)
    return probability_of_prime                                         #(C22)


def pollard_rho_simple(p):                                               #(D1)
    probes = [2,3,5,7,11,13,17]                                          #(D2)
    for a in probes:                                                     #(D3)
        if p%a == 0: return a                                            #(D4)
    d = 1                                                                #(D5)
    a = random.randint(2,p)                                              #(D6)
    random_num = []                                                      #(D7)
    random_num.append( a )                                               #(D8)
    while d==1:                                                          #(D9)
        b = random.randint(2,p)                                         #(D10)
        for a in random_num[:]:                                         #(D11)
            d = gcd( a-b, p )                                           #(D12)
            if d > 1: break                                             #(D13)
        random_num.append(b)                                            #(D14)
    return d                                                            #(D15)

def pollard_rho_strong(p):                                               #(E1)
    probes = [2,3,5,7,11,13,17]                                          #(E2)
    for a in probes:                                                     #(E3)
        if p%a == 0: return a                                            #(E4)
    d = 1                                                                #(E5)
    a = random.randint(2,p)                                              #(E6)
    c = random.randint(2,p)                                              #(E7)
    b = a                                                                #(E8)
    while d==1:                                                          #(E9)
        a = (a * a + c) % p                                             #(E10)
        b = (b * b + c) % p                                             #(E11)
        b = (b * b + c) % p                                             #(E12)
        d = gcd( a-b, p)                                                #(E13)
        if d > 1: break                                                 #(E14)
    return d                                                            #(E15)

def factorize(n):                                                        #(F1)
    prime_factors = []                                                   #(F2)
    factors = [n]                                                        #(F3)
    while len(factors) != 0:                                             #(F4)
        p = factors.pop()                                                #(F5)
        if test_integer_for_prime(p):                                    #(F6)
            prime_factors.append(p)                                      #(F7)
            #print "Prime factors (intermediate result): ", prime_factors#(F8)
            continue                                                     #(F9)
#        d = pollard_rho_simple(p)                                      #(F10)
        d = pollard_rho_strong(p)                                       #(F11)
        if d == p:                                                      #(F12)
            factors.append(d)                                           #(F13)
        else:                                                           #(F14)
            factors.append(d)                                           #(F15)
            factors.append(p/d)                                         #(F16)
    return prime_factors                                                #(F17)


def MI(num, mod):
    '''
    The function returns the multiplicative inverse (MI) of num modulo mod
    '''
    NUM = num; MOD = mod
    x, x_old = 0L, 1L
    y, y_old = 1L, 0L
    while mod:
        q = num // mod
        num, mod = mod, num % mod
        x, x_old = x_old - q * x, x
        y, y_old = y_old - q * y, y
    if num != 1:
        return "NO MI. However, the GCD of %d and %d is %u" % (NUM, MOD, num)
    else:
        MI = (x_old + MOD) % MOD
        return MI

class PrimeGenerator( object ):   

    def __init__( self, **kwargs ): 
        if kwargs.has_key('bits'): bits = kwargs.pop('bits')
        if kwargs.has_key('debug'): debug = kwargs.pop('debug')
        self.bits = bits
        self.debug = debug

    def set_initial_candidate(self):
        candidate = random.getrandbits( self.bits )
        if candidate & 1 == 0: candidate += 1
        candidate |= (1 << self.bits-1)
        candidate |= (2 << self.bits-3)
        self.candidate = candidate
      
    def set_probes(self):
        self.probes = [2,3,5,7,11,13,17]

    # This is the same primality testing function as shown earlier
    # in Section 11.5.6 of Lecture 11:
    def test_candidate_for_prime(self):
        'returns the probability if candidate is prime with high probability'
        if any([self.candidate % a == 0 for a in self.probes]): return 0
        p = self.candidate
        # need to represent p-1 as  q * 2^k  
        k, q = 0, self.candidate-1
        while not q&1:  # while q is even
            q >>= 1
            k += 1
        if self.debug: print "q = ", q, " k = ", k
        for a in self.probes:
            a_raised_to_q = pow(a, q, p)     
            if a_raised_to_q == 1 or a_raised_to_q == p-1: continue
            a_raised_to_jq = a_raised_to_q
            primeflag = 0
            for j in range(k-1):
                a_raised_to_jq = pow(a_raised_to_jq, 2, p) 
                if a_raised_to_jq == p-1: 
                    primeflag = 1
                    break
            if not primeflag: return 0
        self.probability_of_prime = 1 - 1.0/(4 ** len(self.probes))
        return self.probability_of_prime

    def findPrime(self):
        self.set_initial_candidate()
        if self.debug:  print "        candidate is: ", self.candidate
        self.set_probes()
        if self.debug:  print "        The probes are: ", self.probes
        while 1:
            if self.test_candidate_for_prime():
                if self.debug:
                    print "Prime number: ", self.candidate, \
                       " with probability: ", self.probability_of_prime
                break
            else:
                self.candidate += 2
                if self.debug: print "        candidate is: ", self.candidate
        return self.candidate

# Author: Tanmay Prakash
#         tprakash at purdue dot edu
# Solve x^p = y for x
# for integer values of x, y, p
# Provides greater precision than x = pow(y,1.0/p)
# Example:
# >>> x = solve_pRoot(3,64)
# >>> x
# 4L

import numpy as np
import sys

def solve_pRoot(p,y):
    p = long(p);
    y = long(y);
    # Initial guess for xk
    try:
        xk = long(pow(y,1.0/p));
    except:
        # Necessary for larger value of y
        # Approximate y as 2^a * y0
        y0 = y;
        a = 0;
        while (y0 > sys.float_info.max):
            y0 = y0 >> 1;
            a += 1;
        # log xk = log2 y / p
        # log xk = (a + log2 y0) / p
        xk = long(pow(2.0, ( a + np.log2(float(y0)) )/ p ));

    # Solve for x using Newton's Method
    err_k = pow(xk,p)-y;
    while (abs(err_k) > 1):
        gk = p*pow(xk,p-1);
        err_k = pow(xk,p)-y;
        xk = -err_k/gk + xk;
    return xk
""" --------------------- END PROVIDED CODES -----------------------------------"""""
def findPQ():
    generator = PrimeGenerator( bits = Bsize, debug = 0);
    while(1):
        p, q = generator.findPrime(), generator.findPrime();
            
        
        if(BitVector(intVal = p)[0] == 1 and BitVector(intVal = p)[1] == 1 and BitVector(intVal = q)[0] == 1 and BitVector(intVal = q)[1] == 1):
            if(p != q):
                if(gcd(p - 1, e) == 1 and gcd(q - 1,e) == 1):
                    break;

    return p, q;


def genkeys():
    while(1):
        p1, q1 = findPQ();
        p2, q2 = findPQ();
        p3, q3 = findPQ();
        n1, n2, n3 = (p1*q1), (p2*q2), (p3*q3)
        if(gcd(n1, n2) == 1 and gcd(n2, n3) == 1 and gcd(n1, n3) == 1): # n1,n2,n3 has gotta be relative prime to each other
            break;
    tot1, tot2, tot3 = (p1-1)*(q1-1),(p2-1)*(q2-1),(p3-1)*(q3-1)
    d1, d2, d3 = MI(e, tot1), MI(e, tot2), MI(e, tot3)
    
    return n1, n2, n3,

def encrypt(text, npub):
    enc_text = "";
    i = 0;
    # use 128 bits = 16 bytes for block size padded with zeros to the left (total 256 bits)
    while(i*textsize < len(text)):
        if(i*textsize + textsize > len(text)):
            slice = text[i*textsize:len(text)];
        else:
            slice = text[i*textsize:i*textsize + textsize];

        enc_slice = BitVector(intVal = pow(int(BitVector(textstring = slice)), e, npub), size  = modsize);
        enc_text += (enc_slice.get_text_from_bitvector());
        i += 1;
     
    #print i
    return enc_text

    
def decrypt(text1, text2, text3, npub1, npub2, npub3):
    N = npub1 * npub2 * npub3;
    M1 = N/npub1;
    M2 = N/npub2;
    M3 = N/npub3;
    M1_mi = MI(M1, npub1);
    M2_mi = MI(M2, npub2);
    M3_mi = MI(M3, npub3);

    i = 0;
    dec_text = "";

    while(i*textsize * 2 + textsize * 2 <= len(text1)):
        C1 = int(BitVector(textstring = text1[i*textsize * 2:i*textsize * 2 + textsize * 2]));
        C2 = int(BitVector(textstring = text2[i*textsize * 2:i*textsize * 2 + textsize * 2]));
        C3 = int(BitVector(textstring = text3[i*textsize * 2:i*textsize * 2 + textsize * 2]));
        # CRT
        message_cubed_mod_N = (C1 * M1 * M1_mi + C2 * M2 * M2_mi + C3 * M3 * M3_mi) % N
        message_slice = solve_pRoot(e, message_cubed_mod_N);
        if(i*textsize * 2 + textsize * 2 == len(text1)):
            dec_slice =  BitVector(intVal = message_slice);
            while(dec_slice.length() % 8 != 0):
                dec_slice.pad_from_left(1);
        else:
            dec_slice =  BitVector(intVal = message_slice, size = Bsize);
        dec_text += dec_slice.get_text_from_bitvector();
        i += 1;
    return dec_text;

def main():

    if(len(sys.argv) < 3):
        print "Usage: [mode] [input] [output]"
        sys.exit();

    n1, n2, n3, = genkeys();
    #print n1, n2, n3
    fp = open(sys.argv[1], "rb");
    text = fp.read();
    
    enc1 = encrypt(text, n1);
    enc2 = encrypt(text, n2);
    enc3 = encrypt(text, n3);
    file1, file2, file3 = open("enc1.txt", "wb"), open("enc2.txt", "wb"), open("enc3.txt", "wb"),
    file1.write(enc1);

    file2.write(enc2);
    
    file3.write(enc3);

    
    result = decrypt(enc1, enc2, enc3, n1, n2, n3);
    out = open(sys.argv[2], "wb");
    out.write(result);
    fp.close();
    file1.close();
    file2.close();
    file3.close();
    out.close();
        
if __name__ == "__main__":
    main()
    
