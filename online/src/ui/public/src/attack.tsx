export default class Attack {

    /**
     * options = {target, attackType}
     */
    constructor(options) {
        this.target = null;
        this.attackType = null; // This is an AttackOption or null
        this.setOptions(options);
    }

    setOptions(options) {
        if (options.target) {
            this.target = options.target;
            console.log("Setting target");
        }
        if (options.attackType) {
            this.attackType = options.attackType
            console.log("setting attack type");
        }
    }

    setAttackType(attackType) {
        this.attackType = attackType;
    }

    setTarget(target) {
        this.target = target;
    }

    confirmAttack() {
        // boolean
        return (this.target && this.attackType);
    }
}