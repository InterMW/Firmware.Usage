import os
import socket
import subprocess
import pika
import json
from time import sleep
import sys
def system_call(command):
    p = subprocess.Popen([command], stdout=subprocess.PIPE, shell=True)
    return p.stdout.read()
 
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

mac = str(system_call("$(ifconfig eth0 | grep -Eo ..\(\:..\){5})"))

while(True):
    action(mac)
    sleep(60)

