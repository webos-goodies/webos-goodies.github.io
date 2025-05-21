#! /usr/bin/env python3

import ssl
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import PurePath


CERT_DIR = PurePath('/Users/ito/projects/deen/secrets_deploy/development/sourcewalker_com')


class DevHttpRequestHandler(SimpleHTTPRequestHandler):

  def __init__(self, request, client_address, server, **kwargs):
    if (directory := getattr(server, 'directory', None)):
      kwargs.setdefault('directory', directory)
    super(DevHttpRequestHandler, self).__init__(request, client_address, server, **kwargs)

  def end_headers(self):
    self.send_my_headers()
    SimpleHTTPRequestHandler.end_headers(self)

  def send_my_headers(self):
    self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
    self.send_header("Pragma", "no-cache")
    self.send_header("Expires", "0")


class DevHttpServer(HTTPServer):

  def __init__(self, address='', port=8080, directory=None, ctx=None):
    super(DevHttpServer, self).__init__((address, port), DevHttpRequestHandler)
    self.directory = directory
    if ctx is not None: self.socket = ctx.wrap_socket(self.socket)


def start_dev_https_server(address='0.0.0.0', port=8080, directory=None):
  ctx  = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
  ctx.load_cert_chain(str(CERT_DIR / 'full_chain.pem'), keyfile=str(CERT_DIR / 'domain.key'))
  ctx.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1
  server = DevHttpServer(address, port, directory, ctx)
  server.serve_forever()


def main():
  start_dev_https_server()
  #start_dev_https_server(directory=str(ROOT_DIR))


main()
