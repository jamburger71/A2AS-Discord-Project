import json

class CarClass:

    def __init__(self, classID):

        self.id = classID

        with open(f"{classID}.json") as classData:
            data = json.load(classData)
            self.name = data.name
            self.desc = data.desc
            self.cars = data.cars
            self.maxCars = data.maxCars
            self.minCarsPerTeam = data.minCarsPerTeam
            self.maxCarsPerTeam = data.maxCarsPerTeam
            