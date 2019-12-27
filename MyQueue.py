from multiprocessing import Process
from multiprocessing import Queue
import os, time, random

def proc_write(q, urls):
    print("%s writing.." % os.getpid())
    for url in urls:
        q.put(url)
        print("put %s" % url)
        time.sleep(random.random())

def proc_read(q):
    print("%s reading" % os.getpid())
    while(True):
        url = q.get(True)
        print("%s from queue" % url)

if __name__ == '__main__':
    q = Queue()
    pw1 = Process(target=proc_write, args=(q,['url1', 'url2', 'url3']))
    pw2 = Process(target=proc_write, args=(q, ['url4', 'url5', 'url6']))
    pr = Process(target=proc_read, args=(q,))
    pw1.start()
    pw2.start()
    pr.start()
    pw1.join()
    pw2.join()
    pr.terminate()
