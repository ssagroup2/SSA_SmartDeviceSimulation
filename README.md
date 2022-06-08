# University of Essex - MSc CyberSecurity - Secure Software Architecture Module - May 2022

## Introduction ##

An application was developed in [Python](https://www.python.org/) to simulate interactions between smart devices, sensors and brokers using the MQTT protocol. MQTT is a well-known standard for IoT messaging (MQTT, 2022). The code simulates lamps (on, off), heating sensors (temperature values) as well as oximeters (heartbeats, body temperature).

[Features](#features) •
[Getting Started](#getting-started) •
[Code Structure](#code-structure) •
[Configuration](#configuration) •
[Running the Code](#running-the-code) •
[Discussion](#discussion) •
[Functional Testing Images](#functional-testing-images) •
[References](#references) •

## Features

- Client-based authentication
- SSL/TLS encryption on a network level - protecting authentication data
- Payload encryption on an application level - e2e encryption of payload data
- Efficient, modular and easy-to-use
- JSON-based single configuration file
- Pre-defined fixed topics
- Multiple topics based on variable ID
- Random data generation based on JSON parameters used for simulation purposes

## Getting Started

### Prerequisites

The following pre-requisites are required to successfully run the code:

* Python 3.10.3
* Mosquitto Broker installed and running on port 8884

### Installing Dependencies

The following python libraries are required:

* time
* json
* random
* threading
* ssl
* paho.mqtt.client
* cryptography.fernet
* base64
* hashlib
* logging
* string
* struct
* sys
* uuid

## Code Structure

The code structure is as follows:

![This is an image](https://github.com/ssagroup2/SSA_SmartDeviceSimulation/blob/main/images/structure.jpg)

`app.py` - Application placeholder file to run `simulator.py`

`simulator.py` - Responsible for reading topics and displaying data to the terminal. This data is communication between sensors and the broker.

`topic.py` - Used to establish a connection between sensors and the broker. The broker uses the topic of a message to decide which client receives which message. TLS client certificates and key paths are configured in this file.

`sample-mosquitto.conf` - Configuration file for Mosquitto broker. TLS broker certificates and key paths are configured in this file.

## Configuration

- The `config/settings.json` file has three main configuration parameters:

  ```json
  {
  	"BROKER_URL": "mqtt.eclipse.org",
  	"BROKER_PORT": 1883,
  	"TOPICS": [
  		...
  	]
  }
  ```
   ![This is an image](https://github.com/ssagroup2/SSA_SmartDeviceSimulation/blob/main/images/broker1.png)

- The key **TOPICS** has a array of objects where each one has the format:

  ```json
  {
  	"TYPE": "multiple",
  	"PREFIX": "temperature",
  	"RANGE_START": 1,
  	"RANGE_END": 2,
  	"TIME_INTERVAL": 25,
  	"RETAIN_PROBABILITY": 0.5,
  	"DATA": [
  		...
  	]
  }
  ```
   ![This is an image](https://github.com/ssagroup2/SSA_SmartDeviceSimulation/blob/main/images/topics1.png)

- The key **DATA** inside TOPICS has an array of objects where each one has the format:

  ```json
  {
    "NAME": "temperature",
    "TYPE": "float",
    "MIN_VALUE": 30,
    "MAX_VALUE": 40,
    "MAX_STEP": 0.2
  }
  ```
   ![This is an image](https://github.com/ssagroup2/SSA_SmartDeviceSimulation/blob/main/images/topics2.png)
  
## Running the Code

1. Run the Mosquitto Broker which produces the following output:

![This is an image](https://github.com/ssagroup2/SSA_SmartDeviceSimulation/blob/main/images/mos1.png)

2. Run `app.py` which produces the following output:

![This is an image](https://github.com/ssagroup2/SSA_SmartDeviceSimulation/blob/main/images/sensors1.png)

## Discussion

The figure below represents a summary of the vulnerabilities identified in the initial design document:

![This is an image](https://github.com/ssagroup2/SSA_SmartDeviceSimulation/blob/main/images/vul.png)

5 vulnerabilities were selected to be mitigated, these were as follows:

01 - No Default, Weak or hardcoded passwords were used. Communication between sensor devices were performed via TLS certificate based authentication.

03 - All communication was performed via port 8884 which supports TLS with Encryption. No insecure ports are used.

05 - Secure protocols such as MQTTS (Message Queuing Telemetry Transport Secured) are used to encrypt traffic in transit.

08 - Only secure (verified by md5 checksums) libraries are used. Example below:

![This is an image](https://github.com/ssagroup2/SSA_SmartDeviceSimulation/blob/main/images/crypt.jpg)

Insecure Remote Access - The broker is configured to allow connection over SSL/TLS with a valid certificate and refuses connections from unauthorised devices/sensors. 

Furthermore the application addresses reliability by the use of the MQTT protocol. MQTT provides the following benefits (MQTT, 2022):

* Lightweight & Efficient - require minimal resources, reducing power consumption as well as optimizing network bandwidth by utilising relatively small header messages.

* Reliable Message Delivery - supports QoS (Quality of Service) and persistent sessions which addresses latency as well as lost messages. The implementation of QoS can be seen in the screenshot below. According to the experiment performed by Lee et al. (2013) message loss was reduced by 1.57 times when QoS 2 was used.

![This is an image](https://github.com/ssagroup2/SSA_SmartDeviceSimulation/blob/main/images/qos2.png)

* Security Enabled - allows the implementation of TLS as well as message encryption as seen in the application code.

## Functional Testing Images

(TBD)


## References 

MQTT (2022) MQTT: The Standard for IoT Messaging. Available from: https://mqtt.org [Accessed 26 May 2022].

Lee, S., Kim, H., Hong, D & Ju, H. (2013) 'Correlation analysis of MQTT loss and delay according to QoS level', <i> The International Conference on Information Networking 2013 (ICOIN)</i>. Bangkok, 28-30 January 2013. USA: IEEE. Available from: https://ieeexplore.ieee.org/document/6496715 [Accessed 02 June 2022].

