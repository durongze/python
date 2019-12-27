import random
import threading
import time
#继承threading.Thread
class myThread(threading.Thread):
    def __init__(self,name,urls):
        threading.Thread.__init__(self,name=name)
        self.urls = urls

    def run(self):
        print ('%s' % threading.current_thread().name)
        for url in self.urls:
            print("%s:%s" % (threading.current_thread().name, url))
            time.sleep(random.random())
        print("%s ended" % (threading.current_thread().name))

if __name__ == "__main__":
    t1 = myThread(name='t1', urls=['url1','url2','url3'])
    t2 = myThread(name='t2', urls=['url4', 'url5','url6'])
    t1.start()
    t2.start()
    t1.join()
    t2.join()
