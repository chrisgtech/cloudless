#! python3

from twisted.internet import ssl, task, protocol, endpoints, defer
from twisted.python.modules import getModule
from twisted.internet.defer import Deferred
from twisted.internet.protocol import ClientFactory
from twisted.protocols.basic import LineReceiver

from twisted.internet import reactor, defer, endpoints
from twisted.internet.endpoints import TCP4ClientEndpoint, connectProtocol
from twisted.protocols.amp import AMP
from twisted.internet.task import deferLater

from server import Info, Cloudless
import security
    
#class CloudClient(AMP):

    #def connectionMade(self):
    #    pass
        #print('Connected')
        #self.callRemote(Divide, numerator=1234, denominator=1)

    #def lineReceived(self, line):
    #    print("receive:", line)
    #    if line == self.end:
    #        self.transport.loseConnection()

    
@defer.inlineCallbacks
def run(reactor, group, machine, remote, host, port):
    print('{} connecting to {}({}) on {}:{}'.format(machine, remote, group, host, port))
    factory = protocol.Factory.forProtocol(Cloudless)
    groupcert = security.loadcert(group, private=False)
    machinecert = security.loadcert(machine, private=True)
    options = ssl.optionsForClientTLS(remote, groupcert, machinecert)
    endpoint = endpoints.SSL4ClientEndpoint(reactor, host, port, options)
    cloudClient = yield endpoint.connect(factory)
    
    result = yield cloudClient.callRemote(Info)
    print(result)
    
    result = yield cloudClient.callRemote(Info, machine='test')
    print(result)
    return
    
    #def trapZero(result):
    #    result.trap(ZeroDivisionError)
    #    print("Divided by zero: returning INF")
    #    return 1e1000
    #divideDeferred.addErrback(trapZero)
    
    #done = defer.Deferred()
    #def cally(reason):
    #    print('connection lost:', reason.getErrorMessage())
    #    done.callback(None)
    #cloudClient.connectionLost = cally
    #yield done

def main(group, machine, remote, host, port):
    task.react(run, (group, machine, remote, host, port))
    
if __name__ == '__main__':
    import client
    client.main('testgroup', 'test', 'test', 'localhost', 80)
