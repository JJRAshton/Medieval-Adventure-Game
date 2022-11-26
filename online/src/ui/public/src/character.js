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
        let blah = <ul className="stats" style={this.statsStyle}>
            <li>Strength: {this.strength}</li>
            <li>Dexterity: {this.dexterity}</li>
            <li>Health: {this.health} / {this.maxHealth}</li>
            <li>Weapon: {this.weapon}</li>
        </ul>
        console.log(blah);
        return blah;
    }
   
}