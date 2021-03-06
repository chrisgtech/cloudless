#! python3

import socket
import netifaces, ipgetter
from ipaddress import ip_address

def localips():
    ips = []
    for iface in netifaces.interfaces():
        addresses = netifaces.ifaddresses(iface)
        if not netifaces.AF_INET in addresses:
            continue
        info = addresses[netifaces.AF_INET]
        address = ip_address(info[0]['addr'])
        if address.is_loopback:
            #print('Ignoring loopback {}'.format(address))
            continue
        if address.is_global:
            #print('Ignoring public {}'.format(address))
            continue
        ips.append(str(address))
    return ips
    
def gateways():
    ips = []
    for name, gateway in netifaces.gateways().items():
        if not netifaces.AF_INET in gateway:
            continue
        ip = gateway[netifaces.AF_INET][0]
        ips.append(ip)
    return ips
    
def publicip():
    ip = ipgetter.myip()
    if ip is None or ip == '':
        return None
    address = ip_address(ip)
    if not address.is_global:
        return publicip()
    return str(address)
    
def internet(host="8.8.8.8", port=53, timeout=3):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except Exception as ex:
        print(str(ex))
        return False
    
if __name__ == '__main__':
    print(localips())
    print(gateways())
    print(publicip())
    print(internet())