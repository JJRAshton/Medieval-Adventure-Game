import React from "react";

export default class Character {
    
    constructor(id, x, y) {
        this.infoReceived = false; // Keeps track of whether the full player info for this character has been received
        this.id = id;
        this.x = x;
        this.y = y;
        this.statsStyle = {
            fontSize: 20,
            listStyle: "none",
            justifyContent: "center",
            textAlign: "center"
        }
    }

    setPosition(x, y) {
        this.x = x;
        this.y = y;
    }

    update(updateInfo) {
        this.health = updateInfo.Health;
        this.x = updateInfo.coords[0];
        this.y = updateInfo.coords[1];
    }

    construct(characterInfo) {
        console.log(characterInfo);

        this.attacks = characterInfo.Attacks;
        this.armour = null; // Not yet implemented
        this.health = characterInfo.Health;
        this.maxHealth = characterInfo.Max_health;
        this.inventory = null // Not yet implemented
        this.range = characterInfo.Max_range;
        this.movesLeft = Math.floor(characterInfo.Remaining_movement / 5);
        this.stats = this.constructStats(characterInfo.Stats);
        this.team = characterInfo.Team;
        this.weapons = this.constructWeapons(characterInfo.Weapons); // Not yet implemented
        
        this.infoReceived = true;
    }

    constructStats(statInfo) {
        let statMap = new Map();
        statMap.set("Constitution", statInfo.CON);
        statMap.set("Dexterity", statInfo.DEX);
        statMap.set("Strength", statInfo.STR);
        statMap.set("Wit", statInfo.WIT);
        return statMap;
    }

    constructWeapons (weaponInfo) {
        return null;
    }

    renderAttacks() {
        if (this.infoReceived) {
            let children = [];
            this.attacks.forEach((attack) => {children.push(this.createAttackLi(attack))});
            return <div className="stats"> {children} </div>
        }
        else {
            return <div className="stats">Could not load attacks</div>
        }
    }

    createAttackLi(attack) {
        return <div key={attack.Name+"_"+attack.Weapon}>{attack.Name} ({attack.Weapon})</div>
    }

    renderStats() {
        if (this.infoReceived) {
            let children = [];
            this.stats.forEach((value, stat) => {children.push(this.createStatRow(stat, value))});
            return <div className="stats"><table className="statTable"><tbody>{children}</tbody></table></div>
        }
        else {
            return <div className="stats">Could not load stats</div>
        }
    }

    createStatRow(statName, stat) {
        return <tr key={statName}><td>{statName}</td><td>{stat}</td></tr>
    }
   
}