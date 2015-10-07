import urllib
import http.client
import urllib.request
from urllib.error import URLError
import socket
import json

class RequestSender:

    def sendAnswerMd5(send_ip, send_port, my_ip, my_port, idf, md5data, result_code, resutlt):
        data = {
            'ip': my_ip,
            'port': my_port,
            'id': idf,
            'md5': md5data['md5'],
            'result': result_code,
            'resultstring': resutlt
        }
        json_data = json.dumps(data)

        url = 'http://' + send_ip + ':' + send_port + '/answermd5'
        print(url)
        req = urllib.request.Request(url)
        req.add_header('Content-Type', 'application/json')
        try:
            res = urllib.request.urlopen(req, data=json_data.encode('UTF-8'), timeout=2)
            r = res.read()
            # print(r)
        except URLError as e:
            print('answermd5 : ' + str(e.reason))
        except socket.timeout as e:
            print("Timeout")

        return

    def sendCheckMd5(send_ip, send_port, my_ip, my_port, idf, md5data):
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

        url = 'http://' + send_ip + ':' + send_port + '/checkmd5'
        print(url)
        req = urllib.request.Request(url)
        req.add_header('Content-Type', 'application/json')
        try:
            res = urllib.request.urlopen(req, data=json_data.encode('UTF-8'), timeout=2)
            r = res.read()
            # print(r)
        except URLError as e:
            print('checkmd5 : ' + str(e.reason))
        except socket.timeout as e:
            print("Timeout")

        return

    def sendResourceRequest(ip, port, path, q):
        qs = urllib.parse.urlencode(q, True)
        url = 'http://' + ip + ':' + port + path + '?' + qs

        req = urllib.request.Request(url)
        try:
            res = urllib.request.urlopen(req, timeout=1)
            r = res.read()
            print(r)
        except URLError as e:
            print(str(e.reason))
        except socket.timeout as e:
            print("Timeout")

        return

    def send_resource_reply(send_ip, send_port, my_ip, my_port, idf, resource):
        data = {
            'ip': my_ip,
            'port': my_port,
            'id': idf,
            'resource': resource
        }
        json_data = json.dumps(data)

        url = 'http://' + send_ip + ':' + send_port + '/resourcereply'
        print(url)
        req = urllib.request.Request(url)
        req.add_header('Content-Type', 'application/json')
        try:
            res = urllib.request.urlopen(req, data=json_data.encode('UTF-8'), timeout=2)
            r = res.read()
            # print(r)
        except URLError as e:
            print('resourcereply : ' + str(e.reason))
        except socket.timeout as e:
            print("Timeout")

        return
