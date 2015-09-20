import json

class FileReader:
    def getFileJSON(filename):
        data = []
        with open(filename) as data_file:
            data = json.load(data_file)
        return data
