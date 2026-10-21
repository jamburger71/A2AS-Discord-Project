import json

 Car:

    def __init__(self, ams2id: str):

        self.id = ams2id

        with open(f"{ams2id}.json") as carData:
            data = json.load(carData)
            self.name = data.name
            self.desc = data.desc
            self.year = data.year
            self.maxCars = data.maxCars