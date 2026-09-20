from yaml import load
try: from yaml import CLoader as Loader
except ImportError: from yaml import Loader
import json

from itertools import zip_longest

def getMetadata():
    return load(open("appMetadata.yaml").read(), Loader=Loader)

def ordinalConv(n):
    return str(n) + {1: 'st', 2: 'nd', 3: 'rd'}.get(4 if 10 <= n % 100 < 20 else n % 10, "th")

def groupReturnsByN(n, iteratedList, defaultFillVal=None):
    args = [iter(iteratedList)] * n
    return zip_longest(fillvalue=defaultFillVal, *args)

def getTrackData(trackName):
    return json.loads(open(f"FixedData\TrackData\{trackName}"))