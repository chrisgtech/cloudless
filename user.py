#! python3
from configparser import ConfigParser
from pathlib import Path
from io import StringIO

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
    content = config.read_text()
    options.read_string(content)
    return options
    
def saveconfig(options):
    config = CONFIG_FILE
    with StringIO() as writer:
        options.write(writer)
        content = writer.getvalue()
        config.write_text(content)

def prompt(text):
    return input(text)
    
