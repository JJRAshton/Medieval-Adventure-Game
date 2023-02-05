import React from "react";

import orc from "../../../images/orc.png";
import me from "../../../images/me.png";
import notMe from "../../../images/notMe.png";

import PlayerInfoParser from "./playerInfoParser";
import Weapon from "../attack/weapon";
import AttackOption from "../attack/attackOption";

type CharacterInfo =  {
    Weapons: JSON;
    Attacks: JSON;
    Stats: Array<number>;
    Health: number;
    Max_health: number;
    Range: number;
    Remaining_movement: number;
    Team: any; 
}

export default class Character {
    public infoReceived: boolean;
    public id: number;
    public x: number;
    public y: number;
    public health: any;
    
    private statsStyle: { fontSize: number; listStyle: string; justifyContent: string; textAlign: string; };
    
    private static infoParser = new PlayerInfoParser();

    public weapons: Array<Weapon> | null;
    public attacks: Array<AttackOption>;
    public stats: Map<string, number>;
    public armour: null;
    public inventory: null;
    public maxHealth: number;
    public range: number;
    public movesLeft: number;
    public team: number;

    public image: HTMLImageElement;
    public imageLoaded: boolean;
    
    constructor(id: number, x: number, y: number) {
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

    setPosition(x: number, y: number) {
        this.x = x;
        this.y = y;
    }

    update(updateInfo: { Health: any; coords: number[]; }) {
        this.health = updateInfo.Health;
        this.x = updateInfo.coords[0];
        this.y = updateInfo.coords[1];
    }

    /**
     * Called when a full player info is received from the server
     */
    construct(characterInfo: CharacterInfo, isPlayer: any, selectionHandler: any) {
        console.log(characterInfo);

        this.weapons = Character.infoParser.parseWeapons(characterInfo.Weapons); // Not yet implemented
        this.attacks = Character.infoParser.parseAttacks(characterInfo.Attacks, selectionHandler);
        this.stats = Character.infoParser.parseStats(characterInfo.Stats);
        this.armour = Character.infoParser.parseArmour(null); // Not yet implemented
        this.inventory = Character.infoParser.parseInventory(null); // Not yet implemented

        this.health = characterInfo.Health;
        this.maxHealth = characterInfo.Max_health;
        this.range = Math.floor(characterInfo.Range / 5); // This seems like a random thing to expose given that it should be attainable from the attacks/weapons as well?
        this.movesLeft = Math.floor(characterInfo.Remaining_movement / 5);
        this.team = characterInfo.Team;

        this._loadImage(isPlayer);
        
        this.infoReceived = true;
    }

    private _loadImage(isPlayer: boolean) {
        this.image = new Image()
        this.imageLoaded = false;
        this.image.onload = this._loadImage.bind(this);
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
            console.log("An error occured loading image: " + error);
        }
    }

    public checkAttackable(character: Character): boolean {
        return (this.team !== character.team)
            && Math.max(Math.abs(this.x - character.x), Math.abs(this.y - character.y)) <= this.range;
        }
}
