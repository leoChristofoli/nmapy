import multiprocessing
from multiprocessing import Pool, Queue
from package.nmapy import Host, nmap

import sys
import random
import time

from datetime import datetime


result_list = []
error_list = []

def host_analyse(item, q=None):
    host = Host(item)
    to_print = '''
        {name};{isup};{dns};{ns};{addr};{addr_mac};{dt}
    ''' \
    .format(
        name=item,
        isup=host.is_up,
        dns=host.hostname,
        ns=host.dns,
        addr=host.address,
        addr_mac=host.address_with_mac,
        dt=datetime.now().date()
    )
    if q:
        q.put(to_print)
    return(to_print.strip())

def log_result(res):
    result_list.append(res)

def create_pool(l, f):
    _list = open(l, 'r').readlines()
    _list = [l.strip() for l in _list]
    q = multiprocessing.Queue()
    pool = Pool(processes=4)

    results = [pool.apply_async(f, args=(host, ), callback=log_result) for host in _list]

    output = []
    for p in results:
        try:
            output.append(p.get())
        except Exception as err:
            output.append(str(err))

    print(output)
    while not q.empty():
        result_list.append(q.get())


def print_result():
    print(len(result_list))
    for r in result_list:
        print(r)

def main(l):
    start = datetime.now()
    print('the processes are begining')
    create_pool(l, host_analyse)
    print('pool is done')
    print_result()
    print('finnished')

    end = datetime.now()
    total = end-start
    print(total)
    with open('result.txt', 'w') as _file:
        _file.write('\n'.join(result_list))
        _file.close()

if __name__ == '__main__':

    host_analyse('169.6.168.25')
