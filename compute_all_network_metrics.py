
import sys

# to create directories
from pathlib import Path

import os
from subprocess import call

# Available networks
files = os.listdir('input_data/networks/')
# Sorting files
files.sort()


# Go to the metrics directory
mydir = os.chdir('src/metrics/')
mydir = os.getcwd()

for file in files:
	print('Computing metrics: ', file)
	os.system('python net_metrics.py ' + file[:-8])