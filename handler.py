from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
from utilis import delay
from file_reader import FileReader
from request_sender import RequestSender
import socket


class MyHandler(BaseHTTPRequestHandler):
    machines = []
    slaves = []
    hash = ''
    working = False

    def do_GET(self):
        url = urlparse(self.path)

        if url.path == '/crack':
            query = parse_qs(url.query)
            if 'q' in query:
                self.hash = query['q']
                self.machines = FileReader.get_file_json('machines.txt')

                q = {'sendip': '127.0.0.1', 'sendport': str(self.server.server_port), 'ttl': '4',
                     'id': 'kuusepuukuller'}
                # q['sendip'] = str(socket.gethostbyname(socket.gethostname()))

                for machine in self.machines:
                    dest_ip = machine[0]
                    dest_port = machine[1]
                    if dest_ip == q['sendip'] and dest_port == q['sendport']:
                        continue
                    RequestSender.make_resource_request(dest_ip, dest_port, '/resource', q)

                self.send_assignment()

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

            self.machines = FileReader.get_file_json('machines.txt')

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

                RequestSender.make_resource_request(dest_ip, dest_port, '/resource', q)


            # self.wfile.write(bytes('Welcome to %s' % self.path, 'UTF-8'))

            if not self.working:
                if 'id' not in q: q['id'] = ['']
                RequestSender.send_resource_reply(q['sendip'][0], q['sendport'][0], my_ip, my_port, q['id'][0], 100)

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

    @delay(10.0)
    def send_assignment(self):

        print(self.slaves)

    # def log_request(self, code=None, size=None):
    #     print('Request')
    #
    # def log_message(self, format, *args):
    #     print('Message')
