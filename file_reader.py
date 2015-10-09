import json


class FileReader:
    @staticmethod
    def get_file_json(filename):
        data = []
        with open(filename) as data_file:
            data = json.load(data_file)
        return data
