from time import sleep
import os
import pika

def get_usage():
    with open("/usage") as usagefile:
        return usagefile.readline().split(" ")[0]

def get_core_count():
    with open("/cpuinfo") as cpuinfofile:
        for line in reversed(cpuinfofile.readlines()):
            print(line, end="")
            if "processor\t" in line:
                print(line[-2])
                return int(line[-2])
    return 1

            
 
def action():
    value = float(get_usage())
    core_count = get_core_count()

    credentials = pika.PlainCredentials(os.environ["USER"],os.environ["PASS"])
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbit.centurionx.net',5672,'/',credentials))
    channel = connection.channel()
    channel.exchange_declare(exchange='Inter',exchange_type='direct',durable=True)

    message = {}

    message["HostName"] = os.environ["HOST"]
    message["Usage"] = str(value/core_count)

    channel.basic_publish(exchange='InterTopic', routing_key='node.usage', body=str(message))
    connection.close()

while(True):
    action()
    sleep(60*5)
