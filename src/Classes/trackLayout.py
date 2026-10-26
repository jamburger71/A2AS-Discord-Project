class TrackLayout:
    
    def __init__(self, dboutput: tuple):
            
            self.id = dboutput[0]
            self.name = dboutput[1]
            self.description = dboutput[2]
            self.year = dboutput[3]
            self.length = dboutput[4]
            self.corners = dboutput[5]
    
    def toTuple(self) -> tuple:
        
        return (
            self.id,
            self.name,
            self.description,
            self.year,
            self.length,
            self.corners
        )