

class Sponsor:

    def __init__(self, dboutput):

        self.id = dboutput[0]
        self.name = dboutput[1]
        self.contractLength = dboutput[2]
        self.isAvailable = dboutput[3]
        self.signingPay = dboutput[4]
        self.racePay = dboutput[5]

    def toTuple(self) -> tuple:

        return (
            self.id,
            self.name,
            self.contractLength,
            self.isAvailable,
            self.signingPay,
            self.racePay
        )