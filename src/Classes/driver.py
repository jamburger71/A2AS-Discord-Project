

class Driver:

    def __init__(self, databaseData: tuple, unsaved: bool = False):
        
        self.id = databaseData[0]
        self.firstName = databaseData[1]
        self.lastName = databaseData[2]
        self.threecode = databaseData[3]
        self.nationality = databaseData[4]
        self.age = databaseData[5]
        self.qualiPace = databaseData[6]
        self.racePace = databaseData[7]
        self.wetPace = databaseData[8]
        self.tyreManagement = databaseData[9]
        self.aggressiveness = databaseData[10]
        self.defending = databaseData[11]
        self.contractCost = databaseData[12]
        if unsaved:
            self.races = 0
            self.wins = 0
            self.podiums = 0
            self.isAvailable = True
        else:
            self.races = databaseData[13] or 0
            self.wins = databaseData[14] or 0
            self.podiums = databaseData[15] or 0
            self.isAvailable = databaseData[16] or True