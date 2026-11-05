from enum import Enum

class TargetType(Enum):
    FINISHPOS = 1               # Where they finished
    DOUBLEFINISHPOS = 2         # Where both cars finished
    NODNFS = 3                  # Both cars finished the race
    MINSTOPS = 4                # At least this many stops on both cars
    MAXSTOPS = 5                # At most this many stops on both cars

class RaceFinishStatus(Enum):
    FINISHED = 1
    DNFDAMAGE = 2
    DNFENGINE = 3
    DNFFUEL = 4

class keyVals(Enum):
    CURRENTSEASON = "CurrentSeason"
    CURRENTROUND = "CurrentRound"
    NEXTTEAMID = "NextTeamID"
    NEXTDRIVERID = "NextDriverID"
    NEXTPRIMARYSPONSORID = "NextPrimarySponsorID"
    NEXTSECONDARYSPONSORID = "NextSecondarySponsorID"
    MINDRIVERAGE = "MinDriverAge"
    MAXDRIVERAGE = "MaxDriverAge"

class PointsModel(Enum):
    F1TOP8 = 1
    F1TOP10 = 2
    MOTOGPTOP15 = 3
    MOTOGPTOP9S = 4
    WEC8HTOP10 = 5
    WEC24HTOP10 = 6
    F1TOP6 = 7
    F1TOP10S = 8