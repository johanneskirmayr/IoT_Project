# DataBank class to store and retrieve UUIDs and their locations

class DataBank:
    def __init__(self):
        # hardcoded databank of UUIDs and their locations
        self.databank = {
            "8882358095064d379d5b437e33a09e8c": {"floor": 1, "room": "A", "voice_message": "Welcome to Stockholm University, I am happy to navigate you to your destination. I will also give you some insights of important spots on our way!"},
            "2a7f6ba12ff44a6aa74df05abc062b0a": {"floor": 2, "room": "B", "voice_message": "Great, we made it to our first waypoint. On the right you can see the university's cafeteria, today's special dish is Kötbullar with mashed potatoes. The next stop will be your destination."},
            "9912e0beec0b4fd3854eb6fca1501669": {"floor": 3, "room": "C", "voice_message": "Congratulations, you've arrived at your destination. I hope you enjoyed the guidance. Have a nice day!"},
            "3700ad2975ee4ec999fe9a8e27192c3a": {"floor": 4, "room": "D", "voice_message": "Test Beacon 1"},
            "d369a9b2a854459e8e9d5403ee320eef": {"floor": 5, "room": "E", "voice_message": "Test Beacon 2"}

        }

    def get_location(self, uuid):
        # check if the UUID is in the databank
        if uuid in self.databank:
            # return the location if found
            return self.databank[uuid]
        else:
            # return None if not found
            return None
