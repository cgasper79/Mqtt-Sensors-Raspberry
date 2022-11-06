#!/usr/bin/env python3

import random
import time
from paho.mqtt import client as mqtt_client
import json


broker = '192.168.1.140'
port = 1883
topic = "servers/artemisa"
client_id = f'homeassistant-artemisa-{random.randint(0, 1000)}'
username = 'guest'
password = '123456'

def get_cpu_temp():
    tempFile = open( "/sys/class/thermal/thermal_zone0/temp" )
    cpu_temp = tempFile.read()
    tempFile.close()
    return float(cpu_temp)/1000

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
    # Set Connecting Client ID
    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def publish(client):
    
    datos = round(get_cpu_temp())
    data_out = json.dumps(datos) # encode object to JSON
    while True:
        time.sleep(60)
        msg = f"{data_out}"
        result = client.publish(topic, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        
def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)


if __name__ == '__main__':
    run()  



