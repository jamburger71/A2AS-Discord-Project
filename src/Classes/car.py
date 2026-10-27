class Car:

    def __init__(self, dboutput: tuple | None):

        if dboutput is None: return
            
        self.id = dboutput[0]
        self.name = dboutput[1]
        self.description = dboutput[2]
        self.manufacturer = dboutput[3]
        self.year = dboutput[4]
        self.maxTeams = dboutput[5]
        self.carClass = dboutput[6]
        self.defaultWeight = dboutput[7]
        self.noUpgradesWeight = dboutput[8]
        self.weightUpgradeAmount = dboutput[9]
        self.noUpgradeDrag = dboutput[10]
        self.dragUpgradeAmount = dboutput[11]

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
            self.noUpgradesWeight,
            self.weightUpgradeAmount,
            self.noUpgradeDrag,
            self.dragUpgradeAmount
        )