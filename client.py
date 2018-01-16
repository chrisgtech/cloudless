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

#class EchoClient(LineReceiver):
#    end = b"Bye-bye!"
#
#    def connectionMade(self):
#        self.sendLine(b"Hello, world!")
#        self.sendLine(b"What a fine day it is.")
#        self.sendLine(self.end)


#    def lineReceived(self, line):
#        print("receive:", line)
#        if line == self.end:
#            self.transport.loseConnection()

#class EchoClientFactory(ClientFactory):
#    protocol = EchoClient

#    def __init__(self):
#        self.done = Deferred()


#    def clientConnectionFailed(self, connector, reason):
#        print('connection failed:', reason.getErrorMessage())
#        self.done.errback(reason)


#    def clientConnectionLost(self, connector, reason):
#        print('connection lost:', reason.getErrorMessage())
#        self.done.callback(None)

#@defer.inlineCallbacks
#def run(reactor, host, port, name, group):
#    factory = protocol.Factory.forProtocol(EchoClient)
#    certData = getModule(__name__).filePath.sibling('{}.pem'.format(group)).getContent()
#    authority = ssl.Certificate.loadPEM(certData)
#    options = ssl.optionsForClientTLS(name, authority)
#    endpoint = endpoints.SSL4ClientEndpoint(reactor, host, port, options)
#    echoClient = yield endpoint.connect(factory)

#    done = defer.Deferred()
#    def cally(reason):
#        print('connection lost:', reason.getErrorMessage())
#        done.callback(None)
#    echoClient.connectionLost = cally
#    yield done

#@defer.inlineCallbacks
def doMath(host, port, name, group):
    #factory = protocol.Factory.forProtocol(EchoClient)
    certData = getModule(__name__).filePath.sibling('{}.pem'.format(group)).getContent()
    authority = ssl.Certificate.loadPEM(certData)
    options = ssl.optionsForClientTLS(name, authority)
    destination = endpoints.SSL4ClientEndpoint(reactor, host, port, options)
    sumDeferred = connectProtocol(destination, AMP())
    def connected(ampProto):
        return ampProto.callRemote(Sum, a=13, b=81)
    sumDeferred.addCallback(connected)
    def summed(result):
        return result['total']
    sumDeferred.addCallback(summed)

    divideDeferred = connectProtocol(destination, AMP())
    def connected(ampProto):
        return ampProto.callRemote(Divide, numerator=1234, denominator=1)
    divideDeferred.addCallback(connected)
    def trapZero(result):
        result.trap(ZeroDivisionError)
        print("Divided by zero: returning INF")
        return 1e1000
    divideDeferred.addErrback(trapZero)

    def done(result):
        print('Done with math:', result)
        reactor.stop()
    defer.DeferredList([sumDeferred, divideDeferred]).addCallback(done)

def main(host, port , name, group):
    doMath(host, port, name, group)
    reactor.run()
    #task.react(run, (host, port , name, group))
    
if __name__ == '__main__':
    import client
    client.main('localhost', 8000, 'test', 'test')
