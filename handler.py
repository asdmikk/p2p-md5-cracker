from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse, urlencode
import urllib
from file_reader import FileReader
from request_sender import RequestSender
import socket
import json
import random
import time
import cgi

class MyHandler(BaseHTTPRequestHandler):
    # def __init__(self):
    #     super(MyHandler, self).__init__()
    #     # self.master = False

    mashines = []
    slaves = []

    def do_GET(self):
        url = urlparse(self.path)

        if url.path == '/crack':
            query = parse_qs(url.query)
            if 'q' in query:
                self.mashines = FileReader.getFileJSON('mashines.txt')
                q = {
                    'sendip': str(socket.gethostbyname(socket.gethostname())),
                    'sendport': str(self.server.server_port),
                    'ttl': '2',
                    'id': 'kuusepuukuller'
                }
                q['sendip'] = '127.0.0.1'

                for mashine in self.mashines:
                    dest_ip = mashine[0]
                    dest_port = mashine[1]
                    if dest_ip == q['sendip'] and dest_port == q['sendport']:
                        continue
                    try:
                        RequestSender.sendResourceRequest(dest_ip, dest_port, '/resource', q)
                    except ConnectionRefusedError:
                        print("connection refused: %s:%s" % (dest_ip, dest_port))

        if url.path == '/resource':
            print('GET to /resource')
            q = parse_qs(url.query)

            if not self.checkRequestQuery(q):
                self.send_response(400)
                self.end_headers()
                return

            self.send_response(200)
            self.end_headers()

            my_ip = socket.gethostbyname(socket.gethostname())
            my_port = self.server.server_port

            # for local testing
            my_ip = '127.0.0.1'

            if 'noask' in q:
                q['noask'].append("%s_%s" % (my_ip, my_port))
            else:
                q['noask'] = ["%s_%s" % (my_ip, my_port)]

            self.mashines = FileReader.getFileJSON('mashines.txt')

            q['ttl'][0] = str(int(q['ttl'][0]) - 1)
            if int(q['ttl'][0]) < 1:
                print('TTL IS < 1, RETURNING')
                return

            for mashine in self.mashines:
                dest_ip = mashine[0]
                dest_port = mashine[1]
                no_ask = '%s_%s' % (dest_ip, dest_port)

                if no_ask in q['noask'] or dest_ip == q['sendip'][0] and dest_port == q['sendport'][0]:
                    print('not sending to ' + no_ask)
                    continue

                print('sending to port ' + dest_port)

                try:
                    RequestSender.sendResourceRequest(dest_ip, dest_port, '/resource', q)
                except ConnectionRefusedError:
                    print("connection refused: %s:%s" % (dest_ip, dest_port))

            # self.wfile.write(bytes('Welcome to %s' % self.path, 'UTF-8'))

            random_bool = bool(random.getrandbits(1))

            if True:
                if 'id' not in q:
                    q['id'] = ['']
                try:
                    RequestSender.send_resource_reply(q['sendip'][0], q['sendport'][0], my_ip, my_port, q['id'][0], 100)
                except ConnectionRefusedError:
                    print("connection refused: %s:%s" % (dest_ip, dest_port))



        return

    def do_POST(self):
        url = urlparse(self.path)

        if url.path == '/resourcereply':
            print('POST to /resourcereply')

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            data = self.rfile.read(int(self.headers['Content-Length'])).decode('UTF-8')
            self.slaves.append(data)

            print(data)

        return

    def checkRequestQuery(self, q):
        if not 'sendip' in q:
            return False
        if not 'sendport' in q:
            return False
        if not 'ttl' in q:
            return False
        return True

    # def log_request(self, code=None, size=None):
    #     print('Request')
    #
    # def log_message(self, format, *args):
    #     print('Message')
