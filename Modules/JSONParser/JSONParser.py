import json

class JSONParser:
    def __init__(self, json_array):
        self.json_array = json_array
        self.parsed_data = []

    def parse_json(self):
        for json_str in self.json_array:
            data = json.loads(json_str)
            self.parsed_data.append(data)

    def get_parsed_data(self):
        return self.parsed_data