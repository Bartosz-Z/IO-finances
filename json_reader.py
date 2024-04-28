import json

class JSONReader:

    def getJsonDict(json_path):
        with open(json_path) as json_file:
            return json.load(json_file)