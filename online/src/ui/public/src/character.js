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
        }
        this.initialiseStats()
    }

    initialiseStats() {
        this.strength = 20;
        this.dexterity = 23;
        this.health = 100;
        this.maxHealth = 200;
        this.weapon = "Twig";
    }

    setPosition(x, y) {
        this.x = x;
        this.y = y;
    }

    construct(characterInfo) {
        console.log(characterInfo);

        this.attacks = characterInfo.Attacks;
        this.armour = null; // Not yet implemented
        this.health = characterInfo.Health;
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
            return <ul className="stats" style={this.statsStyle}> {children} </ul>
        }
        else {
            return <ul className="stats" style={this.statsStyle}>Could not load attacks</ul>
        }
    }

    createAttackLi(attack) {
        return <li key={attack.Name+"_"+attack.Weapon}>{attack.Name} ({attack.Weapon})</li>
    }

    renderStats() {
        if (this.infoReceived) {
            let children = [];
            this.stats.forEach((value, stat) => {children.push(this.createStatLi(stat, value))});
            return <ul className="stats" style={this.statsStyle}> {children} </ul>
        }
        else {
            return <ul className="stats" style={this.statsStyle}>Could not load stats</ul>
        }
    }

    createStatLi(statName, stat) {
        return <li key={statName}>{statName}: {stat}</li>
    }
   
}