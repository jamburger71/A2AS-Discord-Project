import json

class Track:

    def __init__(self, trackID):

        self.id = trackID

        with open(f"{trackID}.json") as trackData:

            data = json.load(trackData)
            self.fullName = data.fullName
            self.shortName = data.ShortName
            self.country = data.Country
            self.state = data.State
            self.city = data.City
            self.layouts = data.Layouts