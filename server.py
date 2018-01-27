#! python3

import sys
from pathlib import Path

from twisted.internet import ssl, protocol, task, defer
from twisted.protocols import amp
from twisted.python import log
from twisted.python.modules import getModule

class Sum(amp.Command):
    arguments = [(b'a', amp.Integer()),
                 (b'b', amp.Integer())]
    response = [(b'total', amp.Integer())]


class Divide(amp.Command):
    arguments = [(b'numerator', amp.Integer()),
                 (b'denominator', amp.Integer())]
    response = [(b'result', amp.Float())]
    errors = {ZeroDivisionError: b'ZERO_DIVISION'}


class Cloudless(amp.AMP):
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
        
def run(reactor, group, machine, port):
    log.startLogging(sys.stdout)
    grouppath = Path('{}.pem'.format(group))
    groupcontent = grouppath.read_text()
    machinepath = Path('{}-prv.pem'.format(machine))
    machinecontent = machinepath.read_text()
    
    groupcert = ssl.Certificate.loadPEM(groupcontent)
    machinecert = ssl.PrivateCertificate.loadPEM(machinecontent)
    factory = protocol.Factory.forProtocol(Cloudless)
    reactor.listenSSL(port, factory, machinecert.options(groupcert))
    return defer.Deferred()

def main(group, machine, port):
    task.react(run, (group, machine, port))
    
if __name__ == '__main__':
    import server
    server.main('testgroup', 'test', 80)
