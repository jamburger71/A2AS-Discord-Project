from sponsor import Sponsor
from enums import TargetType

class PrimarySponsor(Sponsor):

    def __init__(self, dboutput):

        super().__init__(dboutput)
        self.target = dboutput[6]
        self.targetType: TargetType = dboutput[7]
        self.targetReward = dboutput[8]

    def toTuple(self) -> tuple:

        return super().toTuple() + (self.target, self.targetType, self.targetReward)