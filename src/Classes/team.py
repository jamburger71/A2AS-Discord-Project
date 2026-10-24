

class Team:

    def __init__(self, databaseData: tuple):

        self.id: int = databaseData[0]
        self.name: str = databaseData[1]
        self.desc: str = databaseData[2]
        self.nationality: str = databaseData[3]
        self.ownerID: str = databaseData[4]
        self.isActive: bool = databaseData[5] or False
        self.engine: str = databaseData[6] or ""
        self.car: str = databaseData[7] or ""
        self.driverOne: int = databaseData[8] or -1
        self.driverTwo: int = databaseData[9] or -1
        self.currentFunds: int = databaseData[10]
        self.dragUpgrades: int = databaseData[11]
        self.weightUpgrades: int = databaseData[12]
        self.primarySponsor = databaseData[13] or None
        self.secondarySponsor1 = databaseData[14] or None
        self.secondarySponsor2 = databaseData[15] or None
        self.secondarySponsor3 = databaseData[16] or None