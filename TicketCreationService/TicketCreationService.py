from Modules.DataWriterMongo.DataWriterMongo import DataWriterMongo
from Modules.MongoDBReader.MongoDBReader import MongoDBReader
from Modules.TicketCreator.Ticket import Ticket
from Credentials import storecreds as cfg
import requests


class TicketCreationService:

    def _fetch_data_trigger_cleaning(self):
        import time
        import datetime

        response = requests.post(
            f"http://{cfg.httprequests['receiver_ms']}:{cfg.httprequests['receiver_port']}/getdataonefield",
            json=["Room", "ID"]
        )
        room_array = response.json()
        rooms = []
        for row in room_array:
            for room in row:
                rooms.append(room)

        while True:
            current_time = datetime.datetime.now().time()
            target_time = datetime.time(cfg.config["ticket_time"], 0)  # 20:00

            # self.check_for_ticket() # just for testing

            if current_time >= target_time:
                self.check_for_ticket(rooms=rooms)
                # Sleep for 24 hours before checking again
                time.sleep(24 * 60 * 60)
            else:
                # Calculate the time remaining until 20:00
                time_remaining = (
                    datetime.datetime.combine(datetime.date.today(), target_time)
                    - datetime.datetime.now()
                )
                # Sleep until 20:00
                time.sleep(time_remaining.total_seconds())
            
    def check_for_ticket(self, rooms):
        # check if total people entering per room has passed 20
        # for each room
        for room in rooms:
            # build the query
            query = f"SELECT COUNT(*) AS total_rows FROM data d JOIN Sensor s ON d.sensor_id = s.ID JOIN Room r ON s.room_id = r.ID WHERE d.direction = 'in' AND r.ID = '{room}' AND DATE(d.timestamp) = CURDATE();;"
            # run the query
            response = requests.post(
                f"http://{cfg.httprequests['receiver_ms']}:{cfg.httprequests['receiver_port']}/getdatawithquery",
                data=query
            )
            count_array = response.json()
            for row in count_array:
                for count in row:
                    count = count
            # check if the value is over 20
            if count > 20:
                # ticket needs to be sent
                # create ticket
                print(
                    f"#[Calculator]: Occupancy for room {room} surpassed the limit. Creating ticket...\n"
                )
                ticket = Ticket(room=room, occupancy=count)
                dataToWrite = ticket.getTicketAsCollection()
                mongowriter = DataWriterMongo()
                mongowriter.insert_ticket(dataToWrite)
            else:
                print(
                    f"#[Cleaning]: Occupancy for room {room} is below the limit. Passing room...\n"
                )

    def get_tickets(self):
        mr = MongoDBReader()
        data = mr.read_tickets()
        return data