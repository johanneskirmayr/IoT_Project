# DataBank class to store and retrieve UUIDs and their locations

class DataBank:
    def __init__(self):
        # hardcoded databank of UUIDs and their locations
        self.databank = {
            "11111111-1111-1111-1111-111111111111": {"floor": 1, "room": "A", "voice_message": "You are at the start"},
            "22222222-2222-2222-2222-222222222222": {"floor": 2, "room": "B", "voice_message": "TODO"},
            "33333333-3333-3333-3333-333333333333": {"floor": 3, "room": "C", "voice_message": "TODO"},
        }

    def get_location(self, uuid):
        # check if the UUID is in the databank
        if uuid in self.databank:
            # return the location if found
            return self.databank[uuid]
        else:
            # return None if not found
            return None
