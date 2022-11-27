import math

# Hardcoded stuff for testing
row = [0 for i in range(0,10)]
map_grid = [row for j in range(0,10)]

# locations is the result of a locationsRequest
locations = {'1': (1, 1), '2': (2, 5), '3': (9, 10), '4': (1,2)}

class Brain1:

    """
    Brain1 is an AI with the following decision process:
     - Turn begins
     - Makes a dictionary of all character locations, starting with the nearest one
     - Chooses the closest character of the opposing team as its target
     - While the target is out of attack range, moves towards the target (prioritises diagonal movement)
     - Attacks when the target is in range, using all of its actions to attack
     - If movement runs out, ends turn without doing anything else
     - If actions run out, ends turn without doing anything else

    What Brain1 does NOT do:
     - Move around terrain blocking its path (will end turn early instead)
     - Choose a 'new target' if it kills the one picked at the start of its turn
     - Kite if it has a ranged weapon
     - Factor in anything other than 'closeness' when choosing a target
     - Have an awareness of its own mortality
     - Do anything other than move and attack
    """

    def __init__(self, backend, id):
        self.locations = backend.locationsRequest()
        self.my_id = id
        self.my_location = backend.locationsRequest()[id]
        self.my_range = backend.infoRequest(id)['Max_range']
        self.my_movement = backend.infoRequest(id)['Remaining_movement']
        self.actions = backend.infoRequest(id)['Action_number']

    def check_distance(self, char_id):
        target_location = self.locations[char_id]
        x_distance = self.my_location[0] - target_location[0]
        y_distance = self.my_location[1] - target_location[1]
        distance = math.sqrt(x_distance ** 2 + y_distance ** 2)

        return distance

    def check_team(self, char_id, backend):
        print(char_id)
        team = backend.infoRequest(char_id)['Team'] # 1 is player, 2 is npc

        return team

    def choose_target(self, backend):
        character_distances = {}
        for option in self.locations:
            option_distance = self.check_distance(option)
            character_distances.update({option: option_distance})
        character_distances.pop(self.my_id)

        closest_chars = sorted(character_distances.items(), key=lambda item: item[1])
        print(closest_chars)
        # Go through the list to find the nearest character of the opposing team
        for char in closest_chars:
            if self.check_team(char[0], backend) == 1:
                target = char
                print(f"chosen target is {char}")
                break

        return target

    def check_can_attack(self, target):
        if self.my_range / 5 > self.check_distance(target):
            print("target is in range!")
            return True
        return False

# Temporary backend references below
    def approach_and_attack_target(self, backend, target):
        target_location = self.locations[target[0]]
        while self.actions > 0:
            while not self.check_can_attack(target[0]):
                x_movement = int(target_location[0]-self.my_location[0])/abs(target_location[0]-self.my_location[0])
                y_movement = int(target_location[1]-self.my_location[1])/abs(target_location[1]-self.my_location[1])
                movement_coords = (self.my_location[0] + x_movement, self.my_location[1] + y_movement)
                # I think this line will also make a move request, not just check if true?
                if not backend.moveRequest(self.my_id, movement_coords):
                    self.actions = 0    # Not really needed now
                    print('ran out of movement')
                    return
            backend.attackRequest(self.my_id, target[0])
            self.actions -= 1
        # Ends turn after a move request is denied (i.e. out of movement) or using up all actions

print('game')