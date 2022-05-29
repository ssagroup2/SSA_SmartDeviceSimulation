# smartdevices

MSc Cybersecurity - Secure Software Architecture May 2022

MQTT simulator coded in [Python](https://www.python.org/) to simulate interactions between smart devices, sensors and brokers.

[Features](#features) •
[Getting Started](#getting-started) •
[Configuration](#configuration) •

![Simulator Running - Demo](tbd)

## Features

- Client-based authentication
- SSL/TLS encryption on network level - protecting authentication data
- Payload encryption on application level - e2e of payload data (work-in-progress)
- Efficient, modular and easy-to-use
- JSON-based single configuration file
- Pre-defined fixed topics
- Multiple topics based on variable ID or ITEMs
- Random data generation based on JSON parameters for simulating

# Getting Started

#### Prerequisites

#### Installing Dependencies

#### Running

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

- The key **DATA** inside TOPICS has a array of objects where each one has the format:

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
