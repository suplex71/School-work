import mysql.connector

class DataReader:
    def __init__(self):
        self.connection = None

    def connect(self):

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

    def read_data_from_database(self, table_name, criteria=None, field_to_match=None): 
    
        #created a cursor object to execute SQL queries on the database
        cursor = self.connection.cursor()

        #customize the query 
        if(criteria == None):
            query = f"SELECT * FROM {table_name}" 
        else:
            query = f"SELECT * FROM {table_name} WHERE {field_to_match} = {criteria}" 
        cursor.execute(query)
        rows = cursor.fetchall()

        # an empty list to store the retrieved data
        data = []
        for row in rows:
            data.append(row)

        cursor.close()

        return data
    
    def custom_query(self, query):
        #created a cursor object to execute SQL queries on the database
        cursor = self.connection.cursor()

        cursor.execute(query)
        rows = cursor.fetchall()

        # an empty list to store the retrieved data
        data = []
        for row in rows:
            data.append(row)

        cursor.close()

        return data

    def get_single_field(self, table_name, field):
        #created a cursor object to execute SQL queries on the database
        cursor = self.connection.cursor()

        cursor.execute(f"SELECT {field} FROM {table_name}")
        rows = cursor.fetchall()

        # an empty list to store the retrieved data
        data = []
        for row in rows:
            data.append(row)

        cursor.close()

        return data

#function to establish connection to the database
