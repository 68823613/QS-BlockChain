#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 30 17:26:25 2019

@author: bai
"""

import random
import math
import numpy as np

class Chameleonhash:
    def Hash(self,message):
        n = random.randint(1,10)
        q = random.randint(2,10)
        m0 = n*int(math.ceil(math.log(q,2)))
        k = int(math.ceil(math.log(q,2)))
        m = m0 + n * k
        l = 1024
        s = math.sqrt(5*n * math.log(q,2))
        N0 = np.random.randint(0,q,(n,l))
        NZ = np.random.randint(0,q,(n,m0))
        T = np.random.randint(0,255,(m0,n * k))
        
        r_sum = 0
        while True:
          r = np.random.randint(0,10,(m,1)) 
          r_len = len(r)
          
          for i in range(r_len):
              r_sum = r_sum + r[i]**2
          r_sum = math.sqrt(r_sum)
          if r_sum > math.floor(s * math.log(m,2)):
              r = np.random.randint(0,255,(m,1))
          else:
              break   
        while True:
          M = np.random.randint(0,q,(n,n))     
          if np.linalg.det(M) <= 0 :
              M = np.random.randint(0,q,(n,n))
          else:
              break
        G = np.zeros((n,n * k))
        for i in range(0,n):
            for j in range(i*k,(i+1)*k):
                #print('j = ',j)
                G[i][j] = int(2**(j-i*k))
        Ny = -np.dot(NZ,T)+np.dot(M,G)
        N1 = np.c_[NZ,Ny]
        #print('N1 = ',N1)
        #message1 = bin(message)
        message1 = ''.join([bin(ord(c)).replace('0b', '') for c in message])
        message1_len = len(message1)
        miu = np.zeros((l,1))
        for i in range(message1_len)[::-1]:
            miu[l-message1_len+i] = int(message1[i])
    
        
        HN = np.dot(N0,miu) + np.dot(N1,r)
        HN1 = str(HN)
        #print("HN1",HN1)
        
                
            
        return HN1
        
        
        
