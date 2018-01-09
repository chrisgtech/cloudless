#! python3

from OpenSSL import crypto, SSL
from uuid import uuid4

def certgen(name, root=None):
    private = crypto.PKey()
    private.generate_key(crypto.TYPE_RSA, 4096)
    cert = crypto.X509()
    subject = cert.get_subject()
    subject.C = 'NA'
    subject.ST = 'N/A'
    subject.L = 'N/A'
    subject.O = 'N/A'
    subject.OU = 'N/A'
    subject.CN = name
    uuid = uuid4().int
    cert.set_serial_number(uuid)
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(68*365*24*60*60)
    rootcert = cert
    rootkey = private
    if root:
        with open('{}.pem'.format(root), "rb") as pemfile:
            rootcert = crypto.load_certificate(crypto.FILETYPE_PEM, pemfile.read())
        with open('{}-prv.pem'.format(root), "rb") as pemfile:
            rootkey = crypto.load_privatekey(crypto.FILETYPE_PEM, pemfile.read())
    cert.set_issuer(rootcert.get_subject())
    cert.set_pubkey(private)
    cert.sign(rootkey, 'sha256')

    with open('{}.pem'.format(name), "wb") as pemfile:
        pemfile.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
    with open('{}-prv.pem'.format(name), "wb") as pemfile:
        pemfile.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
        pemfile.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, private))
        