# !bin/env python3
# Author(s): cryptopal85
#
# Version history: May 26 2022 - initialising the broker topic structure
#                  Placeholder - placeholder
#
# Notes: 'topic.py' =>> the broker uses the topic of a message to decide which client receives which message
# for more information about topics refer to the =>> https://mosquitto.org/man/mqtt-7.html and
# https://www.hivemq.com/blog/mqtt-essentials-part-5-mqtt-topics-best-practices/

import time
import json
import random
import threading
from abc import ABC, abstractmethod
import paho.mqtt.client as mqtt


# AbstractMethod =>> https://docs.python.org/3.10/library/abc.html#abc.abstractmethod
# define and parse configs
class Topic(ABC):
	def __init__(self, broker_url, broker_port, topic_url, topic_data, retain_probability):
		self.broker_url = broker_url
		self.broker_port = broker_port
		self.topic_url = topic_url
		self.topic_data = topic_data
		self.retain_probability = retain_probability
		self.client = None
		
	# establish a connection between the broker and smart devices or sensors
	def connect(self):
		self.client = mqtt.Client(self.topic_url, clean_session=True, transport='tcp')
		self.client.on_publish = self.on_publish
		self.client.connect(self.broker_url, self.broker_port)
		self.client.loop_start()
		
	@abstractmethod
	def run(self):
		pass
		
	def disconnect(self):
		self.client.lood_end()
		self.client.disconnect()
		
	# display publish data on a terminal based on 'H:M:S' format
	def on_publish(self, client, userdata, result):
		print(f'[{time.strftime("%H:%M:%S")}] Data published on: {self.topic_url}')
		
		
class TopicAuto(Topic, threading.Thread):
	def __init__(self, broker_url, broker_port, topic_url, topic_data, retain_probability, time_interval):
		Topic.__init__(self, broker_url, broker_port, topic_url, topic_data, retain_probability)
		threading.Thread.__init__(self, args=(), kwargs=None)
		self.time_interval = time_interval
		self.old_payload = None
		
	def run(self):
		self.connect()
		while True:
			payload = self.generate_data()
			self.old_payload = payload
			self.client.publish(topic=self.topic_url, payload=json.dumps(payload), qos=2, retain=False)
			time.sleep(self.time_interval)
			
	def generate_data(self):
		payload = {}
		
		if self.old_payload == None:
			# populate initial data
			for data in self.topic_data:
				if data['TYPE'] == 'int':
					payload[data['NAME']] = random.randint(data['MIN_VALUE'], data['MAX_VALUE'])
				elif data['TYPE'] == 'float':
					payload[data['NAME']] = random.uniform(data['MIN_VALUE'], data['MAX_VALUE'])
				elif data['TYPE'] == 'bool':
					payload[data['NAME']] = random.choice([True, False])
		else:
			# populate next data
			payload = self.old_payload
			for data in self.topic_data:
				if random.random() > (1 - self.retain_probability):
					continue
				if data['TYPE'] == 'bool':
					payload[data['NAME']] = not payload[data['NAME']]
				else:
					step = random.uniform(-data['MAX_STEP'], data['MAX_STEP'])
					step = round(step) if data['TYPE'] == 'int' else step
					payload[data['NAME']] = max(payload[data["NAME"]]+step, data['MIN_VALUE']) if step < 0 else min(payload[data['NAME']]+step, data['MAX_VALUE'])
					
		return payload