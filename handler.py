from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
from utilis import delay
from machines import Machines
from request_sender import RequestSender
import socket
import json


class MyHandler(BaseHTTPRequestHandler):
    machines = []
    slaves = []
    hash = ''
    working = False

    def do_GET(self):
        url = urlparse(self.path)

        if url.path == '/crack':
            query = parse_qs(url.query)
            if 'md5' in query:
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()

                self.hash = query['md5']
                self.machines = Machines.get_machines()

                q = {'sendip': '127.0.0.1', 'sendport': str(self.server.server_port), 'ttl': '4',
                     'id': 'kuusepuukuller'}
                # q['sendip'] = str(socket.gethostbyname(socket.gethostname()))

                self.wfile.write(bytes('Starting calculations\n', 'UTF-8'))

                for machine in self.machines:
                    dest_ip = machine[0]
                    dest_port = machine[1]
                    if dest_ip == q['sendip'] and dest_port == q['sendport']:
                        continue
                    RequestSender.make_resource_request(dest_ip, dest_port, q)

                self.send_assignments()
            else:
                self.send_response(400)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(bytes('No hash given\n', 'UTF-8'))

        if url.path == '/resource':
            q = parse_qs(url.query)

            if not self.check_request_query(q):
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

            self.machines = Machines.get_machines()

            q['ttl'][0] = str(int(q['ttl'][0]) - 1)
            if int(q['ttl'][0]) < 1:
                print('TTL = < 1')
                return

            for machine in self.machines:
                dest_ip = machine[0]
                dest_port = machine[1]
                no_ask = '%s_%s' % (dest_ip, dest_port)

                if no_ask in q['noask'] or dest_ip == q['sendip'][0] and dest_port == q['sendport'][0]:
                    print('not sending to ' + no_ask)
                    continue

                RequestSender.make_resource_request(dest_ip, dest_port, q)

            # self.wfile.write(bytes('Welcome to %s' % self.path, 'UTF-8'))

            if not self.working:
                if 'id' not in q: q['id'] = ['']
                RequestSender.send_resource_reply(q['sendip'][0], q['sendport'][0], my_ip, my_port, q['id'][0], 100)
            else:
                RequestSender.send_resource_reply(q['sendip'][0], q['sendport'][0], my_ip, my_port, q['id'][0], 0)

        return

    def do_POST(self):
        url = urlparse(self.path)

        if url.path == '/resourcereply':
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            data = self.rfile.read(int(self.headers['Content-Length'])).decode('UTF-8')
            if data not in self.slaves:
                self.slaves.append(data)

        if url.path == '/checkmd5':
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            data = self.rfile.read(int(self.headers['Content-Length'])).decode('UTF-8')
            json_data = json.loads(data)

            # TODO: calculada md5, given the range and symbolrange in json_data
            resutl = 'sitaxcoolparool'
            result_code = 0 # 0 - match found, 1 - not found

            my_ip = socket.gethostbyname(socket.gethostname())
            my_port = self.server.server_port

            # for local testing
            my_ip = '127.0.0.1'

            RequestSender.send_md5_result(json_data['ip'], json_data['port'], my_ip, my_port, 'idjo', self.hash, result_code, resutl)

        if url.path == '/answermd5':
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            data = self.rfile.read(int(self.headers['Content-Length'])).decode('UTF-8')
            json_data = json.loads(data)

            if json_data['result'] == 0:
                print('cracked pass: ' + json_data['resultstring'])
                # self.wfile.write(bytes('cracked pass: %s\n' % json_data['resultstring'], 'UTF-8'))

        return

    @staticmethod
    def check_request_query(q):
        if 'sendip' not in q:
            return False
        if 'sendport' not in q:
            return False
        if 'ttl' not in q:
            return False
        return True

    @delay(5.0)
    def send_assignments(self):

        print('slaves: ' + str(self.slaves))

        my_ip = socket.gethostbyname(socket.gethostname())
        my_port = self.server.server_port

        # for local testing
        my_ip = '127.0.0.1'

        for slave in self.slaves:
            slave_json = json.loads(slave)

            # TODO: calculata ranges and symbolrange here

            md5data = {
                'md5': self.hash,
                'ranges': ['asd','dsa','???'], # add real ranges later
                'wildcard': '?', # add real wildcard later
                'symbolrange': [[3, 10], [100, 150]] # add real symbolrange later
            }
            RequestSender.send_md5(slave_json['ip'], slave_json['port'], my_ip, my_port, 'idjo', md5data)

    # def log_request(self, code=None, size=None):
    #     print('Request')
    #
    # def log_message(self, format, *args):
    #     print('Message')
