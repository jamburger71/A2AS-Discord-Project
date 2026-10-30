

class Event:

    def __init__(self, databaseData: tuple):

        self.seasonNo = databaseData[0]
        self.roundNo = databaseData[1]
        self.title = databaseData[2]
        self.date = databaseData[3]
        self.track = databaseData[4]
        self.weather = databaseData[5]
        self.qualiDuration = databaseData[6]
        self.raceLength = databaseData[7]

    def toTuple(self) -> tuple:

        return (
            self.seasonNo,
            self.roundNo,
            self.title,
            self.date,
            self.weather,
            self.qualiDuration,
            self.raceLength,
        )

    @classmethod
    def new(cls, seasonNo, roundNo, title, date, track, qualiDuration, raceLength):
        return cls((seasonNo, roundNo, title, date, track, "Unset", qualiDuration, raceLength))