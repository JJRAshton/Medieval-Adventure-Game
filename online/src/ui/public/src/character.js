import React from "react";

export default class Character {
    
    constructor(id, x, y) {
        this.id = id;
        this.x = x;
        this.y = y;
        this.statsStyle = {
            fontSize: 20,
            listStyle: "none"

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

    renderStats() {
        return <ul className="stats" style={this.statsStyle}>
            {this.createStatLi("Strength", this.strength)}
            {this.createStatLi("Dexterity", this.dexterity)}
            {this.createStatLi("Health", this.health)}
            {this.createStatLi("Weapon", this.weapon)}
        </ul>
    }

    createStatLi(statName, stat) {
        return <li>
            <div>{statName}</div>
            <div>{stat}</div>
        </li>
    }
   
}