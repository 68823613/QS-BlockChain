# -*- coding: utf-8 -*-
# @Author: LQH and ZY
# @Created Date: 2019-10-31 10:45:28
# @Last Modified time: 2019-11-04 12:08:56
# @Software: Sublime
import sys
sys.path.append('../Server')
import block_chain
import server


if __name__ == '__main__':
	server.start_server()
	pass
	# bc = block_chain.new_block_chain()
	# bc.send_data("send 1 BTC to jack")
	# bc.send_data("send 2 BTC to jack")
	# bc.blockprint()


