from datetime import datetime


class Event:

    def __init__(self, databaseData: tuple):

        self.seasonNo: int = databaseData[0]
        self.roundNo: int = databaseData[1]
        self.title: str = databaseData[2]
        print(type(databaseData[3]))
        self.date: datetime = datetime.fromisoformat(databaseData[3])
        self.trackLayout: str = databaseData[4]
        self.weather: str | None = databaseData[5]
        self.qualiDuration: int = databaseData[6]
        self.raceLength: int = databaseData[7]

    def toTuple(self) -> tuple:

        return (
            self.seasonNo,
            self.roundNo,
            self.title,
            self.date.isoformat(),
            self.trackLayout,
            self.weather,
            self.qualiDuration,
            self.raceLength
        )

    @classmethod
    def create(cls, seasonNo, roundNo, title, date, trackLayout, weather, qualiDuration, raceLength):

        return cls((seasonNo, roundNo, title, date.isoformat(), trackLayout, weather, qualiDuration, raceLength))

    @classmethod
    def new(cls, dbinput):
        if dbinput is None:
            return None
        return cls(dbinput)
