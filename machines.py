import json
import urllib.request
from urllib.error import HTTPError

class Machines:
    @staticmethod
    def get_file_json(filename):
        data = []
        with open(filename) as data_file:
            data = json.load(data_file)
        return data

    @staticmethod
    def get_machines_from_url(url):
        data = []
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode("utf-8"))
        return data

    @staticmethod
    def get_machines(filename='machines.txt', url='http://dijkstra.cs.ttu.ee/~priit/P2MD5.txt'):
        machines = []
        from_file = Machines.get_file_json(filename)
        try:
            from_url = Machines.get_machines_from_url(url)
        except HTTPError:
            from_url = []
        machines = machines + from_file + from_url
        return machines
