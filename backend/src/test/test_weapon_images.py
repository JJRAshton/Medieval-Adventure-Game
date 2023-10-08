import unittest
import glob

from dnd.backend.processing.entities.classes.player_class import ALL
from dnd.backend.processing.entities.stats.make_dataframes import ENTITY_STAT_PROVIDER

class TestWeaponImages(unittest.TestCase):
    
    def test_image_for_all_weapons(self):
        all_weapons = set()
        weapons_with_images = {image.split("/")[-1].removesuffix(".png") for image in glob.glob("../../frontend/src/images/weapons/*.png")}
        for player_class in ALL:
            df = ENTITY_STAT_PROVIDER.weapons
            available_weapons = df[(df.Type.isin(player_class.weapons))].index.tolist()
            all_weapons = all_weapons.union(available_weapons)

        print(f"All weapons: {all_weapons}")
        missing = all_weapons.difference(weapons_with_images)
        extra = weapons_with_images.difference(all_weapons)
        assert not missing, f"The following {len(missing)} weapons are missing images: {missing}"
        assert not extra, f"The following {len(extra)} weapons do not need images: {extra}"