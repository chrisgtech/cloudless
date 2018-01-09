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
        
def run(reactor):
    log.startLogging(sys.stdout)
    certData = getModule(__name__).filePath.sibling('work-prv.pem').getContent()
    certificate = ssl.PrivateCertificate.loadPEM(certData)
    factory = protocol.Factory.forProtocol(Echo)
    reactor.listenSSL(8000, factory, certificate.options())
    return defer.Deferred()

def main():
    task.react(run)
    
if __name__ == '__main__':
    import server
    server.main()
