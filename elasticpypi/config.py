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

# load config
config = {k.lower(): v for k, v in os.environ.iteritems() if k in WATCHED}
