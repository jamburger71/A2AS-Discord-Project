class Car:

    def __init__(self, dboutput: tuple):
            
        self.ID = dboutput[0]
        self.name = dboutput[1]
        self.description = dboutput[2]
        self.manufacturer = dboutput[3]
        self.year = dboutput[4]
        self.carClass = dboutput[5]
        self.maxTeams = dboutput[6]
        self.defaultWeight = dboutput[7]
        self.baseWeight = dboutput[8]
        self.weightUpgradeSize = dboutput[9]
        self.maxWeightUpgrades = dboutput[10]
        self.baseDrag = dboutput[11]
        self.dragUpgradeSize = dboutput[12]
        self.maxDragUpgrades = dboutput[13]

    @classmethod
    def new(cls, dbinput: tuple | None):

        if dbinput is None: return None
        return cls(dboutput=dbinput)
        
    def toTuple(self) -> tuple:

        return (
            self.ID, 
            self.name, 
            self.description, 
            self.manufacturer, 
            self.year, 
            self.carClass,
            self.maxTeams, 
            self.defaultWeight,
            self.baseWeight,
            self.weightUpgradeSize,
            self.maxWeightUpgrades,
            self.baseDrag,
            self.dragUpgradeSize,
            self.maxDragUpgrades
        )