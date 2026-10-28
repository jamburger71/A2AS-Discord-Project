

class Driver:

    def __init__(self, databaseData: tuple):
        
        self.threecode = databaseData[0]
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
        if len(databaseData) > 12:
            self.races = databaseData[12]
            self.wins = databaseData[13]
            self.podiums = databaseData[14]
        else:
            self.races = 0
            self.wins = 0
            self.podiums = 0
        
    def toTuple(self) -> tuple:
        
        return (
            self.threecode,
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
            self.races,
            self.wins,
            self.podiums
        )
    
def byVariable(threecode, firstname, lastname, nationality, age, qualipace, racepace, wetpace, tyremanagement, aggressiveness, defending, contractcost, races, wins, podiums):
    
    return Driver((threecode, firstname, lastname, nationality, age, qualipace, racepace, wetpace, tyremanagement, aggressiveness, defending, contractcost, races, wins, podiums))