#!/usr/bin/python3
import json
import time

import django
import paho.mqtt.client as mqtt
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from django.conf import settings
from web.models import Sensor, Colector, SensorType, SensorMeasure

def on_connect(client, userdata, flags, rc):
    client.subscribe("/gustavoguerino2@gmail.com/#")


def on_message(client, userdata, message):
    # print("\n\n\nMessage received " ,str(message.payload.decode("utf-8")))
    # print("Message topic=",message.topic)
    # print("Message qos=",message.qos)
    # print("Message retain flag=",message.retain)

    topics = message.topic.split("/")
    if(len(topics) > 4):
        try:
            colector = Colector.objects.get(identify=topics[2])
        except:
            colector = None
        if colector:
            data = json.loads(str(message.payload.decode("utf-8")))
            sensor_name = topics[3]
            sensor_type = topics[4]
            try:
                sensor_type_obj = SensorType.objects.get(
                    name=sensor_type
                )
            except ObjectDoesNotExist:
                sensor_type_obj = SensorType(
                    name=sensor_type
                ).save()
            try:
                sensor_obj = Sensor.objects.get(
                    name=sensor_name,
                    sensor_type=sensor_type_obj,
                    colector=colector
                )
            except:
                sensor_obj = Sensor(
                    name=sensor_name,
                    sensor_type=sensor_type_obj,
                    colector=colector
                ).save()
            SensorMeasure(
                sensor=sensor_obj,
                measurement_value=data['measurement'],
                unit_of_measurement=data['unit']
            ).save()
            print(data, str(message.payload.decode("utf-8")))
        print(Colector.objects.filter(identify=topics[2]))

def run():
    brokerUserName = "gustavoguerino2@gmail.com"
    brokerPassword = "66db79f5"
    brokerApi = "mqtt.dioty.co"
    brokerPort = 1883

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.username_pw_set(username=brokerUserName, password=brokerPassword)

    client.connect(brokerApi, brokerPort, 60)

    client.loop_start()
    while 1:
        time.sleep(1)
