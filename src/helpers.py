
from pathlib import Path
from itertools import zip_longest
import random

from Classes.car import Car
from Classes.result import Result
from enums import PointsModel

def ordinalConv(n):
    return str(n) + {1: 'st', 2: 'nd', 3: 'rd'}.get(4 if 10 <= n % 100 < 20 else n % 10, "th")

def groupReturnsByN(n, iteratedList, defaultFillVal=None):
    args = [iter(iteratedList)] * n
    return list(zip_longest(fillvalue=defaultFillVal, *args))

def convertToPounds(amount: int) -> str:
    return f"£{amount:,}"

points = [
    [10, 8, 6, 5, 4, 3, 2, 1],
    [25, 18, 15, 12, 10, 8, 6, 4, 2, 1],
    [25, 20, 16, 13, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1],
    [12, 9, 7, 6, 5, 4, 3, 2, 1],
    [38, 27, 23, 18, 15, 12, 9, 6, 3, 2],
    [50, 36, 30, 24, 20, 16, 12, 8, 4, 2],
    [10, 6, 4, 3, 2, 1],
    [8, 7, 6, 5, 4, 3, 2, 1]
    
]

def getPoints(pointsModel: PointsModel, position: int, pointForPole: bool) -> int:

    polePoint = 1 if pointForPole and position == 1 else 0
    if position > len(points[pointsModel.value-1]): return 0
    return points[pointsModel.value-1][position-1] + polePoint

def getCurrentStandings(results: list[Result], pointsModel: PointsModel, pointForPole: bool) -> list[tuple]:
    
    standingsTable = {}
    for result in results:
        standingsTable[result.driver] = standingsTable.get(result.driver, 0) + getPoints(pointsModel, result.racePosition, pointForPole)
    return list(standingsTable.items())