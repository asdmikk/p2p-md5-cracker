import urllib
import urllib.request
from urllib.error import URLError
import socket
import json


class RequestSender:

    @staticmethod
    def send_md5_result(send_ip, send_port, my_ip, my_port, idf, md5, result_code, resutlt, path='/answermd5'):
        data = {
            'ip': my_ip,
            'port': my_port,
            'id': idf,
            'md5': md5,
            'result': result_code,
            'resultstring': resutlt
        }
        json_data = json.dumps(data)

        url = 'http://' + send_ip + ':' + str(send_port) + path
        req = urllib.request.Request(url)
        req.add_header('Content-Type', 'application/json')
        try:
            res = urllib.request.urlopen(req, data=json_data.encode('UTF-8'), timeout=2)
            r = res.read()
        except URLError as e:
            print('answermd5 : ' + str(e.reason))
        except socket.timeout as e:
            print("Send md5 result Timeout")

        return

    @staticmethod
    def send_md5(send_ip, send_port, my_ip, my_port, idf, md5data, path='/checkmd5'):
        data = {
            'ip': my_ip,
            'port': my_port,
            'id': idf,
            'md5': md5data['md5'],
            'ranges': md5data['ranges'],
            'wildcard': md5data['wildcard'],
            'symbolrange': md5data['symbolrange']
        }
        json_data = json.dumps(data)

        url = 'http://' + send_ip + ':' + str(send_port) + path
        req = urllib.request.Request(url)
        req.add_header('Content-Type', 'application/json')
        try:
            res = urllib.request.urlopen(req, data=json_data.encode('UTF-8'), timeout=0.1)
            r = res.read()
        except URLError as e:
            print('checkmd5 : ' + str(e.reason))
        except socket.timeout as e:
            1 == 1
            # print("Send md5 Timeout")

        return

    @staticmethod
    def make_resource_request(ip, port, q, path='/resource'):
        qs = urllib.parse.urlencode(q, True)
        url = 'http://' + ip + ':' + port + path + '?' + qs
        print('Making resource request to http://' + ip + ':' + port)
        req = urllib.request.Request(url)
        try:
            res = urllib.request.urlopen(req, timeout=1)
            r = res.read()
        except URLError as e:
            print(str(e.reason) + ' : http://' + ip + ':' + port)
        except socket.timeout:
            print('Timeout http://' + ip + ':' + port)

        return

    @staticmethod
    def send_resource_reply(send_ip, send_port, my_ip, my_port, idf, resource, path='/resourcereply'):
        data = {
            'ip': my_ip,
            'port': my_port,
            'id': idf,
            'resource': resource
        }
        json_data = json.dumps(data)

        url = 'http://' + send_ip + ':' + send_port + path

        print('Sending resource reply ' + str(resource) + ' to http://' + send_ip + ':' + send_port)
        req = urllib.request.Request(url)
        req.add_header('Content-Type', 'application/json')
        try:
            res = urllib.request.urlopen(req, data=json_data.encode('UTF-8'), timeout=2)
            r = res.read()
        except URLError as e:
            print(str(e.reason) + ' : http://' + send_ip + ':' + send_port)
        except socket.timeout as e:
            print('Timeout http://' + send_ip + ':' + send_port)

        return
