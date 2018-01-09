#! python3

from twisted.internet import ssl, task, protocol, endpoints, defer
from twisted.python.modules import getModule
from twisted.internet.defer import Deferred
from twisted.internet.protocol import ClientFactory
from twisted.protocols.basic import LineReceiver

class EchoClient(LineReceiver):
    end = b"Bye-bye!"

    def connectionMade(self):
        self.sendLine(b"Hello, world!")
        self.sendLine(b"What a fine day it is.")
        self.sendLine(self.end)


    def lineReceived(self, line):
        print("receive:", line)
        if line == self.end:
            self.transport.loseConnection()

class EchoClientFactory(ClientFactory):
    protocol = EchoClient

    def __init__(self):
        self.done = Deferred()


    def clientConnectionFailed(self, connector, reason):
        print('connection failed:', reason.getErrorMessage())
        self.done.errback(reason)


    def clientConnectionLost(self, connector, reason):
        print('connection lost:', reason.getErrorMessage())
        self.done.callback(None)

@defer.inlineCallbacks
def run(reactor):
    factory = protocol.Factory.forProtocol(EchoClient)
    certData = getModule(__name__).filePath.sibling('cloudy.pem').getContent()
    authority = ssl.Certificate.loadPEM(certData)
    options = ssl.optionsForClientTLS('work', authority)
    endpoint = endpoints.SSL4ClientEndpoint(reactor, 'localhost', 8000,
                                            options)
    echoClient = yield endpoint.connect(factory)

    done = defer.Deferred()
    def cally(reason):
        print('connection lost:', reason.getErrorMessage())
        done.callback(None)
    echoClient.connectionLost = cally
    yield done

def main():
    task.react(run)
    
if __name__ == '__main__':
    import client
    client.main()
