import unittest, sys

from dnd.backend.processing.back import Back


class TestBack(unittest.TestCase):

    def test_movement(self):
        """ Test movement on back """
        back = Back(1, 1, True)
        first_chr = back.characters[0]
        first_chr_coords = first_chr.coords
        back.moveCharacter(first_chr.id, [first_chr_coords[0], first_chr_coords[1] + 1])
        assert first_chr.coords == (first_chr_coords[0], first_chr_coords[1] + 1)
        assert back.characterGrid[first_chr_coords[0]][first_chr_coords[1] + 1].id == first_chr.id
        back.moveCharacter(first_chr.id, [first_chr_coords[0], first_chr_coords[1]])
        assert first_chr.coords == (first_chr_coords[0], first_chr_coords[1])
        assert back.characterGrid[first_chr_coords[0]][first_chr_coords[1]].id == first_chr.id

if __name__ == '__main__':
    unittest.main()