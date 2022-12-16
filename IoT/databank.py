# DataBank class to store and retrieve UUIDs and their locations

class DataBank:
    def __init__(self):
        # hardcoded databank of UUIDs and their locations
        self.databank = {
            "8882358095064d379d5b437e33a09e8c": {"floor": 1, "room": "A", "voice_message": "You are at the start"},
            "2a7f6ba12ff44a6aa74df05abc062b0a": {"floor": 2, "room": "B", "voice_message": "TODO"},
            "9912e0beec0b4fd3854eb6fca1501669": {"floor": 3, "room": "C", "voice_message": "TODO"},
        }

    def get_location(self, uuid):
        # check if the UUID is in the databank
        if uuid in self.databank:
            # return the location if found
            return self.databank[uuid]
        else:
            # return None if not found
            return None
