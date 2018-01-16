#! python3

import sys

from twisted.internet import ssl, protocol, task, defer
from twisted.python import log
from twisted.python.modules import getModule

class Echo(protocol.Protocol):
    def dataReceived(self, data):
        """
        As soon as any data is received, write it back.
        """
        self.transport.write(data)
        
def run(reactor, port, name):
    log.startLogging(sys.stdout)
    certData = getModule(__name__).filePath.sibling('{}-prv.pem'.format(name)).getContent()
    certificate = ssl.PrivateCertificate.loadPEM(certData)
    factory = protocol.Factory.forProtocol(Echo)
    reactor.listenSSL(port, factory, certificate.options())
    return defer.Deferred()

def main(port, name):
    task.react(run, (port, name))
    
if __name__ == '__main__':
    import server
    server.main(8000, 'test')
