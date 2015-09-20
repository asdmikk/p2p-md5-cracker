from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse
from file_reader import FileReader
from request_sender import RequestSender
import socket
import json

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
            q['ttl'][0] = int(q['ttl'][0]) - 1
            q = self.fixQuery(q)
            print(q)

            for mashine in mashines:
                dest_ip = mashine[0]
                dest_port = mashine[1]
                no_ask = '%s_%s' % (dest_ip, dest_port)

                if no_ask in q['noask']:
                    print('not sending to ' + no_ask)
                    continue

                print('sending to ' + dest_port)

                sender = RequestSender()
                try:
                    sender.sendResourceRequest(dest_ip, dest_port, '/resource', q)
                except ConnectionRefusedError:
                    print("connection refused: %s:%s" % (dest_ip, dest_port))


            if False:
                q = parse_qs(url.query)
                res = {}
                res['ip'] = '10.10.10.10'
                res['port'] = '9999'
                res['id'] = 'ididid'
                res['resource'] = 100
                json_data = json.dumps(res)
                print('response: ' + json_data)




        # self.send_response(200)
        # self.send_header("Content-type", "text/html")
        # self.end_headers()

        return

    def do_POST(self):
        print("Just received a POST request")
        url = urlparse(self.path)

        if url.path == '/resourcereply':
            print('resourcereply post')


        return

    def checkRequestQuery(self, q):
        if not 'sendip' in q:
            return False
        if not 'sendport' in q:
            return False
        if not 'ttl' in q:
            return False
        return True

    def fixQuery(self, q):
        q2 = {}
        q2['sendip'] = q['sendip'][0]
        q2['sendport'] = q['sendport'][0]
        q2['ttl'] = q['ttl'][0]
        q2['noask'] = q['noask']
        return q2

    def log_request(self, code=None, size=None):
        print('Request')

    def log_message(self, format, *args):
        print('Message')
