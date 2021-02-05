# -*- coding: utf-8 -*-
# @Author: ZYSama
# @Created Date: 2019-10-30 20:03:02
# @Last Modified time: 2019-11-03 16:52:17
# @Software: Sublime

# import hashlib as hl
import numpy as np

# s = hl.sha256("111123132132")
# print s
# print list(str(s))[0:7]
# ms = str([1,0,1,0,1])
ms = 'fasfsnflkasnkld'
print(hash(ms))
ms = str(hash(ms))
# print map(int,ms)
ms = list(ms)[-7:-1]
# print ','.join(ms)
print map(int,ms)