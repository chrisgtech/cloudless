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
        print('Connected')
        #self.callRemote(Divide, numerator=1234, denominator=1)

    #def lineReceived(self, line):
    #    print("receive:", line)
    #    if line == self.end:
    #        self.transport.loseConnection()

    
@defer.inlineCallbacks
def run(reactor, host, port, name, group):
    factory = protocol.Factory.forProtocol(CloudClient)
    certData = getModule(__name__).filePath.sibling('{}.pem'.format(group)).getContent()
    authority = ssl.Certificate.loadPEM(certData)
    options = ssl.optionsForClientTLS(name, authority)
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

def main(host, port , name, group):
    task.react(run, (host, port , name, group))
    
if __name__ == '__main__':
    import client
    client.main('localhost', 8000, 'test', 'test')
