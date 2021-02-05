# -*- coding: utf-8 -*-
# @Author: ZYSama
# @Created Date: 2019-10-30 18:51:38
# @Last Modified time: 2019-11-04 15:55:01
# @Software: Sublime
# NTRUSign by zy

import math
from fractions import gcd
import poly


class NTRUSign:
	N=None
	p=None
	q=None
	d=None
	f=None
	g=None
	h=None
	f_p=None
	f_q=None
	g_p=None
	pf_q=None
	D=None

	def __init__(self,N_new,p_new,q_new):
			self.N=N_new
			self.p=p_new
			self.q=q_new
			D=[0]*(self.N+1)
			D[0]=-1
			D[self.N]=1
			self.D=D


	#genrate public key h
	def genPublicKey(self,f_new,g_new,d_new):
		# Using Extended Euclidean Algorithm for Polynomials
		# to get s and t. Note that the gcd must be 1
		self.f=f_new
		self.g=g_new
		self.d=d_new

		pf = poly.multPoly([self.p],self.f)
		[gcd_f,s_f,t_f]=poly.extEuclidPoly(self.f,self.D)
		[gcd_pf,s_pf,t_pf]=poly.extEuclidPoly(pf,self.D)
		self.f_p=poly.modPoly(s_f,self.p)
		self.f_q=poly.modPoly(s_f,self.q)
	
		self.pf_q=poly.modPoly(s_pf,self.q)

		self.h=self.reModulo(poly.multPoly(self.g,self.pf_q),self.D,self.q)

		if not self.runTests():
			print "Failed!"
			quit()

	def getPublicKey(self):
		return self.h

	def setPublicKey(self,public_key):
		self.h=public_key


	def reModulo(self,num,div,modby):
		[_,remain]=poly.divPoly(num,div)
		return poly.modPoly(remain,modby)

	def myhash(self,ms):
		ms = str(ms)
		ms = str(hash(ms))
		ms = list(ms)[-self.N:-1]
		return map(int,ms)

	def sign(self,message,randPol,b,f_new,g_new,d_new):
		self.f=f_new
		self.g=g_new
		self.d=d_new
		#compute up,vp
		up = self.myhash(message)
		vp = self.myhash(self.h)

		#compute u1
		u1_pre = poly.multPoly([self.p],randPol)
		u1 = poly.addPoly(u1_pre,up)

		#compute v1
		v1 = self.reModulo(poly.multPoly(u1,self.h),self.D,self.q)

		#compute a
		[gcd_g,s_g,t_g] = poly.extEuclidPoly(self.g,self.D)
		self.g_p = poly.modPoly(s_g,self.p)

		a_pre = poly.subPoly(vp,v1)
		a = self.reModulo(poly.multPoly(a_pre,self.g_p),self.D,self.p)

		#compute v
		v_pre = poly.multPoly([int(math.pow(-1,b))],poly.multPoly(a,self.g)) 
		v = poly.addPoly(v1,v_pre)

		#compute sign
		sign_pre = poly.multPoly([int(math.pow(-1,b))],poly.multPoly(a,self.f))
		sign = poly.addPoly(randPol,sign_pre)
		return sign 

	def verify(self,message,sign):
		up = self.myhash(message)
		vp = self.myhash(self.h)

		u = poly.addPoly(poly.multPoly([self.p],sign),up)
		v = self.reModulo(poly.multPoly(u,self.h),self.D,self.q)

		w = self.reModulo(poly.subPoly(v,vp),self.D,self.p)
		for i in w:
			if i != 0:
				return "Error"
				return False
			else:
				continue
		print "success"
		return True



	def isPrime(self):
	    if self.N % 2 == 0 and self.N > 2: 
	        return False
	    return all(self.N % i for i in range(3, int(math.sqrt(self.N)) + 1, 2))

	def runTests(self):			
		# Checking if inputs satisfy conditions
		if not self.isPrime() :
			print "Error: N is not prime!"
			return False
	
		if gcd(self.N,self.p) != 1 :
			print "Error: gcd(N,p) is not 1"
			return False

		if gcd(self.N,self.q)!=1 :
			print "Error: gcd(N,q) is not 1"
			return False
	
		if self.q<=(6*self.d+1)*self.p:
			print "Error: q is not > (6*d+1)*p"
			return False
	
		if not poly.isTernary(self.f,self.d+1,self.d):
			print "Error: f does not belong to T(d+1,d)"
			return False
		
		if not poly.isTernary(self.g,self.d+1,self.d):
			print "Error: g does not belong to T(d+1,d)"
			return False
	
		return True		









	