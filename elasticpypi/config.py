import json
import os


dir_path = os.path.dirname(os.path.realpath(__file__))
with open('{}/config.json'.format(dir_path), 'r') as f:
    config = json.load(f)
