from http.server import HTTPServer
from handler import MyHandler
from socketserver import ThreadingMixIn
import sys


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    pass

# argv : -p [port]
#        -h [hash]
def get_argv():
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
    args = get_argv()

    port = 1215
    if 'port' in args:
        port = args['port']

    # print(socket.gethostbyname(socket.gethostname()))
    print('localhost')

    try:
        server = ThreadedHTTPServer(('127.0.0.1', port), MyHandler)
        print('Started http server at port ' + str(port))
        server.serve_forever()
    except KeyboardInterrupt:
        print('^C received, shutting down server')
        server.socket.close()
