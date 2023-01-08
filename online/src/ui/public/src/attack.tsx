import AttackOption from "./attackOption";
import Character from "./character";
import { GameUISelection } from "./gameUISelection";

export default class Attack implements GameUISelection {
    target: Character | null;
    attackType: AttackOption | null;

    constructor(options: { target: any; attackType: any; }) {
        this.target = null;
        this.attackType = null; // This is an AttackOption or null
        this.setOptions(options);
    }

    setOptions(options: { target: any; attackType: any; }) {
        if (options.target) {
            this.target = options.target;
            console.log("Setting target");
        }
        if (options.attackType) {
            this.attackType = options.attackType
            console.log("setting attack type");
        }
    }

    setAttackType(attackType: AttackOption) {
        this.attackType = attackType;
    }

    setTarget(target: Character) {
        this.target = target;
    }

    confirmAttack() {
        // boolean
        return (this.target && this.attackType);
    }
}