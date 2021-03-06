#! python3
import sys
if sys.version_info < (3, 0):
    sys.stdout.write("Python 3.x is required")
    sys.exit(1)

from argparse import ArgumentParser

import security, server, client, net, user
        
def init(options):
    groupname = user.prompt('Enter name for new group: ')
    security.certgen(groupname)
    return groupname
    
def addmachine(options):
    groupname = options['group']['name']
    machinename = user.prompt('Enter name for the machine: ')
    security.certgen(machinename, groupname)
    return machinename

def main():
    parser = ArgumentParser()
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument('-s', '--server', action="store_true", help='Run in server mode')
    modes.add_argument('-m', '--machine', help='Machine to connect to')
    parser.add_argument('-r', '--remote', help='Remote host of machine')
    parser.add_argument('-p', '--port', help='Port for connection')
    args = parser.parse_args()
    options = user.loadconfig()
    notsetup = options['group']['name'] == user.UNKNOWN
    if notsetup:
        print('No group set, running init')
        groupname = init(options)
        options['group']['name'] = groupname
        user.saveconfig(options)
        return
    nomachine = options['machine']['name'] == user.UNKNOWN
    if nomachine:
        print('No machine set, adding machine')
        machinename = addmachine(options)
        options['machine']['name'] = machinename
        user.saveconfig(options)
        return
    thismachine = options['machine']['name']
    group = options['group']['name']
    if args.server:
        print('Running server for {}'.format(thismachine))
        port = options['group']['port']
        if 'port' in options['machine']:
            port = options['machine']['port']
        if args.port:
            port = args.port
        server.main(group, thismachine, int(port))
        return
    if args.machine:
        remote = args.machine
        print('Contacting {}'.format(remote))
        port = options['group']['port']
        if 'port' in options['machine']:
            port = options['machine']['port']
        if args.port:
            port = args.port
        host = 'localhost'
        if args.remote:
            host = args.remote
        client.main(group, thismachine, remote, host, int(port))
        return
    parser.print_help()
    
if __name__ == "__main__":
    main()