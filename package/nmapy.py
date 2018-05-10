import xml.etree.ElementTree as ET
import subprocess
import xmltodict
import multiprocessing
import time
import socket
from datetime import datetime

import json

if __name__ == '__main__':
    from utils import Response
else:
    from package.utils import Response


def nmap(host, num=0):
    '''
    This function uses xmltodict

    <mydocument has="an attribute">
    <and>
        <many>elements</many>
        <many>more elements</many>
    </and>
    <plus a="complex">
        element as well
    </plus>
    </mydocument>

    doc['mydocument']['@has'] # == u'an attribute'
    doc['mydocument']['and']['many'] # == [u'elements', u'more elements']
    doc['mydocument']['plus']['@a'] # == u'complex'
    doc['mydocument']['plus']['#text'] # == u'element as well'
    '''
    response = Response()
    p = multiprocessing.current_process()
    print(p.name, p.pid)
    a = 'nmap -O {h} -oX -'.format(h=host)
    print(host)
    try:
        r = subprocess.check_output(a)
    except Exception as error:
        response.success = False
        response.error = str(error)
        return response

    try:
        doc = xmltodict.parse(r)
        response.result = doc
    except Exception as error:
        response.success = False
        response.error = str(error)
        return response
    time.sleep(num)

    return response


class Host(object):

    def __init__(self, host):
        self.host = host
        self.nmap = nmap(self.host)
        self.nmaprun = self.nmap.result['nmaprun'] if self.nmap.success else None

    @property
    def get_nmap(cls):
        return cls.nmap.success

    @property
    def is_up(cls):
        if cls.nmap.success:
            res = cls.nmaprun
            if 'host' in res:
                state = res['host']['status']['@state']
                if state == 'up':
                    return True

        return False

    @property
    def state(cls):
        if cls.nmap.success:
            res = cls.nmaprun
            if 'host' in res:
                state = res['host']['status']['@state']
                return state

        return None

    @property
    def hostname(cls):
        if 'host' in cls.nmaprun:
            hostnames = cls.nmaprun['host']['hostnames']

            return json.dumps(hostnames)

    @property
    def dns(cls):
        try:
            n = socket.gethostbyaddr(cls.host)
            m = socket.gethostbyname_ex(cls.host)
            print(cls.host, ' -> ',m)
            return n
        except Exception as err:
            print(err)
            return None

    @property
    def address(cls):
        if cls.nmap.success:
            res = cls.nmaprun
            if 'host' in res:
                addresses = res['host']['address']
                if '@addr' in addresses:
                    addr = res['host']['address']['@addr']
                else:
                    addr_list = []
                    for i in addresses:
                        if  i['@addrtype'] == 'ipv4':
                            addr = i['@addr']
                        else:
                            addr = None
                return addr

        return None

    @property
    def address_with_mac(cls):
        if cls.nmap.success:
            res = cls.nmaprun
            if 'host' in res:
                addresses = res['host']['address']
                print(addresses)
                if '@addr' in addresses:
                    addr = res['host']['address']['@addr']
                else:
                    addr_list = []
                    for i in addresses:
                        if '@vendor' in i:
                            res =  i['@addrtype'] + ': '  + i['@addr'] + ' vendor: ' + i['@vendor']
                        else:
                            res =  i['@addrtype'] + ': '  + i['@addr']
                        addr_list.append(res)
                    addr = ', '.join(addr_list)
                return addr

        return None

    @property
    def os(cls):
        if cls.nmap.success:
            res = cls.nmaprun
            if 'host' in res:
                # os = res['host']['os']['osmatch']
                # name = [o['@name'] for o in os]
                # acc = [o['@accuracy'] for o in os]
                # return [a for a in zip(name, acc)]
                os = res['host']['os']
                return os

        return None

    @property
    def nmap_str(cls):
        start = datetime.now()
        response = Response()

        a = 'nmap -O {h}'.format(h=cls.host)
        try:
            r = subprocess.check_output(a)
            response.result = r
        except Exception as error:
            response.success = False
            response.error = str(error)
            return response

        end = datetime.now()
        response.execution_time = end - start

        if response.success:
            return response.result
        return response.error


if __name__ == '__main__':
    h = Host('BRWS2580.lapa.mmm.com')
    print(h.address_with_mac)
    h = Host('br-garibaldi')
    print(h.address_with_mac)
