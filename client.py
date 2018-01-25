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
from server import Sum, Divide
    
class CloudClient(AMP):

    def connectionMade(self):
        pass
        #print('Connected')
        #self.callRemote(Divide, numerator=1234, denominator=1)

    #def lineReceived(self, line):
    #    print("receive:", line)
    #    if line == self.end:
    #        self.transport.loseConnection()

    
@defer.inlineCallbacks
def run(reactor, group, machine, remote, host, port):
    factory = protocol.Factory.forProtocol(CloudClient)
    machinecontent = getModule(__name__).filePath.sibling('{}-prv.pem'.format(machine)).getContent()
    groupcontent = getModule(__name__).filePath.sibling('{}.pem'.format(group)).getContent()
    machinecert = ssl.PrivateCertificate.loadPEM(machinecontent)
    groupcert = ssl.Certificate.loadPEM(groupcontent)
    options = ssl.optionsForClientTLS(machine, groupcert, machinecert)
    endpoint = endpoints.SSL4ClientEndpoint(reactor, host, port, options)
    cloudClient = yield endpoint.connect(factory)
    print('connected!')
    
    result = yield cloudClient.callRemote(Sum, a=13, b=81)
    print(result['total'])
    
    result = yield cloudClient.callRemote(Divide, numerator=1234, denominator=1)
    print(result['result'])
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
