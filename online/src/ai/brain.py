import math


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

    def __init__(self, backend, bot_id):
        self.locations = backend.locationsRequest()
        self.player_ids = [x for x in backend.locationsRequest() if backend.infoRequest(x)['Team'] == 1]
        self.my_id = bot_id
        self.my_location = backend.locationsRequest()[bot_id]
        self.my_range = backend.infoRequest(bot_id)['Range']
        self.my_movement = backend.infoRequest(bot_id)['Remaining_movement']
        self.actions = backend.infoRequest(bot_id)['Action_number']

    def check_distance(self, char_id):
        target_location = self.locations[char_id]
        x_distance = self.my_location[0] - target_location[0]
        y_distance = self.my_location[1] - target_location[1]
        distance = math.sqrt(x_distance ** 2 + y_distance ** 2)

        return distance

# Not currently used but might in future
    def check_team(self, char_id, backend):
        print(char_id)
        team = backend.infoRequest(char_id)['Team']  # 1 is player, 2 is npc

        return team

    def choose_target(self):
        character_distances = {}
        for option in self.player_ids:
            option_distance = self.check_distance(option)
            character_distances.update({option: option_distance})

        target_id = sorted(character_distances.items(), key=lambda item: item[1])[0]
        print(f"chosen target is {target_id}")

        return target_id

    def check_can_attack(self, target_id):
        if self.my_range / 5 >= self.check_distance(target_id):
            print("target is in range!")
            return True
        return False

# Temporary backend references below
    def approach_and_attack_target(self, backend, target_id):
        target_location = self.locations[target_id]
        while self.actions > 0:
            while not self.check_can_attack(target_id):
                sign = lambda i: 0 if not i else int(i/abs(i))
                x_diff = (target_location[0] - self.my_location[0])
                x_movement = sign(x_diff)
                y_diff = (target_location[1] - self.my_location[1])
                y_movement = sign(y_diff)
                movement_coords = (int(self.my_location[0] + x_movement), int(self.my_location[1] + y_movement))
                # I think this line will also make a move request, not just check if true?
                if backend.moveRequest(self.my_id, movement_coords):
                    self.my_location = backend.locationsRequest()[self.my_id]
                else:
                    self.actions = 0    # Not really needed now
                    print('ran out of movement')
                    return
            backend.attackRequest(self.my_id, target_id)
            self.actions -= 1
        # Ends turn after a move request is denied (i.e. out of movement) or using up all actions


print('game')
