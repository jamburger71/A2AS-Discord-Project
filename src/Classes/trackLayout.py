class TrackLayout:
    
    def __init__(self, dboutput: tuple):
            
        self.id = dboutput[0]
        self.track = dboutput[1]
        self.name = dboutput[2]
        self.description = dboutput[3]
        self.year = dboutput[4]
        self.length = dboutput[5]
        self.corners = dboutput[6]
    
    def toTuple(self) -> tuple:
        
        return (
            self.id,
            self.track,
            self.name,
            self.description,
            self.year,
            self.length,
            self.corners
        )

    @classmethod
    def new(cls, id, track, name, description, year, length, corners):
        return cls((id, track, name, description, year, length, corners))