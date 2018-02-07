#! python3

import sys, time

from twisted.internet import protocol, task, defer
from twisted.protocols import amp
from twisted.python import log
from twisted.python.modules import getModule

import security, net, user

global connections
connections = {}

def saveinfo(info):
    options = user.loadconfig()
    remote = info['machine']
    name = 'machine-{}'.format(remote)
    if name in options:
        entry = options[name]
        newtimestamp = info['timestamp']
        oldtimestamp = float(entry['timestamp'])
        if newtimestamp < oldtimestamp:
            return
    print('Saving details for {}'.format(remote))
    options[name] = info
    user.saveconfig(options)

class Info(amp.Command):
    arguments = [(b'machine', amp.Unicode(optional=True))]
    response = [(b'machine', amp.Unicode()), (b'publicip', amp.Unicode()),
                (b'internet', amp.Boolean()), (b'localips', amp.ListOf(amp.Unicode())),
                (b'gateways', amp.ListOf(amp.Unicode())), (b'timestamp', amp.Float())]

class Cloudless(amp.AMP):
    def __init__(self):
        super().__init__()
        options = user.loadconfig()
        self.machine = options['machine']['name']
        
    def addConnection(self, info):
        remote = info['machine']
        print('Adding connection for {}'.format(remote))
        global connections
        connections[remote] = self
    
    @defer.inlineCallbacks   
    def makeConnection(self, transport):
        super().makeConnection(transport)
        print('Made connection')
        info = yield self.callRemote(Info)
        self.addConnection(info)
        saveinfo(info)
        
    def connectionLost(self, reason):
        super().connectionLost(reason)
        print('Lost connection')
    
    def info(self, machine):
        if not machine:
            machine = self.machine
        print('Loading machine info for {}'.format(machine))
        unixtime = time.time()
        info = {'machine': machine, 'publicip': user.UNKNOWN, 'internet': False, 'localips': [], 'gateways': [], 'timestamp': unixtime}
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
    print('{}({}) running server on port {}'.format(machine, group, port))
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
