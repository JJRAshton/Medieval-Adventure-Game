import sharpStick from "./images/weapons/sharpStick.png"
import sickle from "./images/weapons/sickle.png"
import hatchet from "./images/weapons/hatchet.png"
import club from "./images/weapons/club.png"

let imagesDict = new Map();
imagesDict.set("sharp_stick", sharpStick);
imagesDict.set("sickle", sickle);
imagesDict.set("hatchet", hatchet);
imagesDict.set("club", club);

/**
 * This class is envisioned to contain information needed 
 * for attacks that apply to that weapon specific (stuff like light/normal?).
 */
export default class Weapon {

    constructor(weaponType, range) {
        this.name = weaponType;
        this.imageSource = imagesDict.get(weaponType);
        this.range = range; // Range is attached to weapon to reflect how the backend does it, but should really be on an AttackOption
    }
}