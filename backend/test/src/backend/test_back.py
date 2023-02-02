from unittest import TestCase
from dnd.backend.processing.back import Back


class TestBack(TestCase):

    def testMovement(self):
        back = Back()
        first_chr = back.characters[0]
        first_chr_coords = first_chr.coords

        back.moveCharacter(first_chr.id, [first_chr_coords[0], first_chr_coords[1] + 1])
        assert first_chr.coords == (first_chr_coords[0], first_chr_coords[1] + 1)
        assert back.characterGrid[first_chr_coords[0]][first_chr_coords[1] + 1].id == first_chr.id
        back.moveCharacter(first_chr.id, [first_chr_coords[0], first_chr_coords[1]])
        assert first_chr.coords == (first_chr_coords[0], first_chr_coords[1])
        assert back.characterGrid[first_chr_coords[0]][first_chr_coords[1]].id == first_chr.id

