from datetime import datetime
import multiprocessing as m
import os

from package.nmapy import Host


def atl(hostname):
    host = Host(hostname)
    to_print = '''
        NAME: {name}
        IS_UP: {isup}
        NMAP HOSTNAME: {dns}
        DNS: {ns}
        ADDRESS: {addr}
        THIS SCAN DATE: {dt}

        ------------------------
        NMAP RESULT
        {np}

    ''' \
    .format(
        name=hostname,
        isup=host.is_up,
        dns=host.hostname,
        ns=host.dns,
        addr=host.address,
        dt=datetime.now().date(),
        np=host.nmap_str
    )
    res = {
        'host': hostname,
        'res': to_print
    }
    return res

def auto_scan(l):
    try:
        _file = open(l, 'r').readlines()
    except Exception as err:
        return str(err)
    
    _list = [l.strip() for l in _file]

    q = m.Queue()

    worker(atl, _list, q)

    print('reading queue')
    while not q.empty():
        res = q.get()

        write(res['host'], res['res'])

def write(name, what):
    path = 'results\\'
    path_exists = (os.path.isdir(path))
    if not path_exists:
        os.mkdir(path)

    w = open(path + name, 'w')
    w.write(what)
    w.close()

def worker(f, _list, queue):

    pool = m.Pool(processes=4)
    results = [pool.apply_async(f, args=(x, )) for x in _list]
    for r in results:
        try:
            queue.put(r.get())
        except Exception as err:
            queue.put(str(err))


if __name__ == '__main__':
    # auto_scan('m.txt')
    write('123', '321')