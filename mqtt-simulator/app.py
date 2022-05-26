# !bin/env python3
# Author(s): cryptopal85
#
# Version history: May 26 2022 - Initialising main structure
#                                - placeholder
#                  Placeholder - placeholder
#
# Notes: app.py is a init placeholder where will be used to run the main app 'simulator.py'

import argparse
from pathlib import Path
from simulator import Simulator


# fetch default settings for each of the defined smart devices and sensors
def default_settings():
	base_folder = Path(__file__).resolve().parent.parent
	settings_file = base_folder / 'config/settings.json'
	return settings_file
	

# sanity check on the config file
def is_valid_file(parser, arg):
	settings_file = Path(arg)
	if not settings_file.is_file():
		return parser.error(f"argument -f/--file: cannot open '{arg}'")
	return settings_file
	

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file', dest='settings_file', type=lambda x: is_valid_file(parser, x), help='settings_file', default=default_settings())
args = parser.parse_args()

# run the Simulator for interacting with a Broker
simulator = Simulator(args.settings_file)
simulator.run()