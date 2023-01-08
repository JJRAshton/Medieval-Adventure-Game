import AttackOption from "./attackOption";
import Weapon from "./weapon";

export default class PlayerInfoParser {

    parseWeapons(weaponInfo) {
        return null;
    }

    parseAttacks(attackInfo, selectionHandler) {
        let attacks = new Array();
        for (let attack of attackInfo) {
            attacks.push(new AttackOption(new Weapon(attack.Weapon, Math.floor(attack.Range / 5)), attack.Name, selectionHandler));
        }
        return attacks;
    }

    parseArmour(armourInfo) {
        return null;
    }

    parseInventory(inventoryInfo) {
        return null;
    }

    parseStats(statInfo) {
        let statMap = new Map();
        statMap.set("Constitution", statInfo.CON);
        statMap.set("Dexterity", statInfo.DEX);
        statMap.set("Strength", statInfo.STR);
        statMap.set("Wit", statInfo.WIT);
        return statMap;
    }

}