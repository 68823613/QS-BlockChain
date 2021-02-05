# -*- coding=utf-8 -*-
import socket
import threading
import Queue
from HttpHead import HttpRequest
import sys
sys.path.append('../blockchaindemo')
sys.path.append('../ntrusign')
import block_chain,ntrusign



# 每个任务线程
class WorkThread(threading.Thread):
    def __init__(self, work_queue):
        # super().__init__()

        self.work_queue = work_queue
        self.daemon = True

    def run(self):
        while True:
            func, args = self.work_queue.get()
            func(*args)
            self.work_queue.task_done()


# 线程池
class ThreadPoolManger():
    def __init__(self, thread_number):
        self.thread_number = thread_number
        self.work_queue = Queue.Queue()
        for i in range(self.thread_number):     # 生成一些线程来执行任务
            thread = WorkThread(self.work_queue)
            thread.start()

    def add_work(self, func, *args):
        self.work_queue.put((func, args))


def tcp_link(bc,sock, addr):
    print('Accept new connection from %s:%s...' % addr)
    request = sock.recv(1024)
    http_req = HttpRequest()
    http_req.passRequest(bc,request)
    sock.send(http_req.getResponse().encode('utf-8'))
    sock.close()


def start_server(bc):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('127.0.0.1', 9999))
    s.listen(10)
    # thread_pool = ThreadPoolManger(5)
    print('listen in %s:%d' % ('127.0.0.1', 9999))
    while True:
        sock, addr = s.accept()
        tcp_link(bc,sock, addr)
        # thread_pool.add_work(tcp_link, *(sock, addr))



if __name__ == '__main__':
    bc = block_chain.new_block_chain()
 
    start_server(bc)
    pass
