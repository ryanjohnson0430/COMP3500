import paho.mqtt.client as mqtt
import time
import RPi.GPIO as GPIO

#setup board
GPIO.setmode(GPIO.BCM)

#setup pin as input
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(18, GPIO.OUT)

clickedflag = False

broker_address="192.168.1.22" #broker address (your pis ip address)

def on_message(client, userdata, message):
	print(message.topic + " " + str(message.payload)) #print incoming messages
	lightstate = GPIO.input(18)
	if (lightstate):
		GPIO.output(18,GPIO.LOW)
	else:
		GPIO.output(18,GPIO.HIGH)
		

client = mqtt.Client() #create new mqtt client instance

client.connect(broker_address) #connect to broker

client.on_message=on_message #set the on message function

client.subscribe("/test") #subscirbe to topic

client.loop_start() #start client

while True:	

	#get button state
	buttonstate = GPIO.input(21)

	#if the button is pressed and was not previously clicked
	if (buttonstate and not clickedflag):
		#set as clicked
		clickedflag = True;

	#if button is not clicked and was previously not clicked 
	if (not buttonstate and clickedflag):
		#set as not clicked
		clickedflag = False;

		#print
		print ('clicked')
		#send a message to toggle the LED
		client.publish("/led","toggle")

client.loop_stop() #stop client