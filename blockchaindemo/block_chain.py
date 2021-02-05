#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov  3 14:50:46 2019

@author: bai
"""

import block
import json
import sys
sys.path.append('../ntrusign')
from ntrusign import *
import numpy as np
#import chameleon_hash

class BlockChain:
    def __init__(self):
        self.blocks=[]


    def send_data(self, tx,sign):#web端增加信息时调用
        print "send_data:",tx
        if dataverify(tx,sign):
          pre_block = self.blocks[len(self.blocks) - 1]
          new_block = block.generate_new_block(pre_block, tx)
          self.append_block(new_block)
        else:
          print "data verify error"

        
    def searchedit(self,dataid,data,sign):#web端修改信息时调用
      if dataverify(data,sign):
        for block1 in self.blocks:
            print "dataid:",dataid
            print "edit data:",data
            print  block1.Tx
            if block1.Tx == 'Genesis Block':
              continue         
            if dataid in str(block1.Tx):
              block1.Tx = data
            else:
              print "error"
        self.blockprint()
      else:
        print "data verity error"
      

    def append_block(self, new_block):#增加新区块，每增加一个就打印一遍
        print "append_block"
        if len(self.blocks) == 0 or is_valid(new_block, self.blocks[len(self.blocks) - 1]):
            self.blocks.append(new_block)
            self.blockprint()

    

    def blockprint(self):#打印区块链
        print "----------------blockchain begin------------------"
        for block1 in self.blocks:
            
            print("Index: %d\n"
                  "Pre.Has: %s\n"
                  "Curr.Hash: %s\n"
                  "Txhash: %s\n"
                  "Timestamp: %d\n"
                  "Nonce:%d\n"
                  "Tx:%s\n"
                  % (block1.index, block1.prevBlockHash, block1.hash, block1.Txhash, block1.timestamp, block1.Nonce,block1.Tx))
        print "----------------blockchain end------------------"

def is_valid(new_block, old_block):#检验相关有效性
    if new_block.index - 1 != old_block.index:
        return False
    if new_block.prevBlockHash != old_block.hash:
        return False
    proofofwork = block.NewProofOfWork(new_block)
    nonce,blockhash = block.Run(new_block,proofofwork)
    if blockhash != new_block.hash:
        return False
    return True


def new_block_chain():#创建新的区块链
    genesis_block = block.generate_genesis_block()
    block_chain = BlockChain()
    block_chain.append_block(genesis_block)
    return block_chain

def readjsonuser():#寻找用户json数据
    # print "readjsonuser"
    path = 'D:/Workspace/java/test-master/data/database.json'
    with open(path,'r') as fr:
        datas = json.load(fr)
        # print len(datas)
    # for data in datas:
    #     print data["username"]
    # print datas
    return datas

#read the data of doctor
def readjsondoctor():#寻找医生json数据
    # print "readjsondoctor"
    path = 'D:/Workspace/java/test-master/data/doctor-database.json'
    with open(path,'r') as fr:
        datas = json.load(fr)
    return datas


def editdata(dataid,dataact,bc):#修改数据操作
    if dataact == 'user-edit':          
        datas = readjsonuser()
    elif dataact == 'doctor-edit':
        datas = readjsondoctor()
    for data in datas:
        # print "dataid in json:",data["id"]
        # print "dataid",dataid
        if str(data["id"]) == dataid:
        # print "select id "
          sign = datasign(data)
          bc.searchedit(dataid,data,sign)

   
    

def adddata(dataid,dataact,bc):#添加数据操作
    if dataact == 'user-add':
        datas = readjsonuser()
    elif dataact == 'doctor-add':
        datas = readjsondoctor()
    for data in datas:
        # print "dataid in json:",data["id"]
        # print "dataid",dataid
        if str(data["id"]) == dataid:
            print "select block data"
            sign = datasign(data)
            bc.send_data(json.dumps(data),sign)

def datasign(data):#数据签名
    serverp = NTRUSign(7,2,491531)
    ranPol=[-1,-1,1,1]
    b = np.random.randint(0,2)
    f=[1,0,-1,1,-1,1]
    g=[-1,0,1,1,1,0,-1]
    d=2
    blockp = NTRUSign(7,2,491531)
    blockp.genPublicKey(f,g,2)
    pub_key=blockp.getPublicKey()
    serverp.setPublicKey(pub_key)
    return serverp.sign(str(data),ranPol,b,f,g,2)



def dataverify(data,sign):#验证签名
  blockp = NTRUSign(7,2,491531)
  f=[1,0,-1,1,-1,1]
  g=[-1,0,1,1,1,0,-1]
  d=2
  blockp.genPublicKey(f,g,2)

  pub_key=blockp.getPublicKey()
  
  return blockp.verify(str(data),sign)


