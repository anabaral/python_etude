import multiprocessing as mp
import time

def foo(q):
    time.sleep(1)
    q.put('hello')

if __name__ == '__main__':
#    mp.set_start_method('spawn')
#    q = mp.Queue()
#    p = mp.Process(target=foo, args=(q,))
#    p.start()

    ctx = mp.get_context('spawn')
    q = ctx.Queue()
    p = ctx.Process(target=foo, args=(q,))

    p.start()
    print(q.get())
    p.join()
