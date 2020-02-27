import paho.mqtt.client as mqtt
from influxdb import InfluxDBClient
from flask import Flask, request, json
from flask_restful import Resource, Api
import datetime

broker_address="192.168.1.13"

client = mqtt.Client()
client.connect(broker_address)

dbclient = InfluxDBClient('0.0.0.0', 8086, 'root', 'root', 'mydb')
query = 'select mean("value") from "/light" where "time" > now() - 10s'

app = Flask(__name__)
api = Api(app)

class Test(Resource):
	def get(self):
		try:
			result = dbclient.query(query)
			#print (result)   
			light_avg = list(result.get_points(measurement='/light'))[0]['mean']
			return light_avg

		except:	
			pass
	
	def post(self):
		value = request.get_data()
		value = json.loads(value)
		if value['device'] == 'pi':
			if value['state'] == 'on':
				client.publish("/piled","on");
				print("piled on published")
			if value['state'] == 'off':
				client.publish("/piled","off");
				print("piled off published")
		if value['device'] == 'esp':
			if value['state'] == 'on':
				client.publish("/espled","on");
			if value['state'] == 'off':
				client.publish("/espled","off");
		
		#return {'hello':value['user']}
	
api.add_resource(Test, '/test')

app.run(host='0.0.0.0', debug=True)
