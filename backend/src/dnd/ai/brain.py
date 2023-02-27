import math

from ..backend.back_requests import Requests

from typing import List, Tuple

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

    def __init__(self, backend: Requests, bot_id: int):
        self.locations = backend.locationsRequest()
        self.player_ids: List[int] = [x for x in backend.locationsRequest() if backend.infoRequest(x)['Team'] == 1]
        self.my_id: int = bot_id
        self.my_location: Tuple[int, int] = backend.locationsRequest()[bot_id]
        self.my_range: int = backend.infoRequest(bot_id)['Range']
        self.my_movement: int = backend.infoRequest(bot_id)['Remaining_movement']
        self.actions: int = backend.infoRequest(bot_id)['Action_number']

    def check_distance(self, char_id: int):
        target_location: Tuple[int, int] = self.locations[char_id]
        x_distance: int = self.my_location[0] - target_location[0]
        y_distance: int = self.my_location[1] - target_location[1]
        distance = math.sqrt(x_distance ** 2 + y_distance ** 2)

        return distance

# Not currently used but might in future
    def check_team(self, char_id: int, backend: Requests):
        print(char_id)
        team: int = backend.infoRequest(char_id)['Team']  # 1 is player, 2 is npc

        return team

    def choose_target(self) -> int:
        character_distances = {}
        for option in self.player_ids:
            option_distance = self.check_distance(option)
            character_distances[option] = option_distance

        target_id: int = sorted(character_distances.items(), key=lambda item: item[1])[0][0]
        print(f"chosen target is {target_id}")

        return target_id

    def check_can_attack(self, target_id: int):
        if self.my_range / 5 >= self.check_distance(target_id):
            print("target is in range!")
            return True
        return False

# Temporary backend references below
    def approach_and_attack_target(self, backend: Requests, target_id: int):
        target_location: Tuple[int, int] = self.locations[target_id]
        while self.actions > 0:
            while not self.check_can_attack(target_id):
                if self.my_movement <= 0:
                    print('No movement left, ending turn early')
                    return
                else:
                    sign = lambda i: 0 if not i else int(i/abs(i))
                    x_diff = (target_location[0] - self.my_location[0])
                    x_movement = sign(x_diff)
                    y_diff = (target_location[1] - self.my_location[1])
                    y_movement = sign(y_diff)
                    movement_coords = (int(self.my_location[0] + x_movement), int(self.my_location[1] + y_movement))
                    # I think this line will also make a move request, not just check if true?
                    if backend.moveRequest(self.my_id, movement_coords):
                        self.my_location = backend.locationsRequest()[self.my_id]
                        self.my_movement -= 1
                    else:
                        self.actions = 0    # Not really needed now
                        print('Invalid move requested, ending turn')
                        return
            backend.attackRequest(self.my_id, target_id)
            self.actions -= 1
        # Ends turn after using all actions, being unable to move or attack, or making an invalid move request

"""
Brain2 plan:

Same as Brain1 but with additional features:
 - Will navigate around terrain walls:
        - Has a 'line-of-sight' check
        - Can calculate the nearest location at which it will gain line-of-sight to a potential target
        - The perceived distance to targets blocked by terrain includes this distance needed to gain line-of-sight

"""

print('Started')
