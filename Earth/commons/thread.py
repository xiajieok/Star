import threading
from time import ctime, sleep


def music(func):
    for i in range(5):
        print("This is music %s.%s" % (func, ctime()))
        sleep(1)


def movie(func):
    for i in range(5):
        print("This is move %s.%s" % (func, ctime()))
        sleep(1)


threads = []
t1 = threading.Thread(target=music, args=(u'Hello !!!',))
threads.append(t1)
t2 = threading.Thread(target=movie, args=(u'Fox    !!!',))
threads.append(t2)

if __name__ == '__main__':
    # print(threads)
    for t in threads:
        t.setDaemon(True)
        t.start()
    t.join()
    print('All is over %s' % ctime())
