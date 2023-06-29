import sharpStick from "../../../images/weapons/sharpStick.png"
import sickle from "../../../images/weapons/sickle.png"
import hatchet from "../../../images/weapons/hatchet.png"
import club from "../../../images/weapons/club.png"
import trident from "../../../images/weapons/trident.png"
import greataxe from "../../../images/weapons/greataxe.png"
import war_scythe from "../../../images/weapons/war_scythe.png"

let imagesDict = new Map();
imagesDict.set("sharp_stick", sharpStick);
imagesDict.set("sickle", sickle);
imagesDict.set("hatchet", hatchet);
imagesDict.set("club", club);
imagesDict.set("trident", trident);
imagesDict.set("greataxe", greataxe);
imagesDict.set("war scythe", war_scythe);

/**
 * This class is envisioned to contain information needed 
 * for attacks that apply to that weapon specific (stuff like light/normal?).
 */
export default class Weapon {
    public name: String;
    public imageSource: string;
    public range: number;

    constructor(weaponType: string, range: number) {
        this.name = weaponType;
        this.imageSource = imagesDict.get(weaponType);
        this.range = range; // Range is attached to weapon to reflect how the backend does it, but should really be on an AttackOption
    }
}