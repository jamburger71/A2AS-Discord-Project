from Classes.season import Season

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

    points = [
        [10, 8, 6, 5, 4, 3, 2, 1],
        [25, 18, 15, 12, 10, 8, 6, 4, 2, 1],
        [25, 20, 16, 13, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1],
        [12, 9, 7, 6, 5, 4, 3, 2, 1],
        [38, 27, 23, 18, 15, 12, 9, 6, 3, 2],
        [50, 36, 30, 24, 20, 16, 12, 8, 4, 2],
        [10, 6, 4, 3, 2, 1],
        [8, 7, 6, 5, 4, 3, 2, 1]
    ]
    
    def getPoints(self, season: Season) -> int:

        polePoint = 1 if season.pointForPole and self.qualiPosition == 1 else 0
        if self.racePosition > len(self.points[season.pointsModel.value-1]): return polePoint
        return self.points[season.pointsModel.value-1][self.racePosition-1] + polePoint