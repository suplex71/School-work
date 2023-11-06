from flask import Flask, request
from Credentials import storecreds as cfg
from Lights_Aggregate.Lights import Lights
class LightListener:
    def __init__(self):
        self.ip_address = cfg.httprequests["light_ms"]
        self.app = Flask(__name__)
        self.port = cfg.httprequests["light_port"]
        self.ms = Lights()

        @self.app.route('/start', methods=['POST'])
        def start_ms():
            self.ms._fetch_data_loop_light()
            print("#[Light_API]: Microservices started")
            return 'OK'
        
        @self.app.route('/getdata', methods=['POST'])
        def get_data():
            # get the data here
            data = "This feature is coming soon..."
            return data

    def start_listening(self):
        print(f"#[Light_MS]: Listening on {self.ip_address}/{self.port}...\n")
        self.app.run(host=self.ip_address, port=self.port)  # Specify the desired port        

