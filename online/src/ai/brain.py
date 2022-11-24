import math

# Hardcoded stuff
row = [0 for i in range(0,10)]
map_grid = [row for j in range(0,10)]

# locations is the result of a locationsRequest
locations = {'1': (1, 1), '2': (2, 5), '3': (9, 10), '4': (1,2)}

class Brain:
    def __init__(self, backend, id):
        self.locations = backend.locationsRequest()
        self.my_id = id
        self.my_location = backend.locationsRequest()[id]
        #self.movement = backend.infoRequest(id)[Remaining_movement]

    def choose_target(self, backend):
        character_distances = {}
        for option in self.locations:
            target_location = self.locations[option]
            x_distance = self.my_location[0] - target_location[0]
            y_distance = self.my_location[1] - target_location[1]
            distance = math.sqrt(x_distance**2 + y_distance**2)
            character_distances.update({option: distance})

        closest_chars = sorted(character_distances.items(), key=lambda item: item[1])

        for char in closest_chars:
            if backend.infoRequest(char)['Team'] == 0:
                print('character is hostile')
                squares_away = self.movement_required(char)
                if self.movement < squares_away:
                    pass


    def movement_required(self, target_location):
        squares = 2 # avoid error
        print(f"target is in range by moving {squares} squares")
        return squares

print('game')