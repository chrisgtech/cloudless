#! python3
from argparse import ArgumentParser
from configparser import ConfigParser
from pathlib import Path

CONFIG_FILE = Path('cloudless.ini')
UNKNOWN = 'UNKNOWN'

def loadconfig():
    config = CONFIG_FILE
    options = ConfigParser()
    if not config.exists():
        group = {}
        group['name'] = UNKNOWN
        options['group'] = group
        saveconfig(options)
    options.read(config)
    return options
        
def saveconfig(options):
    config = CONFIG_FILE
    with open(config, 'w') as configfile:
        options.write(configfile)
        
def init(options):
    groupname = input('Enter name for new group: ')
    

def main():
    parser = ArgumentParser()
    parser.parse_args()
    options = loadconfig()
    notsetup = options['group']['name'] == UNKNOWN
    if (notsetup):
        print('No group set, running init')
        init(options)
        
if __name__ == "__main__":
    main()