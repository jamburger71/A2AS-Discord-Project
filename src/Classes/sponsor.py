

class Sponsor:

    def __init__(self, dboutput):

        self.id = dboutput[0]
        self.name = dboutput[1]
        self.contractLength = dboutput[2]
        self.signingPay = dboutput[3]
        self.racePay = dboutput[4]

    def toTuple(self) -> tuple:

        return (
            self.id,
            self.name,
            self.contractLength,
            self.signingPay,
            self.racePay
        )

    @classmethod
    def new(cls, dbinput: tuple | None):

        if dbinput is None: return None
        return cls(dboutput=dbinput)