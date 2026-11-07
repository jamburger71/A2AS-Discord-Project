

class Team:

    def __init__(self, databaseData: tuple):

        self.ID: int = databaseData[0]
        self.name: str = databaseData[1]
        self.desc: str = databaseData[2]
        self.nationality: str = databaseData[3]
        self.ownerID: str = databaseData[4]
        self.engine: str = databaseData[5]
        self.car: str = databaseData[6]
        self.driverOne: int | None = databaseData[7]
        self.driverTwo: int | None = databaseData[8]
        self.currentFunds: int = databaseData[9]
        self.dragUpgrades: int = databaseData[10]
        self.weightUpgrades: int = databaseData[11]
        self.primarySponsor = databaseData[12]
        self.secondarySponsor1 = databaseData[13]
        self.secondarySponsor2 = databaseData[14]
        self.secondarySponsor3 = databaseData[15]

    @classmethod
    def new(cls, dbinput):
        if dbinput is None: return None
        return cls(dbinput)
    
    @classmethod
    def register(cls, ID: int, name: str, desc: str, nationality: str, ownerID: int, defaultCash: int):
        return cls((ID, name, desc, nationality, ownerID, None, None, None, None, defaultCash, 0, 0, None, None, None, None))
    
    def toTuple(self) -> tuple:
        
        return (
            self.ID,
            self.name,
            self.desc,
            self.nationality,
            self.ownerID,
            self.engine,
            self.car,
            self.driverOne,
            self.driverTwo,
            self.currentFunds,
            self.dragUpgrades,
            self.weightUpgrades,
            self.primarySponsor,
            self.secondarySponsor1,
            self.secondarySponsor2,
            self.secondarySponsor3
        )