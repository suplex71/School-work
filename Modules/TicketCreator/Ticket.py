from datetime import datetime

class Ticket:

    def __init__(self, room, occupancy):
        dt = datetime.now()
        self.timestamp = dt.strftime("%Y-%m-%d %H:%M:%S.%f")[:-2]        
        self.room = room
        self.occupancy = occupancy

    def getTicketAsCollection(self):
        collection = [{"timestamp": self.timestamp, "room": self.room, "occupancy": self.occupancy}]
        return collection
