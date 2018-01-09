from multiprocessing import Pool
import time

def f(x):
    time.sleep(4-(x % 4))
    print (x)
    return x*x

if __name__ == '__main__':
    with Pool(3) as p:
        print(p.map(f, [1,2,3,4,5,6,7,8,9,10,11,12,13,14]))