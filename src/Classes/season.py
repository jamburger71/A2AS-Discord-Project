from enums import PointsModel

class Season:

    def __init__(self, dboutput):
        self.seasonNo = dboutput[0]
        self.name = dboutput[1]
        self.carClass = dboutput[2]
        self.year = dboutput[3]
        self.pointsModel = dboutput[4]
        self.pointForPole = bool(dboutput[5])

    def toTuple(self):

        return (self.seasonNo, self.name, self.carClass, self.year, self.pointsModel, self.pointForPole)