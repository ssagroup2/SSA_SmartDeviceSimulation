# University of Essex - MSc CyberSecurity - Secure Software Architecture Module - May 2022

## Introduction ##

An application was developed in [Python](https://www.python.org/) to simulate interactions between smart devices, sensors and brokers using the MQTT protocol. MQTT is a well-known standard for IoT messaging (MQTT, 2022).

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
- Multiple topics based on variable ID or ITEMs
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

  | Key           | Type            | Description                                            | Required |
  | ------------- | --------------- | ------------------------------------------------------ | -------- |
  | `BROKER_URL`  | string          | The broker URL where the data will be published        | yes      |
  | `BROKER_PORT` | number          | The port used by the broker                            | yes      |
  | `TOPICS`      | array\<Objects> | Specification of topics and how they will be published | yes      |

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

  | Key                  | Type            | Description                                                                                                                     | Required                  |
  | -------------------- | --------------- | ------------------------------------------------------------------------------------------------------------------------------- | ------------------------- |
  | `TYPE`               | string          | It can be `"single"`, `"multiple"` or `"list"`                                                                                  | yes                       |
  | `PREFIX`             | string          | Prefix of the topic URL, depending on the `TYPE` it can be concatenated to `/<id>` or `/<item>`                                 | yes                       |
  | `LIST`               | array\<any>     | When the `TYPE` is `"list"` the topic prefix will be concatenated with `/<item>` for each item in the array                     | if `TYPE` is `"list"`     |
  | `RANGE_START`        | number          | When the `TYPE` is `"multiple"` the topic prefix will be concatenated with `/<id>` where `RANGE_START` will be the first number | if `TYPE` is `"multiple"` |
  | `RANGE_END`          | number          | When the `TYPE` is `"multiple"` the topic prefix will be concatenated with `/<id>` where `RANGE_END` will be the last number    | if `TYPE` is `"multiple"` |
  | `TIME_INTERVAL`      | number          | Time interval in seconds between submissions towards the topic                                                                  | yes                       |
  | `RETAIN_PROBABILITY` | number          | Number between 0 and 1 for the probability of the previous data being retained and sent again                                   | yes                       |
  | `DATA`               | array\<Objects> | Specification of the data that will form the JSON to be sent in the topic                                                       | yes                       |

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

  | Key         | Type   | Description                                                                          | Required                             |
  | ----------- | ------ | ------------------------------------------------------------------------------------ | ------------------------------------ |
  | `NAME`      | string | JSON property name to be sent                                                        | yes                                  |
  | `TYPE`      | string | It can be `"int"`, `"float"` or `"bool"`                                             | yes                                  |
  | `MIN_VALUE` | number | Minimum value that the property can assume                                           | If `TYPE` is different from `"bool"` |
  | `MAX_VALUE` | number | Maximum value that the property can assume                                           | If `TYPE` is different from `"bool"` |
  | `MAX_STEP`  | number | Maximum change that can be applied to the property from a published data to the next | If `TYPE` is different from `"bool"` |


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

05 - Secure protocols such as HTTPS are used to encrypt traffic in transit. 

08 - Only secure (verified by md5 checksums) libraries are used. Example below:

![This is an image](https://github.com/ssagroup2/SSA_SmartDeviceSimulation/blob/main/images/crypt.jpg)

Insecure Remote Access - The broker is configured to allow connection over SSL/TLS with a valid certificate and refuses connections from unauthorised devices/sensors. 

Furthermore the application addresses reliability by the use of the MQTT protocol. MQTT provides the following benefits (MQTT, 2022):

* Lightweight & Efficient - require minimal resources, reducing power consumption as well as optimizing network bandwidth by utilising relatively small header messages.

* Reliable Message Delivery - supports QoS (Quality of Service) and persistent sessions which addresses latency as well as lost messages. The implementation of QoS can be seen in the screenshot below. According to the experiment performed by Lee et al. (2021) message loss was reduced by 1.57 times when QoS 2 was used.

![This is an image](https://github.com/ssagroup2/SSA_SmartDeviceSimulation/blob/main/images/qos2.png)

* Security Enabled - allows the implementation of TLS as well as message encryption as seen in the application code.

## Functional Testing Images

(TBD)


## References 

MQTT (2022) MQTT: The Standard for IoT Messaging. Available from: https://mqtt.org [Accessed 26 May 2022].




(TBD)

