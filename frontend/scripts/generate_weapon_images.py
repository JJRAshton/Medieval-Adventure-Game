
import glob


def to_camel_case(weapon):
    words = weapon.split("_")
    camel_case = words[0] + "".join({word[0].upper() + word[1:] for word in words[1:]})

def generate_weapon_images():
    with open("./weaponImages.tsx", "w") as f:
        f.write("/** --------------------------------------------- */\n")
        f.write("/** GENERATED CODE, see generate_weapon_images.py */\n")
        f.write("/** --------------------------------------------- */\n")
        f.write("\n")
        f.write("let weaponImages = {}\n")
        f.write("\n")
        weapons_with_images = {image.split("/")[-1].removesuffix(".png") for image in glob.glob("./frontend/src/images/weapons/*.png")}
        for weaponImage in weapons_with_images:
            f.writelines(f'import {weaponImage} from "../../../images/weapons/{weaponImage}.png"\n')
        f.write("\n")
        for weaponImage in weapons_with_images:
            f.writelines(f'weaponImages["{weaponImage}"] = {weaponImage};\n')
        f.write("\n")
        f.write("export default weaponImages\n")
        






if __name__ == "__main__":
    generate_weapon_images()