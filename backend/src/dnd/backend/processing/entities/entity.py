from typing import Tuple


class Entity:

    def __init__(self, entityName: str):
        self.name = entityName
        self.id = 0

        self.size = 0
        
        self.coords = (0, 0)

    def __eq__(self, other: object):
        return self.id == other
    
    # Moves to new coords
    def move(self, vector: Tuple[int, int]):
        self.coords = (self.coords[0]+vector[0], self.coords[1]+vector[1])

