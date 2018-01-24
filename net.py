#! python3

import netifaces, ipgetter
from ipaddress import ip_address

def ifaceips():
    ips = []
    for iface in netifaces.interfaces():
        addresses = netifaces.ifaddresses(iface)
        if not netifaces.AF_INET in addresses:
            continue
        #print(iface)
        info = addresses[netifaces.AF_INET]
        address = ip_address(info[0]['addr'])
        if address.is_loopback:
            print('Ignoring loopback {}'.format(address))
            continue
        if address.is_global:
            print('Ignoring public {}'.format(address))
            continue
        #print(address)
        ips.append(str(address))
    return ips
    
def publicip():
    ip = ipgetter.myip()
    if ip is None or ip == '':
        return None
    address = ip_address(ip)
    if not address.is_global:
        return publicip()
    return str(address)
    
if __name__ == '__main__':
    print(ifaceips())
    print(publicip())