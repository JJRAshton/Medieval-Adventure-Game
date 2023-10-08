import weaponImages from "./weaponImages";


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
        this.imageSource = weaponImages[weaponType];
        this.range = range; // Range is attached to weapon to reflect how the backend does it, but should really be on an AttackOption
    }
}