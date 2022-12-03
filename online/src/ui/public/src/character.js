import React from "react";

import orc from "./images/orc.png";
import me from "./images/me.png";
import notMe from "./images/notMe.png";

import PlayerInfoParser from "./playerInfoParser";

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

    construct(characterInfo, isPlayer) {
        console.log(characterInfo);

        this.infoParser = new PlayerInfoParser(); // This class is pretty static

        this.weapons = this.infoParser.parseWeapons(characterInfo.Weapons); // Not yet implemented
        this.attacks = this.infoParser.parseAttacks(characterInfo.Attacks);
        this.stats = this.infoParser.parseStats(characterInfo.Stats);
        this.armour = this.infoParser.parseArmour(); // Not yet implemented
        this.inventory = this.infoParser.parseInventory(); // Not yet implemented

        this.health = characterInfo.Health;
        this.maxHealth = characterInfo.Max_health;
        this.range = characterInfo.Max_range; // This seems like a random thing to expose given that it should be attainable from the attacks/weapons as well?
        this.movesLeft = Math.floor(characterInfo.Remaining_movement / 5);
        this.team = characterInfo.Team;

        this.loadImage(isPlayer);
        
        this.infoReceived = true;

    }

    loadImage(isPlayer) {
        this.image = new Image()
        this.imageLoaded = false;
        this.image.onload = this.loadImage.bind(this);
        this.image.onload = () => {
            this.imageLoaded = true;
        }
        if (isPlayer) {
            this.image.src = me;
        }
        else if (this.team === 1) {
            this.image.src = notMe;
        }
        else {
            this.image.src = orc;
        }
        this.image.onerror = (error) => {
            console.log("An error occured loading image" + error);
        }
    }

    renderAttacks() {
        if (this.infoReceived) {
            let children = [];
            console.log(this.attacks);
            this.attacks.forEach((attack) => {children.push(attack.renderAttackOptionElement(attack))});
            console.log(children);
            return <div className="attack stats"><table><tbody>{children}</tbody></table></div>
        }
        else {
            return <div className="attack stats">Could not load attacks</div>
        }
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