import time
from Credentials import storecreds as cfg
import requests
import json


class LightRegulationService:

    def _fetch_data_trigger_lights(self):
        response = requests.post(
            f"http://{cfg.httprequests['receiver_ms']}:{cfg.httprequests['receiver_port']}/getdataonefield",
            json=["Room", "ID"]
        )
        room_array = response.json()
        rooms = []
        for row in room_array:
            for room in row:
                rooms.append(room)

        prev_occ = {}
        while True:
            self.check_for_light(rooms, prev_occ=prev_occ)
            time.sleep()
            
    def check_for_light(self, rooms, prev_occ):
        # lets create key_value pairs to make a object we can reference to
        for room in rooms:
            # get the current occupancy
            query = f"SELECT (SELECT COUNT(*) FROM data d INNER JOIN Sensor s ON d.sensor_id = s.ID WHERE s.room_id = '{room}' AND d.direction = 'in' AND DATE(d.timestamp) = CURDATE()) AS in_count, (SELECT COUNT(*) FROM data d INNER JOIN Sensor s ON d.sensor_id = s.ID WHERE s.room_id = '{room}' AND d.direction = 'out' AND DATE(d.timestamp) = CURDATE()) AS out_count;"

            response = requests.post(
                f"http://{cfg.httprequests['receiver_ms']}:{cfg.httprequests['receiver_port']}/getdatawithquery",
                data=query
            )
            result = response.json()
            in_count, out_count = result[0]
            total_count = in_count - out_count
            
            # check if we are in the first cycle or the room even exists to take into the array
            if prev_occ.get(room) == None:
                prev_occ[room] = total_count
            else:
                # check if this count is larger than zero and larger than the old count and make sure the old one is smaller than one
                # if yes, send request to turn on the light
                if total_count > 0 and total_count > prev_occ.get(room) and prev_occ.get(room) <= 0:
                    print(f"#[Calculator]: Turning on light in room {room}...\n")
                    
                    # get all the light_ids for this room
                    query = f"SELECT ID FROM Light WHERE room_id = '{room}'"
                    response = requests.post(
                        f"http://{cfg.httprequests['receiver_ms']}:{cfg.httprequests['receiver_port']}/getdatawithquery",
                        data=query
                    )
                    light_result = response.json()
                    light_ids = []
                    for row in light_result:
                        for id in row:
                            light_ids.append(id)

                    payload = {
                        "switch":1,
                        "lights":light_ids
                    }

                    requests.post(f"http://{cfg.httprequests['bms']}:{cfg.httprequests['bms_port']}/lights", data=payload)
                # check if the count is smaller than zero and smaller than the last one
                elif total_count <= 0 and total_count < prev_occ.get(room):
                    print(f"#[Calculator]: Turning off light in room {room}...\n")

                    # get all the light_ids for this room
                    query = f"SELECT ID FROM Light WHERE room_id = '{room}'"
                    response = requests.post(
                        f"http://{cfg.httprequests['receiver_ms']}:{cfg.httprequests['receiver_port']}/getdatawithquery",
                        data=query
                    )
                    light_result = response.json()
                    light_ids = []
                    for row in light_result:
                        for id in row:
                            light_ids.append(id)
                    
                    payload = {
                        "switch":0,
                        "lights":light_ids
                    }

                    requests.post(f"http://{cfg.httprequests['bms']}:{cfg.httprequests['bms_port']}/lights", data=payload)

            # assign current values to prev_occ
            prev_occ[room] = total_count