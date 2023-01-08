import AttackOption from "./attackOption";
import Character from "../parsing/character";
import { GameUISelection } from "../gameUISelection";

/**
 * Type used to set attack options
 */
export type AttackOptions = {
    target?: any;
    attackType?: any;
}

/**
 * Class representing a game scene attack selection
 */
export default class Attack implements GameUISelection {
    target: Character | null;
    attackType: AttackOption | null;

    constructor(options: AttackOptions) {
        this.target = null;
        this.attackType = null; // This is an AttackOption or null
        this.setOptions(options);
    }

    setOptions(options: { target?: any; attackType?: any; }) {
        if (options.target) {
            this.target = options.target;
            console.log("Setting target");
        }
        if (options.attackType) {
            this.attackType = options.attackType
            console.log("setting attack type");
        }
    }

    setAttackType(attackType: AttackOption): void {
        this.attackType = attackType;
    }

    setTarget(target: Character): void {
        this.target = target;
    }

    confirmAttack(): boolean {
        // boolean
        return (this.target !== null && this.attackType !== null);
    }
}