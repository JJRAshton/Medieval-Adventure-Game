# Checks for what type of entity the id is
def is_character(entID: str) -> bool:
    return isinstance(entID, str) and entID.startswith('character')

def is_object(entID: str) -> bool:
    return isinstance(entID, str) and entID.startswith('object')

def is_item(entID: str) -> bool:
    return isinstance(entID, str) and entID.startswith('item')


class IDGenerator:
    def __init__(self):
        self.__character_ids: int = 0
        self.__object_ids: int = 0
        self.__item_ids: int = 0

    def get_character_id(self) -> str:
        self.__character_ids += 1
        return f'character_{self.__character_ids}'

    def get_object_id(self) -> str:
        self.__object_ids += 1
        return f'object{self.__object_ids}'

    def get_item_id(self) -> str:
        self.__item_ids += 1
        return f'item{self.__item_ids}'