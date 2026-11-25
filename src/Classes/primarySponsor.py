from Classes.result import Result
import helpers
from Classes.sponsor import Sponsor
from enums import TargetType, RaceFinishStatus


class PrimarySponsor(Sponsor):

    def __init__(self, dboutput):

        super().__init__(dboutput)
        self.target: int = dboutput[5]
        self.targetType = dboutput[6]
        self.targetReward: int = dboutput[7]

    def toTuple(self) -> tuple:

        return super().toTuple() + (
            self.target,
            self.targetType,
            self.targetReward)

    def getRewardText(self) -> str:

        match self.targetType:
            case TargetType.FINISHPOS:
                return f"Achieve {helpers.ordinalConv(self.target)} or above in the race."
            case TargetType.NODNFS:
                return "Have both cars finish the race."
            case TargetType.DOUBLEFINISHPOS:
                return f"Have both cars achieve {helpers.ordinalConv(self.target)} or above in the race."
            case TargetType.MAXSTOPS:
                return f"Have both cars pit a total of {self.target} times or less."
            case TargetType.MINSTOPS:
                return f"Have both cars pit a total of {self.target} times or more."
            case TargetType.QUALIPOS:
                return f"Achieve {helpers.ordinalConv(self.target)} or above in qualifying."
            case TargetType.DOUBLEQUALIPOS:
                return f"Have both cars achieve {helpers.ordinalConv(self.target)} or above in qualifying."

    def isTargetMet(self, result1: Result, result2: Result) -> bool:

        match self.targetType:
            case TargetType.FINISHPOS:
                return result1.racePosition <= self.target or result2.racePosition <= self.target
            case TargetType.DOUBLEFINISHPOS:
                return result1.racePosition <= self.target and result2.racePosition <= self.target
            case TargetType.NODNFS:
                return result1.raceFinishStatus == RaceFinishStatus.FINISHED and result2.raceFinishStatus == RaceFinishStatus.FINISHED
            case TargetType.MAXSTOPS:
                return result1.raceStops + result2.raceStops <= self.target
            case TargetType.MINSTOPS:
                return result1.raceStops + result2.raceStops >= self.target
            case TargetType.QUALIPOS:
                return result1.qualiPosition <= self.target or result2.qualiPosition <= self.target
            case TargetType.DOUBLEQUALIPOS:
                return result1.qualiPosition <= self.target and result2.qualiPosition <= self.target

        return True
