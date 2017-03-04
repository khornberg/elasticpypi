import os

WATCHED=[
    'SERVICE',
    'STAGE',
    'BUCKET',
    'TABLE',
    'USERNAME',
    'PASSWORD',
    'OVERWRITE'
]

TRUTHY = ['TRUE', 'true', 1]
FALSEY = ['FALSE', 'false', 0]

# load config
config = {k.lower(): v for k, v in os.environ.iteritems() if k in WATCHED}

# check config
for k, v in config.iteritems():
    # assume env vars are always stringy
    if v in TRUTHY:
        config[k] = True
    if v in FALSEY:
        config[k] = False

