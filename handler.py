from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse, urlencode
import urllib
from file_reader import FileReader
from request_sender import RequestSender
import socket
import json
import random

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print("Just received a GET request")
        url = urlparse(self.path)

        if url.path == '/resource':
            print('request to /resource')
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

            mashines = FileReader.getFileJSON('mashines.txt')

            q['ttl'][0] = str(int(q['ttl'][0]) - 1)
            if int(q['ttl'][0]) < 1:
                print('TTL IS < 1, RETURNING')
                return

            for mashine in mashines:
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
                print('ended')

            self.wfile.write(bytes('Welcome to %s' % self.path, 'UTF-8'))

            if not bool(random.getrandbits(1)): # if mashine is currently not calculating
                if 'id' not in q:
                    q['id'] = ['']
                try:
                    RequestSender.send_resource_reply(q['sendip'][0], q['sendport'][0], my_ip, my_port, q['id'][0], 100)
                except ConnectionRefusedError:
                    print("connection refused: %s:%s" % (dest_ip, dest_port))
                print('ended')


        return

    def do_POST(self):
        print("Just received a POST request")
        url = urlparse(self.path)

        if url.path == '/resourcereply':
            print('request to /resourcereply')


        return

    def checkRequestQuery(self, q):
        if not 'sendip' in q:
            return False
        if not 'sendport' in q:
            return False
        if not 'ttl' in q:
            return False
        return True

    def log_request(self, code=None, size=None):
        print('Request')

    def log_message(self, format, *args):
        print('Message')
