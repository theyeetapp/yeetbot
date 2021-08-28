import threading
import time

exitFlag = 0


class MyThread(threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        print("Starting {0}".format(self.name))
        threadLock.acquire()
        printTime(self.name, 5, self.counter)
        print("Exiting {0}".format(self.name))
        threadLock.release()


def printTime(threadName, counter, delay):
    while counter:
        if exitFlag:
            threadName.exit()
        time.sleep(delay)
        print("{0}:{1}".format(threadName, time.ctime(time.time())))
        counter -= 1


threads = list()
threadLock = threading.Lock()
thread1 = MyThread(1, "Thread 1", 1)
thread2 = MyThread(2, "Thread 2", 2)
thread3 = MyThread(3, "Thread 3", 3)

thread1.start()
thread2.start()
thread3.start()

threads.append(thread1)
threads.append(thread2)
threads.append(thread3)

for t in threads:
    t.join()

print("Exiting Main Thread")
