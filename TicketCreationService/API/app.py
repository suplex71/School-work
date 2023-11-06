import json
from flask import Flask, jsonify, request
from Credentials import storecreds as cfg
from Cleaning_Aggregate.Cleaning import Cleaning

class CleaningListener:
    def __init__(self):
        self.ip_address = cfg.httprequests["cleaning_ms"]
        self.app = Flask(__name__)
        self.port = cfg.httprequests["cleaning_port"]
        self.ms = Cleaning()

        @self.app.route('/start', methods=['POST'])
        def start_ms():
            self.ms._fetch_data_loop_cleaning()
            print("#[Cleaning_API]: Microservices started")
            return 'OK'
        
        @self.app.route('/gettickets', methods=['GET'])
        def get_data():
            data = self.ms.get_tickets()
            data_list = []
            for document in data:
                # Convert ObjectId to string
                document['_id'] = str(document['_id'])
                data_list.append(document)

            # Convert data_list to JSON
            json_data = json.dumps(data_list)
            return json_data


    def start_listening(self):
        print(f"#[Cleaning_MS]: Listening on {self.ip_address}/{self.port}...\n")
        self.app.run(host=self.ip_address, port=self.port)  # Specify the desired port        

