import urllib
import http.client

class RequestSender:
    def sendResourceRequest(self, ip, port, path, q):
        qs = urllib.parse.urlencode(q)
        url = 'http://' + ip + ':' + port + path + '?' + qs

        # urllib.request.urlopen(url).read()

        path_qs = path + '?' + qs
        # print(url)
        #
        conn = http.client.HTTPConnection(ip, port)
        conn.request("GET", path_qs)
        try:
            res = conn.getresponse()
            print(res.status)
        except http.client.BadStatusLine:
            print("BadStatusLine")

        return
