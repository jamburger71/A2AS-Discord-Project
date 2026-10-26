class Track:

    def __init__(self, dboutput: tuple):

        self.id = dboutput[0]
        self.name = dboutput[1]
        self.nickname = dboutput[2]
        self.country = dboutput[3]
        self.region = dboutput[4]
        self.city = dboutput[5]
        self.dateOpened = dboutput[6]
        
    def toTuple(self) -> tuple:
        
        return (
            self.id,
            self.name,
            self.nickname,
            self.country,
            self.region,
            self.city,
            self.dateOpened
        )