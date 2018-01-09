from multiprocessing import Process
import time, random, os

def info(title):
    print(title)
    print('module name:' , __name__)
    print('parent : ', os.getppid())
    print('self : ', os.getpid())

def f(name):
    info('function f')
    time.sleep(int(random.random() * 4 ))
    print('hello ', name)

if __name__ == '__main__':
    info('main')
    names = ['bob','jane','emma',]
    processes = []
    for name in names:
        p = Process(target=f, args=(name,))
        processes.append(p)
        p.start()
    for p in processes:
        p.join()
