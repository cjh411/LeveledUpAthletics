import paho.mqtt.client as mqtt
from sklearn.externals import joblib
import pandas as pd
import datetime
import time
from sys import argv
exercise='bcurl'
readings, i, index=40, 0, []
columns=['x','y','z','gyro','id','reading']
reptime=time.time()
while i < readings:
    i+=1
    index.append(i)
rep=0
n=0


input_val=pd.DataFrame(index=index,columns=columns).fillna(0)

#model_path1='/Users/elizabethvassallo/Documents/Recess/rep_models/models/spress/spress_rf_out.pkl'
model_path2='/Users/christopherhedenberg/Documents/Recess/rep_models/models/%s/%s_rf_out.pkl' %(exercise,exercise)
#clf1=joblib.load(model_path1)
clf2=joblib.load(model_path2)


date=str(datetime.datetime.today()).replace(" ","_").replace("/","_").replace(".","_").replace("-","_").replace(":","_")
exercise='bcurl'


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("levelup/accel/band1")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    global n
    global reptime
    data = msg.payload
    data_out=data.decode("utf-8") 
    data_out=[float(i) for i in data.decode("utf-8").split(',')]
    data_out=data_out[:4]
    data_out.append(1)
    data_out.append(1)
    input_val.iloc[1:,:]=input_val.shift().iloc[1:,:]
    input_val.iloc[0]=data_out
    input_val['id']=1
    input_val['reading']=index
#    print (input_val)
#    print (data_out)
#
    if clf2.predict(pd.pivot_table(input_val,index='id', columns='reading',values=['x','y','z','gyro']))[0]==1:
        print("rep counted")
#        input_val.iloc[:,:]=0


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("192.168.1.100", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()



    
    
    