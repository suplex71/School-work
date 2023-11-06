from flask import Flask, request
from Credentials import storecreds as cfg
class BMSListener:
    def __init__(self):
        self.ip_address = cfg.httprequests["bms"]
        self.app = Flask(__name__)
        self.port = cfg.httprequests["bms_port"]

        @self.app.route('/lights', methods=['POST'])
        def handle_request():
            payload = request.form
            self.process_request(payload)
            return 'Request received'

    def process_request(self, payload):
        # Process the request payload
        print(f'#[BMS]: Message received - {payload}\n')
        switch = payload["switch"]
        light_array = payload.getlist('lights')
        if switch == "0" or switch == "1":
            for light in light_array:
                if switch == "1":
                    # turn light on
                    print(f'#[BMS]: Turning on light with ID {light}\n')
                    pass
                elif switch == "0":
                    # turn light off
                    print(f'#[BMS]: Turning off light with ID {light}\n')
                    pass
                else:
                    pass
        else:
             print(f'#[BMS]: Wrong switch value: {switch}\n')
            

        print(light_array)
        print(switch)
        

    def start_listening(self):
        print(f"#[BMS]: Listening on {self.ip_address}/{self.port}...\n")
        self.app.run(host=self.ip_address, port=self.port)  # Specify the desired port        

