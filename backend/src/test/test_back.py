import unittest

from dnd.backend.processing.back import Back
from dnd.backend.processing import hub
from dnd.backend.processing.id_generator import IDGenerator


class TestBack(unittest.TestCase):

    def test_movement(self):
        """ Test movement on back """
        back = Back(1, 1, True, IDGenerator())
        first_chr = back.characters[0]
        first_chr_coords = first_chr.coords
        back.moveCharacter(first_chr.id, [first_chr_coords[0], first_chr_coords[1] + 1])
        assert first_chr.coords == (first_chr_coords[0], first_chr_coords[1] + 1)
        assert back.characterGrid[first_chr_coords[0]][first_chr_coords[1] + 1].id == first_chr.id
        back.moveCharacter(first_chr.id, [first_chr_coords[0], first_chr_coords[1]])
        assert first_chr.coords == (first_chr_coords[0], first_chr_coords[1])
        assert back.characterGrid[first_chr_coords[0]][first_chr_coords[1]].id == first_chr.id

    def test_id_generation(self):
        back = Back(1, 4, True, IDGenerator())
        for key_id, entity in back.entities.items():
            assert key_id == entity.id, f"Entity id {entity.id} did not match is key {key_id}" 
            assert hub.is_character(key_id) or hub.is_item(key_id) or hub.is_object(key_id), f"Id '{key_id}' was not of the expected form"
        
        assert len(back.characters) > 0
        character_ids = [character.id for character in back.characters]
        assert len(character_ids) == len(character_ids), "Ids were not unique"
        for character in back.characters:
            assert hub.is_character(character.id), f"Id '{character.id}' was not of the expected form"
        
        # assert len(back.objects) > 0
        objects_ids = [obj.id for obj in back.objects]
        assert len(objects_ids) == len(objects_ids), "Ids were not unique"
        for obj in back.objects:
            assert hub.is_object(obj.id), f"Id '{obj.id}' was not of the expected form"
        
        assert len(back.items) > 0
        item_ids = [item.id for item in back.items]
        assert len(item_ids) == len(item_ids), "Ids were not unique"
        for item in back.items:
            assert hub.is_item(item.id), f"Id '{item.id}' was not of the expected form"



if __name__ == '__main__':
    unittest.main()