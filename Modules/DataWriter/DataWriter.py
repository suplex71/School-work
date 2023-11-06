import mysql.connector
import json

class DataWriter:
    def __init__(self):
        self.connection = None

    def connect(self):
        # Replace the connection parameters with your specific MySQL database details
        from Credentials import storecreds as cfg

        db_host = cfg.sql_database["host"]
        db_user = cfg.sql_database["user"]
        db_password = cfg.sql_database["passwd"]
        db_name = cfg.sql_database["db"]

        # Establish the database connection
        self.connection = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
        )

    def disconnect(self):
        if self.connection:
            self.connection.close()


    def insert_data(self, sensor_id, direction, timestamp):
        query = '''
        INSERT INTO data (timestamp, sensor_id, direction) VALUES (%s, %s, %s)
        '''
        values = (timestamp, sensor_id, direction)
        self.connection.cursor().execute(query, values)
        self.connection.commit()

    def write_data(self, data):
            sensor_id = data.get('unit_id')
            direction = data.get('direction')
            timestamp = data.get('timestamp')
            self.insert_data(sensor_id=sensor_id, direction=direction, timestamp=timestamp)

    def write_json_data(self, json_str):
        parsed_data = json.loads(json_str)
        self.connect()
        # self.create_table()
        self.write_data(parsed_data)
        self.disconnect()
        return parsed_data
