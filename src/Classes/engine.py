class Engine:

    def __init__(self, dboutput: tuple | None):

        if dboutput is None: return
            
        self.model = dboutput[0]
        self.manufacturer = dboutput[1]
        self.year = dboutput[2]
        self.power = dboutput[3]
        self.reliability = dboutput[4]
        self.price = dboutput[5]

    def toTuple(self):

        return (
            self.model,
            self.manufacturer,
            self.year,
            self.power,
            self.reliability,
            self.price
        )