#-------------------------------------------------------------------------------
# Name:        ????
# Purpose:
#
# Author:      gaohe
#
# Created:     12/02/2015
# Copyright:   (c) gaohe 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import threading
import time
import Queue
SHARE_Q = Queue.Queue()  
_WORKER_THREAD_NUM = 100
class MyThread(threading.Thread) :
    def __init__(self, func) :
        super(MyThread, self).__init__()  
        self.func = func 
    def run(self) :
        self.func()
def do_something(item) :
    print item
def worker() :
    global SHARE_Q
    while True :
        if not SHARE_Q.empty():
            item = SHARE_Q.get() 
            do_something(item)
            time.sleep(1)
            SHARE_Q.task_done()
def main() :
    global SHARE_Q
    threads = []
    for task in xrange(5) :
        SHARE_Q.put(task)
    
    for i in xrange(_WORKER_THREAD_NUM) :
        thread = MyThread(worker)
        thread.start()  
        threads.append(thread)
    for thread in threads :
        thread.join()
    SHARE_Q.join()
if __name__ == '__main__':
    main()
