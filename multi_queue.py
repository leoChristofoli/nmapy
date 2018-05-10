import multiprocessing as mp
from multiprocessing import Pool, Queue
from package.nmapy import Host, nmap

import sys
import random
import time

output = Queue()

_list = open('l.txt', 'r').readlines()
_list = [l.strip() for l in _list]

def call_namp(host):
    nmap(host)
    output.put(host)

def print_result(o):
    while True:
        r = [o.get() for res in processes]
        print(r)

def create_processes():
    processes = [mp.Process(target=call_namp, args=(h, )) for h in _list]
    # Run processes
    for p in processes:
        p.start()

    # Exit the completed processes
    for p in processes:
        p.join()


if __name__ == '__main__':
    p1 = mp.Process(target=print_result, args=(output, ))
    p1.start()
    print('creating processes')
    time.sleep(10)
    create_processes()
    print('finished')
    p1.join()