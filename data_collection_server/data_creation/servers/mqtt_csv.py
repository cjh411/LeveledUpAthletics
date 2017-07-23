import paho.mqtt.client as mqtt
import time 
import datetime
import os

date=str(datetime.datetime.today()).replace(" ","_").replace("/","_").replace(".","_").replace("-","_").replace(":","_")
exercise='press'
testtrain='train'
#weight can be dumbell, barbell, bodyweight, machine
weight='dumbell'
category='shoulder'
#[spress=Shoulder Press, cpress = Chest Press, jmpjck = Jumping Jack, runip,triext,ovhtri]



path='/Users/christopherhedenberg/Documents/Recess/rep_models/data/%s/%s/%s/%s/raw/%s_%s.txt' %(testtrain,category,exercise,weight,exercise,date)
dir = os.path.dirname(path)
if not os.path.exists(dir):
    os.makedirs(dir)
    
rep_file=open(path,'w') 
start=time.time()


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("levelup/accel/band1")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    data = msg.payload
    data_out=data.decode("utf-8") + '\n'
    print (data_out)
    rep_file.write(data_out)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("192.168.1.100", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_start()



    
    