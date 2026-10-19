

class Team:

    def __init__(self, databaseData: tuple):

        self.id = databaseData[0]
        self.name = databaseData[1]
        self.desc = databaseData[2]
        self.nationality = databaseData[3]
        self.ownerID = databaseData[4]
        self.isActive = databaseData[5] or False
        self.engineSupplier = databaseData[6] or None
        self.car = databaseData[7] or None
        self.driverOne = databaseData[8] or None
        self.driverTwo = databaseData[9] or None
        self.currentFunds = databaseData[10]
        self.dragUpgrades = databaseData[11]
        self.weightUpgrades = databaseData[12]
        self.primarySponsor = databaseData[13] or None
        self.secondarySponsor1 = databaseData[14] or None
        self.secondarySponsor2 = databaseData[15] or None
        self.secondarySponsor3 = databaseData[16] or None