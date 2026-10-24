from yaml import load
try: from yaml import CLoader as Loader
except ImportError: from yaml import Loader
import json
from pathlib import Path
from itertools import zip_longest
import random

from Classes.car import Car
from enums import Gender

def ordinalConv(n):
    return str(n) + {1: 'st', 2: 'nd', 3: 'rd'}.get(4 if 10 <= n % 100 < 20 else n % 10, "th")

def groupReturnsByN(n, iteratedList, defaultFillVal=None):
    args = [iter(iteratedList)] * n
    return list(zip_longest(fillvalue=defaultFillVal, *args))

def getTrackData(trackName: str) -> dict:

    filePath = Path(__file__).resolve().parent / "Resources" / "Tracks" / f"{trackName}.json"
    with open(filePath, "r") as file:
        return json.loads(file.read())

def convertToPounds(amount: int) -> str:
    return f"£{amount:,}"

def getBestLetterCode(firstName: str, lastName: str, allThreeCodes: list) -> str | None:
    
    noNameAvailable = False
    currentLastChar: int = 2
    currentMiddleChar: int = 1
    currentFirstChar: int = 0
    threecode = lastName[:3].upper()
    if threecode not in allThreeCodes and len(lastName) <= 3:
        noNameAvailable = True
    while threecode not in allThreeCodes and not noNameAvailable:
        threecode = f"{lastName[currentFirstChar]}{lastName[currentMiddleChar]}{lastName[currentLastChar]}".upper()
        if currentMiddleChar < currentLastChar - 1:
            currentMiddleChar += 1
        elif currentLastChar < len(lastName) - 1:
            currentLastChar += 1
            currentMiddleChar = currentFirstChar + 1
        elif currentFirstChar < len(lastName) - 3:
            currentFirstChar += 1
            currentMiddleChar = currentFirstChar + 1
            currentLastChar = currentMiddleChar + 1
        else:
            threecode = f"{firstName[0]}{lastName[0]}{lastName[1]}".upper()
            if threecode not in allThreeCodes:
                return None
    return threecode
            

def getGenderWithWeight() -> Gender:
    
    Genders = [Gender.MALE, Gender.FEMALE, Gender.NONBINARY, Gender.OTHER]
    GenderWeights = [80, 15, 3, 2] # to 100
    
    return random.choices(Genders, weights=GenderWeights, k=1)[0]