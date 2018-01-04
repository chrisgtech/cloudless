#! python3
from argparse import ArgumentParser
from configparser import ConfigParser
from pathlib import Path

import security

WARNING = f'This only works on Python 3.6'
CONFIG_FILE = Path('cloudless.ini')
UNKNOWN = 'UNKNOWN'

def loadconfig():
    config = CONFIG_FILE
    options = ConfigParser()
    if not config.exists():
        group = {}
        group['name'] = UNKNOWN
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
    parser.parse_args()
    options = loadconfig()
    notsetup = options['group']['name'] == UNKNOWN
    if (notsetup):
        print('No group set, running init')
        groupname = init(options)
        options['group']['name'] = groupname
        saveconfig(options)
        return
    nomachine = options['machine']['name'] == UNKNOWN
    if (nomachine):
        print('No machine set, adding machine')
        machinename = addmachine(options)
        options['machine']['name'] = machinename
        saveconfig(options)
        return
        
if __name__ == "__main__":
    main()