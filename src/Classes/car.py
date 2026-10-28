class Car:

    def __init__(self, dboutput: tuple | None):

        if dboutput is None: return
            
        self.id = dboutput[0]
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

    def toTuple(self) -> tuple:

        return (
            self.id, 
            self.name, 
            self.description, 
            self.manufacturer, 
            self.year, 
            self.maxTeams, 
            self.carClass,
            self.defaultWeight,
            self.baseWeight,
            self.weightUpgradeSize,
            self.maxWeightUpgrades,
            self.baseDrag,
            self.dragUpgradeSize
        )