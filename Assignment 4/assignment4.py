import paho.mqtt.client as mqtt
from influxdb import InfluxDBClient
import datetime
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)

broker_address="192.168.1.32"    #broker address (your pis ip address)
dbclient = InfluxDBClient('0.0.0.0', 8086, 'root', 'root', 'mydb')
query = 'select mean("value") from "/light" where "time" > now() - 10s'

def on_message(client, userdata, message):
	print(float(message.payload)) #print incoming messages
	#get current time
	receiveTime = datetime.datetime.utcnow()
	lightValue = float(message.payload)
	#create json to insert into db
	json_body = [
		{
			"measurement": '/light',
			"time": receiveTime,
			"fields": {
				"value": lightValue
			}
		}
	]

	#write to db
	dbclient.write_points(json_body)
	print("Finished writing to InfluxDB")

client = mqtt.Client() #create new client instance
client.connect(broker_address) #connect to broker

client.on_message=on_message #set the on message function

client.subscribe("/light") #subscirbe to topic

client.loop_start() #start client

try:
	while True:   # wait for ctrl-c	
		try:
			result = dbclient.query(query)
			#print (result)   
			light_avg = list(result.get_points(measurement='/light'))[0]['mean']
			print(light_avg)
			if(light_avg < 500):
				GPIO.output(18,GPIO.HIGH)
			else:
				GPIO.output(18,GPIO.LOW)

		except:	
			pass

except KeyboardInterrupt:
	pass

client.loop_stop() #stop client
