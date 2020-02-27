import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
from influxdb import InfluxDBClient
import datetime

broker_address="192.168.1.13"

GPIO.setmode(GPIO.BCM)
GPIO.setup(18,GPIO.OUT)

def on_message(client, userdata, message):
	#print(message.topic + " " + str(message.payload))
	
	if message.topic == '/light':
		#print(float(message.payload)) #print incoming messages
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
		#print("Finished writing to InfluxDB")	
	
	if message.topic == '/piled':
		print("received message with topic led")
		print(message.payload)
		if "on" in str(message.payload):
			print("received payload on")
			GPIO.output(18,GPIO.HIGH)
		if "off" in str(message.payload):
			print("received payload off")
			GPIO.output(18,GPIO.LOW)
	
client = mqtt.Client()
client.connect(broker_address)

client.on_message=on_message

client.subscribe("/light")
client.subscribe("/piled")

dbclient = InfluxDBClient('0.0.0.0', 8086, 'root', 'root', 'mydb')

client.loop_start()

try:
	while True:
		pass
except KeyboardInterrupt:
	pass
	
client.loop_stop()
GPIO.cleanup()
