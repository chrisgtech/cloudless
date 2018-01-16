#! python3

import sys

from twisted.internet import ssl, protocol, task, defer
from twisted.protocols import amp
from twisted.python import log
from twisted.python.modules import getModule

#class Echo(protocol.Protocol):
#    def dataReceived(self, data):
#        """
#        As soon as any data is received, write it back.
#        """
#        self.transport.write(data)

class Sum(amp.Command):
    arguments = [(b'a', amp.Integer()),
                 (b'b', amp.Integer())]
    response = [(b'total', amp.Integer())]


class Divide(amp.Command):
    arguments = [(b'numerator', amp.Integer()),
                 (b'denominator', amp.Integer())]
    response = [(b'result', amp.Float())]
    errors = {ZeroDivisionError: b'ZERO_DIVISION'}


class Math(amp.AMP):
    def sum(self, a, b):
        total = a + b
        print('Did a sum: %d + %d = %d' % (a, b, total))
        return {'total': total}
    Sum.responder(sum)

    def divide(self, numerator, denominator):
        result = float(numerator) / denominator
        print('Divided: %d / %d = %f' % (numerator, denominator, result))
        return {'result': result}
    Divide.responder(divide)
        
def run(reactor, port, name):
    log.startLogging(sys.stdout)
    certData = getModule(__name__).filePath.sibling('{}-prv.pem'.format(name)).getContent()
    certificate = ssl.PrivateCertificate.loadPEM(certData)
    factory = protocol.Factory.forProtocol(Math)
    reactor.listenSSL(port, factory, certificate.options())
    return defer.Deferred()

def main(port, name):
    task.react(run, (port, name))
    
if __name__ == '__main__':
    import server
    server.main(8000, 'test')
