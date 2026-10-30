import json

class CarClass:

    def __init__(self, dboutput: tuple):

        self.id = dboutput[0]
        self.name = dboutput[1]
        self.description = dboutput[2]
    
    def toTuple(self):
        
        return (self.id, self.name, self.description)