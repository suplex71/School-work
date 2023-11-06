from flask import Flask, request, jsonify
from Credentials import storecreds as cfg
from Receiver_Microservice.Receiver import Receiver


class ReceiverListener:
    def __init__(self):
        self.ip_address = cfg.httprequests["receiver_ms"]
        self.app = Flask(__name__)
        self.port = cfg.httprequests["receiver_port"]
        self.ms = Receiver()

        @self.app.route('/start', methods=['POST'])
        def start_ms():
            self.ms.start_rabbitmq_consumer()
            print("#[Receiver_API]: Microservices started")
            return 'OK'
        
        @self.app.route('/getdatawithquery', methods=['POST'])
        def get_data_query():
            payload = request.data.decode('utf-8')
            # get the data here
            data = self.ms.getdatawithquery(payload)
            return jsonify(data)
        
        @self.app.route('/getdataonefield', methods=['POST'])
        def get_data_field():
            payload = request.get_json()
            # get the data here
            data = self.ms.getdataonefield(table=payload[0], field=payload[1])
            return jsonify(data)


    def start_listening(self):
        print(f"#[Receiver_MS]: Listening on {self.ip_address}/{self.port}...\n")
        self.app.run(host=self.ip_address, port=self.port)  # Specify the desired port        

