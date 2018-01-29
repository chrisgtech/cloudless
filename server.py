#! python3

import sys

from twisted.internet import protocol, task, defer
from twisted.protocols import amp
from twisted.python import log
from twisted.python.modules import getModule

import security, net, user

class Info(amp.Command):
    arguments = [(b'machine', amp.Unicode())]
    response = [(b'publicip', amp.Unicode()), (b'internet', amp.Boolean()),
                (b'localips', amp.ListOf(amp.Unicode())), (b'gateways', amp.ListOf(amp.Unicode()))]

class Cloudless(amp.AMP):
    def __init__(self):
        super().__init__()
        self.options = user.loadconfig()
        self.machine = self.options['machine']['name']
    
    def info(self, machine):
        print('Loaded machine info for {}'.format(machine))
        info = {'publicip': user.UNKNOWN, 'internet': False, 'localips': [], 'gateways': []}
        if machine == self.machine:
            print('Getting local info')
            info['publicip'] = net.publicip()
            info['internet'] = net.internet()
            info['localips'] = net.localips()
            info['gateways'] = net.gateways()
        else:
            pass
        return info
    Info.responder(info)
        
def run(reactor, group, machine, port):
    log.startLogging(sys.stdout)
    groupcert = security.loadcert(group, private=False)
    machinecert = security.loadcert(machine, private=True)
    factory = protocol.Factory.forProtocol(Cloudless)
    reactor.listenSSL(port, factory, machinecert.options(groupcert))
    return defer.Deferred()

def main(group, machine, port):
    task.react(run, (group, machine, port))
    
if __name__ == '__main__':
    import server
    server.main('testgroup', 'test', 80)
