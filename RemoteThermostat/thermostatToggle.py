import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time

broker_address="192.168.1.22"    #broker address (your pis ip address)

#setup board
GPIO.setmode(GPIO.BCM)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)
GPIO.output(16,GPIO.HIGH)
GPIO.output(21,GPIO.HIGH)

def on_message(client, userdata, message):
	print(message.topic + " " + str(message.payload)) #print incoming messages
	if message.topic == '/thermo':
		print("received message with topic thermo")
		print(message.payload)
		if "up" in str(message.payload):
			print("turned temperature up")
			GPIO.output(16,GPIO.LOW)
			time.sleep(.25)
			GPIO.output(16,GPIO.HIGH)
			time.sleep(.5)
			print("got here")
		if "down" in str(message.payload):
			print("turned temperature down")
			GPIO.output(21,GPIO.LOW)
			time.sleep(.25)
			GPIO.output(21,GPIO.HIGH)
			time.sleep(.5)

client = mqtt.Client() #create new client instance
client.connect(broker_address) #connect to broker

client.on_message=on_message #set the on message function

client.subscribe("/thermo") #subscribe to topic

client.loop_start() #start client

try:
	while True:   # wait for ctrl-c
		pass

except KeyboardInterrupt:
	pass

client.loop_stop() #stop client
