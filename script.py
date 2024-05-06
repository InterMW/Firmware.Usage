import os
import socket
import subprocess
import pika
import json
import datetime
from time import sleep
import sys
def system_call(command):
    p = subprocess.Popen([command], stdout=subprocess.PIPE, shell=True)
    return p.stdout.read()

def send_temp(mac)
    printout = str(system_call("vcgencmd measure_temp"))[7:].split("'")[0]

    result = []
    result.append(printout)
    temps = []
    spots = ["CPU"]
    for i in range(len(spots)):
        entry = {}
        entry["Temperature"] = float(result[i])
        entry["PartName"] = spots[i]
        temps.append(entry)
    outbound = {}
    outbound["HostName"] = socket.gethostname()
    outbound["Timestamp"] = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
    outbound["Temperatures"] = temps


    credentials = pika.PlainCredentials(os.environ["user"],os.environ["pass"])
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbit.centurionx.net',5672,'/',credentials))
    channel = connection.channel()
    channel.basic_publish(exchange='InterTopic',
                      routing_key='temperature.node',
                      body=str(outbound))
    connection.close()

 
def action(mac):
    value = float(str(system_call("uptime")).split(" ")[-3][:-1])
    core_count = float(str(system_call("nproc"))[2])
    credentials = pika.PlainCredentials(os.environ["user"],os.environ["pass"])
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbit.centurionx.net',5672,'/',credentials))
    channel = connection.channel()
    channel.exchange_declare(exchange='Inter',exchange_type='direct',durable=True)

    message = {}

    message["HostName"] = mac
    message["Usage"] = str(value/core_count)

    channel.basic_publish(exchange='InterTopic', routing_key='node.usage', body=str(message))
    connection.close()

mac = system_call("ifconfig eth0 | grep -Eo ..\(\:..\){5}")[:-1].decode("utf-8")

while(True):
    action(mac)
    send_temp(mac)
    sleep(60)

