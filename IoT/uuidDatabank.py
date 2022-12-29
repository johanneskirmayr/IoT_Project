# DataBank class to store and retrieve UUIDs and their locations

class DataBank:
    def __init__(self):
        # hardcoded databank of UUIDs and their locations
        self.databank = {
            # Start beacon
            "8882358095064d379d5b437e33a09e8c": {"floor": 1, "room": "A", "previous_room": "Start", "voice_message": "Welcome to Stockholm University, I am happy to navigate you to your destination. I will also give you some insights of important spots on our way!", "bridge_voice_message": ""},
            # Waypoint beacons
            "2a7f6ba12ff44a6aa74df05abc062b0a": {"floor": 2, "room": "B", "previous_room": "A", "voice_message": "Great, we made it to our next waypoint. On the right you can see the university's cafeteria, today's special dish is Kötbullar with mashed potatoes.", "bridge_voice_message": "Your next waypoint is room B, the cafeteria!"},
            "d519e1d9ed6f45a1a052b39fc31683e1": {"floor": 2, "room": "C", "previous_room": "A", "voice_message": "Great, we made it to our next waypoint. On the right you can see the university's library, If you want to borrow a book, please contact the front desk right after the entry.", "bridge_voice_message": "Your next waypoint is room C, the libarary!"},
            # Destination beacons
            "9912e0beec0b4fd3854eb6fca1501669": {"floor": 3, "room": "D", "previous_room": "B", "voice_message": "", "bridge_voice_message": "You next stop is already your destination, room number D!"},
            "0c87386ed6cf481b8a7393c075d85d43": {"floor": 3, "room": "E", "previous_room": "B", "voice_message": "", "bridge_voice_message": "You next stop is already your destination, room number E!"},
            "1f2437baded74f9ea308d7bf06a8a406": {"floor": 3, "room": "F", "previous_room": "C", "voice_message": "", "bridge_voice_message": "You next stop is already your destination, room number F!"},
            
            #"3700ad2975ee4ec999fe9a8e27192c3a": {"floor": 4, "room": "D", "previous_room":, "voice_message": "Test Beacon 1"},
            #"d369a9b2a854459e8e9d5403ee320eef": {"floor": 5, "room": "E", "previous_room":, "voice_message": "Test Beacon 2"}

        }

    def get_location(self, uuid):
        """
        Returns the data of the beacon with the given UUID
        """
        # check if the UUID is in the databank
        if uuid in self.databank:
            # return the location if found
            return self.databank[uuid]
        else:
            # return None if not found
            return None

    def get_way(self, room):
        """
        Builds a list of the beacons that the user has to pass to get to the destination
        """
        # initialize list of uuids that the user has to pass to get to the destination
        waypoints = []

        # get the uuid of the destination room
        for key in self.databank:
            if self.databank[key]["room"] == room:
                uuid = key
        if uuid == None:
            print("Room not found in databank")

        # check if the UUID is in the databank
        if uuid in self.databank:
            while self.databank[uuid]["previous_room"] != "Start":
                waypoints.append(uuid)
                uuid = self.get_previous_room(uuid)
            waypoints.append(uuid)
            return waypoints
        else:
            # return None if not found
            print("UUID not found in databank")
            return None
        
    def get_previous_room(self, uuid):
        """
        Returns the uuid of the previous room from the given UUID
        """
        # check if the UUID is in the databank
        if uuid in self.databank:
            # return uuid of previous room if found
            previous_room = self.databank[uuid]["previous_room"]
            previous_uuid = [key for key, value in self.databank.items() if value["room"] == previous_room]
            return previous_uuid[0]
        else:
            # return None if not found
            print("UUID not found in databank")
            return None