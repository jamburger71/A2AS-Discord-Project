from faker import Faker
from faker.config import AVAILABLE_LOCALES
import random

class Driver:

    def __init__(self, databaseData: tuple):
        
        self.ID = databaseData[0]
        self.firstName = databaseData[1]
        self.lastName = databaseData[2]
        self.nationality = databaseData[3]
        self.age = databaseData[4]
        self.qualiPace = databaseData[5]
        self.racePace = databaseData[6]
        self.wetPace = databaseData[7]
        self.tyreManagement = databaseData[8]
        self.aggressiveness = databaseData[9]
        self.defending = databaseData[10]
        self.contractCost = databaseData[11]

    @classmethod
    def new(cls, ID, firstname, lastname, nationality, age, qualipace, racepace, wetpace, tyremanagement, aggressiveness, defending, contractcost):
        return Driver((ID, firstname, lastname, nationality, age, qualipace, racepace, wetpace, tyremanagement, aggressiveness, defending, contractcost))
        
    def toTuple(self) -> tuple:
        
        return (
            self.ID,
            self.firstName,
            self.lastName,
            self.nationality,
            self.age,
            self.qualiPace,
            self.racePace,
            self.wetPace,
            self.tyreManagement,
            self.aggressiveness,
            self.defending,
            self.contractCost,
        )

    @classmethod
    def randomDriver(cls, driverID):

        isMale = random.randint(0, 100) > 5
        faker = Faker(random.choice(AVAILABLE_LOCALES))
        firstname = faker.first_name_male() if isMale else faker.first_name_female()
        lastname = faker.last_name()
        age = random.randint(18, 45)
        nationality = faker.country()
        baseVal = random.randint(0, 100)
        deviation = random.randint(0, 25)
        qualiPace = max(min(random.randint(baseVal-deviation, baseVal+deviation), 100), 0)
        racePace = max(min(random.randint(baseVal-deviation, baseVal+deviation), 100), 0)
        wetPace = max(min(random.randint(baseVal-deviation, baseVal+deviation), 100), 0)
        tyreManagement = max(min(random.randint(baseVal-deviation, baseVal+deviation), 100), 0)
        aggressiveness = max(min(random.randint(baseVal-deviation, baseVal+deviation), 100), 0)
        defending = max(min(random.randint(baseVal-deviation, baseVal+deviation), 100), 0)
        cost = random.randint(-10, 100)*1000

        return Driver((driverID, firstname, lastname, nationality, age, qualiPace, racePace, wetPace, tyreManagement, aggressiveness, defending, cost))