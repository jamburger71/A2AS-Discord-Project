

class Event:

    def __init__(self, databaseData: tuple):

        self.seasonNo = databaseData[0]
        self.roundNo = databaseData[1]
        self.title = databaseData[2]
        self.date = databaseData[3]
        self.weather = databaseData[4]
        self.qualiDuration = databaseData[5]
        self.qualiResults = databaseData[6]
        self.raceLength = databaseData[7]
        self.raceResults = databaseData[8]

    def toTuple(self) -> tuple:

        return (
            self.seasonNo,
            self.roundNo,
            self.title,
            self.date,
            self.weather,
            self.qualiDuration,
            self.qualiResults,
            self.raceLength,
            self.raceResults
        )