import paho.mqtt.client as mqtt
import time

def on_msg(c,u,m):
    print(str(m.topic), m.payload.decode('utf-8'))

def on_connect(c,u,f,rc):
    print('connected',rc)

client=mqtt.Client()
client.on_message=on_msg
client.on_connect=on_connect

client.connect('test.mosquitto.org',1883)
client.loop_start()
subtop=input('subscriber')
pubtop=input('pubtop')
client.subscribe(subtop)
while(1):
    chat=input('Enter your message--')
    if(chat=='q'):
        break
    else:
        client.publish(pubtop,chat)
client.loop_stop()
