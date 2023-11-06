#!/usr/bin/env python
sql_database = {
    "host": "",
    "user": "",
    "passwd": "",
    "db": "",
}
rabbitmq = {
    "host": "localhost",
    "queue": "answer",
    "microservice_queue": "ms_queue"
}
mongo_database = {
    "myclient": "",
    "mydb": "",
    "mycol": ""
}
httprequests = {
    "bms": "", # add more if neccessary
    "bms_port": 5000,

    "gateway": "",
    "gateway_port": 5001,

    # Microservice APIs
    "cleaning_ms": "",
    "cleaning_port": 5002,

    "light_ms": "",
    "light_port": 5003,

    "receiver_ms": "localhost",
    "receiver_port": 5004

}
config = {
    "ticket_time": 20 # put in the time when to check the tickets in a 24 hr format
}