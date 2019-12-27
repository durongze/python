import os
from multiprocessing import Process

def run_proc(name):
    print('child proc %s :%s running... ', name, os.getpid())

if __name__ == '__main__':
    for i in range(5):
        p = Process(target=run_proc, args=(str(i),))
        p.start()
    p.join()
