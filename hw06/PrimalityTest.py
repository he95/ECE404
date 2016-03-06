#!/usr/bin/env python

##  PrimalityTest.py
##  Author: Avi Kak
##  Date:   February 18, 2011
##  An implementation of the Miller-Rabin primality test

def test_integer_for_prime(p):                                           #(A)
    probes = [2,3,5,7,11,13,17]                                          #(B)
    if any([p % a == 0 for a in probes]): return 0                       #(C)
    k, q = 0, p-1        # need to represent p-1 as  q * 2^k             #(D)
    while not q&1:                                                       #(E)
        q >>= 1                                                          #(F)
        k += 1                                                           #(G)
    for a in probes:                                                     #(H)
        a_raised_to_q = pow(a, q, p)                                     #(I)
        if a_raised_to_q == 1 or a_raised_to_q == p-1: continue          #(J)
        a_raised_to_jq = a_raised_to_q                                   #(K)
        primeflag = 0                                                    #(L)
        for j in range(k-1):                                             #(M)
            a_raised_to_jq = pow(a_raised_to_jq, 2, p)                   #(N)
            if a_raised_to_jq == p-1:                                    #(O)
                primeflag = 1                                            #(P)
                break                                                    #(Q)
        if not primeflag: return 0                                       #(R)
    probability_of_prime = 1 - 1.0/(4 ** len(probes))                    #(S)
    return probability_of_prime                                          #(T)

primes = [179, 233, 283, 353, 419, 467, 547, 607, 661, 739, 811, 877, \
          947, 1019, 1087, 1153, 1229, 1297, 1381, 1453, 1523, 1597, \
          1663, 1741, 1823, 1901, 7001, 7109, 7211, 7307, 7417, 7507, \
          7573, 7649, 7727, 7841]                                        #(U)

import random                                                            #(V)
for p in primes:                                                         #(W)
    p += random.randint(1,10)                                            #(X)
    probability_of_prime = test_integer_for_prime(p)                     #(Y)
    if probability_of_prime > 0:                                         #(Z)
        print p, " is prime with probability: ", probability_of_prime    #(a)
    else:                                                                #(b)
        print p, " is composite"                                         #(c)
