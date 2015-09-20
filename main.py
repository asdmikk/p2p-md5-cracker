from http.server import BaseHTTPRequestHandler, HTTPServer
from file_reader import FileReader
from request_sender import RequestSender
from handler import MyHandler
import sys
import socket


# argv : -p [port]
#        -h [hash]
def getArgv():
    args = {}
    if len(sys.argv) < 2:
        return args
    else:
        if '-p' in sys.argv:
            args['port'] = int(sys.argv[sys.argv.index('-p')+1])
        if '-h' in sys.argv:
            args['hash'] =  sys.argv[sys.argv.index('-h')+1]

    return args

if __name__ == "__main__":
    args = getArgv()

    port = 1215
    if 'port' in args:
        port = args['port']

    if 'hash' in args:
        mashines = FileReader.getFileJSON('mashines.txt')
        print(mashines)

        q = {
            'sendip': socket.gethostbyname(socket.gethostname()),
            'sendport': port,
            'ttl': 5
        }
        q['sendip'] = '127.0.0.1'

        for mashine in mashines:
            dest_ip = mashine[0]
            dest_port = mashine[1]
            sender = RequestSender()
            try:
                sender.sendResourceRequest(dest_ip, dest_port, '/resource', q)
            except ConnectionRefusedError:
                print("connection refused: %s:%s" % (dest_ip, dest_port))


    # print(socket.gethostbyname(socket.gethostname()))
    print('localhost')

    try:
        server = HTTPServer(('127.0.0.1', port), MyHandler)
        print('Started http server at port ' + str(port))
        server.serve_forever()
    except KeyboardInterrupt:
        print('^C received, shutting down server')
        server.socket.close()
