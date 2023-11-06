from flask import Flask, render_template, request
from Credentials import storecreds as cfg
import requests
from bson import json_util

class GatewayListener:
    def __init__(self):
        self.ip_address = cfg.httprequests["gateway"]
        self.app = Flask(__name__)
        self.port = cfg.httprequests["gateway_port"]

        @self.app.route('/data', methods=['GET', 'POST'])
        def index():
            query = 'SELECT * FROM data'
            response = requests.post(
                f"http://{cfg.httprequests['receiver_ms']}:{cfg.httprequests['receiver_port']}/getdatawithquery",
                data=query
            )
            data_result = response.json()

            response = requests.get(
                 f"http://{cfg.httprequests['cleaning_ms']}:{cfg.httprequests['cleaning_port']}/gettickets"
            )

            ticket_result = response.json()
            print(response.content)
    
            return render_template('index.html', data=data_result, tickets=ticket_result)

        

    def start_listening(self):
        print(f"#[Gateway]: Waiting for connections on {self.ip_address}/{self.port}...\n")
        self.app.run(host=self.ip_address, port=self.port)  # Specify the desired port        

