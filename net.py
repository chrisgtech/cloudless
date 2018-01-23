#! python3

import netifaces

def getips():
    ips = []
    for iface in netifaces.interfaces():
        addresses = netifaces.ifaddresses(iface)
        if not netifaces.AF_INET in addresses:
            continue
        print(iface)
        info = addresses[netifaces.AF_INET]
        address = info[0]['addr']
        if address == '127.0.0.1':
            continue
        print(address)
        ips.append(address)
    return ips
    
if __name__ == '__main__':
    print(getips())