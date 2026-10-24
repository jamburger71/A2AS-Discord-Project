from enum import Enum

class Gender(Enum):
    MALE = 1,
    FEMALE = 2,
    NONBINARY = 3,
    OTHER = 4

class TargetType(Enum):
    FINISHPOS = 1,
    DOUBLEFINISHPOS = 2,
    DIDNTFINISHBELOW = 3,
    DOUBLEDIDNTFINISHBELOW = 4,
    NODNFS = 5