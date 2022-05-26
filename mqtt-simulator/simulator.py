# !bin/env python3
# Author(s): cryptopal85
#
# Version history: May 26 2022 - Initialising main structure
#                  Placeholder - placeholder
#
# Notes: 'simulator.py' mainly responsible for reading configured topics
# displays details on a terminal for smart devices or sensors communicate
# with the broker

import json
from topic import TopicAuto


class Simulator:
	def __init__(self, settings_file):
		self.broker_url = None
		self.broker_port = None
		self.topics = []
		self.load_settings(settings_file)
		
	def load_settings(self, settings_file):
		with open(settings_file) as json_file:
			config = json.load(json_file)
			self.broker_url = config['BROKER_URL']
			self.broker_port = config['BROKER_PORT']
			# fetch configured topics
			for topic in config['TOPICS']:
				topic_data = topic['DATA']
				topic_time_interval = topic['TIME_INTERVAL']
				topic_retain_probability = topic['RETAIN_PROBABILITY']
				if topic['TYPE'] == 'single':
					# populate single topic based on: /{PREFIX}
					topic_url = topic['PREFIX']
					self.topics.append(TopicAuto(self.broker_url, self.broker_port, topic_url, topic_data, topic_retain_probability, topic_time_interval))
				elif topic['TYPE'] == 'multiple':
					# populate multiple topics based on: /{PREFIX}/{id}
					for id in range(topic['RANGE_START'], topic['RANGE_END']+1):
						topic_url = topic['PREFIX'] + '/' + str(id)
						self.topics.append(TopicAuto(self.broker_url, self.broker_port, topic_url, topic_data, topic_retain_probability, topic_time_interval))
				elif topic['TYPE'] == 'list':
					# populate multiple topics based on /{PREFIX}/{item}
					for item in topic['LIST']:
						topic_url = topic['PREFIX'] + '/' + str(item)
						self.topics.append(TopicAuto(self.broker_url, self.broker_port, topic_url, topic_data, topic_retain_probability, topic_time_interval))
						
	def run(self):
		for topic in self.topics:
			print(f'Starting: {topic.topic_url} ...')
			topic.start()
			
	def stop(self):
		for topic in self.topics:
			print(f'Stopping: {topic.topic_url} ...')
			topic.stop()