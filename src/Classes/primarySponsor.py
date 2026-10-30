import helpers
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

    def getRewardText(self) -> str:

        match self.targetType:
            case TargetType.FINISHPOS:
                return f"Achieve {helpers.ordinalConv(self.target)} or above."
            case TargetType.NODNFS:
                return "Have both cars finish the race."
            case TargetType.DOUBLEFINISHPOS:
                return f"Have both cars achieve {helpers.ordinalConv(self.target)} or above."
            case TargetType.MAXSTOPS:
                return f"Have both cars pit {self.target} times or less."
            case TargetType.MINSTOPS:
                return f"Have both cars pit {self.target} times or more."
                