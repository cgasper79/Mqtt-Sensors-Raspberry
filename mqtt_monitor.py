#!/usr/bin/env python3

from os import error, path
import random
import time
import yaml
from paho.mqtt import client as mqtt_client
import psutil
import json
import pathlib
import argparse
import datetime

settings = {}

def get_cpu_temp():
    temp = 0
    try:
        t = psutil.sensors_temperatures()
        for x in ['cpu-thermal', 'cpu_thermal', 'coretemp', 'soc_thermal']:
            if x in t:
                temp = t[x][0].current
                break
    except Exception as e:
            print('Could not establish CPU temperature reading: ' + str(e))

    return round(temp, 1)

    #Otra opción para raspberry
    #tempFile = open( "/sys/class/thermal/thermal_zone0/temp" )
    #cpu_temp = tempFile.read()
    #tempFile.close()
    #return float(cpu_temp)/1000

def get_cpu_usage():
    return str(psutil.cpu_percent(interval=None))

def get_memory_usage():
    return str(psutil.virtual_memory().percent)

def get_version_so():
    tempFile = open( "/etc/debian_version")
    version_so = tempFile.read()
    tempFile.close()
    return version_so


def connect_mqtt():

    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
            print (client_id)
        else:
            print("Failed to connect, return code %d\n", rc)
                 
    # Set Connecting Client ID
    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    
    while True:
        try:
            client.connect(broker , port)
            break
        except TimeoutError:
            print('Mqtt Server - TimeOut')
            time.sleep(60)              
        except OSError:
            print ('Mqtt Server - Host Down')
            time.sleep(60)
            
    return client
    
   
def get_last_boot():

    return str(datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%d-%m-%Y %H:%M:%S"))

def publish(client):

    while True:
        datos = {"FW": version ,"Version_SO": get_version_so(),"temperature_cpu": get_cpu_temp(), "cpu_usage": get_cpu_usage(), "memory_usage":get_memory_usage(), "last_boot":get_last_boot()}
        data_out = json.dumps(datos) # encode object to JSON
        time.sleep(random.randint(1,settings ['update_interval']))
        msg = f"{data_out}"
        result = client.publish(topic, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        

if __name__ == '__main__':

    try:
        args = argparse.PARSER().parse_args()
        settings_file = args.settings
    except:
        print('Attempting to find settings file in same folder as ' + str(__file__))
        default_settings_path = str(pathlib.Path(__file__).parent.resolve()) + '/config.yml'
        if path.isfile(default_settings_path):
            print('Config file found, attempting to continue...')
            settings_file = default_settings_path
        else:
            print('Could not find config.yml. Please check the documentation')
            exit()

    with open(settings_file, 'r') as file:
        settings = yaml.load(file, Loader=yaml.FullLoader)

    broker = settings ['mqtt']['broker']
    port = settings ['mqtt']['port']
    username = settings ['mqtt']['username']
    password = settings ['mqtt']['password']
    topic = settings ['mqtt']['topic']
    client_id = settings ['client_id']
    timezone = settings ['timezone'] 
    version = settings ['version_fw']

    client = connect_mqtt()
    client.loop_start()
    publish(client) 
    
    



