from multiprocessing import Pool
import os, time, random
def run_task(name):
    print("%s, (%s)" % (name, os.getpid()))
    time.sleep(random.random() % 3)
    print('%s:end' % name)

if __name__ == '__main__':
    p = Pool(processes=3)
    for i in range(5):
        p.apply_async(run_task, args=(i,))
    p.close()
    p.join()
