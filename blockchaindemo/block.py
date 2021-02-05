#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov  3 14:49:54 2019

@author: bai
"""
import sys
sys.path.append('../Chameleon_hash')
import chameleon_hash
import time
import hashlib,math,json



#targetBits = 20 
maxNonce =  sys.maxsize
# print int(maxNonce)

class Block:

    def __init__(self):
        self.index = 0  # 区块编号
        self.timestamp = 0  # 区块时间戳
        self.prevBlockHash= ''  # 上一个区块的哈希值
        self.hash = ''  # 当前区块的哈希值
        self.Txhash = ''  # 区块数据
        self.Nonce = 0 #工作量证明
        self.targetBits = 30 #
        self.Tx = '' # 区块数据



def NewProofOfWork(block2):#工作量证明
    target = 2
    target << (256-block2.targetBits)
    proofofwork = bin(target)
    
    proofofwork = ''.join([bin(ord(c)).replace('0b', '') for c in proofofwork])
    return proofofwork

def prepareData(block,nonce):#区块数据预处理
    blockdata = block.prevBlockHash + block.Txhash + str(block.timestamp) + str(block.targetBits) + str(nonce)
    return blockdata
    
    
def Run(block,proofofwork):#计算哈希的过程
    nonce = 0  
    while True:
        blockdata = prepareData(block,nonce)
        sha256 = hashlib.sha256()
        sha256.update(blockdata.encode())
        blockhash = sha256.hexdigest()
        if blockhash < proofofwork:
            break
        else:
            nonce +=1  
    return nonce,blockhash


def generate_new_block(pre_block, tx):#创建新区块
    new_block = Block()
    new_block.index = pre_block.index + 1
    new_block.prevBlockHash = pre_block.hash
    new_block.timestamp = int(time.time())
    chameleonhash = chameleon_hash.Chameleonhash()
    txhash = chameleonhash.Hash(tx)

    new_block.Txhash = txhash
    new_block.Tx = tx
    proof_of_work = NewProofOfWork(new_block)
    nonce,blockhash = Run(new_block,proof_of_work)
    new_block.Nonce = nonce
    new_block.hash = blockhash
    return new_block


def generate_genesis_block():#生成创世区块
    pre_block = Block()
    pre_block.index = -1
    pre_block.hash = ''
    pre_block.proof = 100
    return generate_new_block(pre_block, "Genesis Block")

