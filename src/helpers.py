
from pathlib import Path
from itertools import zip_longest
import random

from Classes.car import Car
from Classes.result import Result
from Classes.season import Season
from enums import PointsModel

def ordinalConv(n):
    return str(n) + {1: 'st', 2: 'nd', 3: 'rd'}.get(4 if 10 <= n % 100 < 20 else n % 10, "th")

def groupReturnsByN(n, iteratedList, defaultFillVal=None):
    args = [iter(iteratedList)] * n
    return list(zip_longest(fillvalue=defaultFillVal, *args))

def convertToPounds(amount: int) -> str:
    return f"£{amount:,}"
