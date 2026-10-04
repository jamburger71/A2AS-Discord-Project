from yaml import load
try: from yaml import CLoader as Loader
except ImportError: from yaml import Loader
import json

from itertools import zip_longest

def ordinalConv(n):
    return str(n) + {1: 'st', 2: 'nd', 3: 'rd'}.get(4 if 10 <= n % 100 < 20 else n % 10, "th")

def groupReturnsByN(n, iteratedList, defaultFillVal=None):
    args = [iter(iteratedList)] * n
    return list(zip_longest(fillvalue=defaultFillVal, *args))

def getTrackData(trackName: str) -> dict:
    with open(f"..\\FixedData\\TrackData\\{trackName}", "r", encoding="utf-8") as file:
        return json.loads(file.read())

def convertToPounds(amount: int) -> str:
    return f"£{amount:,}"