#! python3
import sys
if sys.version_info < (3, 0):
    sys.stdout.write("Python 3.x is required")
    sys.exit(1)

from argparse import ArgumentParser
from configparser import ConfigParser
from pathlib import Path

import security, server, client

CONFIG_FILE = Path('cloudless.ini')
UNKNOWN = 'UNKNOWN'

def loadconfig():
    config = CONFIG_FILE
    options = ConfigParser()
    if not config.exists():
        group = {}
        group['name'] = UNKNOWN
        group['port'] = '57755'
        options['group'] = group
        machine = {}
        machine['name'] = UNKNOWN
        options['machine'] = machine
        saveconfig(options)
    options.read(config)
    return options
        
def saveconfig(options):
    config = CONFIG_FILE
    with open(config, 'w') as configfile:
        options.write(configfile)
        
def init(options):
    groupname = input('Enter name for new group: ')
    security.certgen(groupname)
    return groupname
    
def addmachine(options):
    groupname = options['group']['name']
    machinename = input('Enter name for the machine: ')
    security.certgen(machinename, groupname)
    return machinename

def main():
    parser = ArgumentParser()
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument('-s', '--server', action="store_true", help='Run in server mode')
    modes.add_argument('-m', '--machine', help='Machine to connect to')
    args = parser.parse_args()
    options = loadconfig()
    notsetup = options['group']['name'] == UNKNOWN
    if notsetup:
        print('No group set, running init')
        groupname = init(options)
        options['group']['name'] = groupname
        saveconfig(options)
        return
    nomachine = options['machine']['name'] == UNKNOWN
    if nomachine:
        print('No machine set, adding machine')
        machinename = addmachine(options)
        options['machine']['name'] = machinename
        saveconfig(options)
        return
    host = options['machine']['name']
    if args.server:
        print('Running server for {}'.format(host))
        port = options['group']['port']
        if 'port' in options['machine']:
            port = options['machine']['port']
        server.main(int(port), host)
        return
    if args.machine:
        remote = args.machine
        print('Connecting to  {}'.format(remote))
        group = options['group']['name']
        port = options['group']['port']
        if 'port' in options['machine']:
            port = options['machine']['port']
        client.main('localhost', int(port), remote, group)
        return
    parser.print_help()
    
if __name__ == "__main__":
    main()