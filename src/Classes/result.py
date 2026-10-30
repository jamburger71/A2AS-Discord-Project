

class Result:

    def __init__(self, dboutput: tuple):

        self.seasonNo = dboutput[0]
        self.roundNo = dboutput[1]
        self.driver = dboutput[2]
        self.team = dboutput[3]
        self.qualiPosition = dboutput[4]
        self.qualiTime = dboutput[5]
        self.racePosition = dboutput[6]
        self.raceGap = dboutput[7]
        self.raceStops = dboutput[8]
        self.raceFinishStatus = dboutput[9]

    def toTuple(self):

        return (
            self.seasonNo, 
            self.roundNo, 
            self.driver, 
            self.team, 
            self.qualiPosition, 
            self.qualiTime, 
            self.racePosition, 
            self.raceGap, 
            self.raceStops,
            self.raceFinishStatus
        )