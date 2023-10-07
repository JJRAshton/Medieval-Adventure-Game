import React from "react";

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

let checkAttackable = (attacker: Character, target: Character) => {
    return (attacker.team !== target.team)
        && Math.max(Math.abs(attacker.x - target.x), Math.abs(attacker.y - target.y)) <= attacker.range;
}

type Character  = {
    infoReceived: boolean;
    id: string;
    x: number;
    y: number;
    health: number;
    weapons: Array<Weapon> | null;
    stats: Record<string, number>;
    armour: null;
    inventory: null;
    maxHealth: number;
    range: number;
    movesLeft: number;
    team: number;
}

const NULL_CHARACTER: Character = {
    infoReceived: false,
    id: "null_id",
    x: 0,
    y: 0,
    health: 0,
    weapons: null,
    stats: {},
    armour: null,
    inventory: null,
    maxHealth: 0,
    range: 0,
    movesLeft: 0,
    team: 0,
}

const createCharacterInitial = (initialCharacterJSON): Character => {
    const x = initialCharacterJSON[1][0];
    const y = initialCharacterJSON[1][1];
    if (x !== 0 && !x || y !== 0 && !y) {
        console.log("Setting invalid position in createCharacterInitial: ")
        console.log([x, y])
    }
    return {
        ...NULL_CHARACTER,
        id: initialCharacterJSON[0],
        x: initialCharacterJSON[1][0],
        y: initialCharacterJSON[1][1]
    }
}

const setPosition = (character: Character, x: number, y: number): Character => {
    if (x !== 0 && !x || y !== 0 && !y) {
        console.log("Setting invalid position in setPosition: ")
        console.log([x, y])
    }
    return {
        ...character, 
        x: x,
        y: y
    }
}

const updateCharacter = (character: Character, health: number, coords) => {
    const x = coords[0];
    const y = coords[1];
    if (x !== 0 && !x || y !== 0 && !y) {
        console.log("Setting invalid position in updateCharacters: ")
        console.log([x, y])
    }
    return {
        ...character,
        health,
        x: coords[0],
        y: coords[1]
    }
}

/**
 * A rubbish and hopefully temporary way of telling if something is a character.
 */
const isCharacter = (character: any): boolean => {
    return character
        && "x" in character 
        && "y" in character
        && "id" in character
}

const CHARACTER_INFO_PARSER = new PlayerInfoParser();

const constructCharacter = (character: Character, characterInfo: CharacterInfo, isPlayer: boolean) => {
    return {
        ...character,
        weapons: CHARACTER_INFO_PARSER.parseWeapons(characterInfo.Weapons), // Not yet implemented
        // attacks: CHARACTER_INFO_PARSER.parseAttacks(characterInfo.Attacks, selection, setSelection),
        stats: CHARACTER_INFO_PARSER.parseStats(characterInfo.Stats),
        armour: CHARACTER_INFO_PARSER.parseArmour(null), // Not yet implemented
        inventory: CHARACTER_INFO_PARSER.parseInventory(null), // Not yet implemented

        health: characterInfo.Health,
        maxHealth: characterInfo.Max_health,
        range: Math.floor(characterInfo.Range / 5),
        movesLeft: Math.floor(characterInfo.Remaining_movement / 5),
        team: characterInfo.Team,

        infoReceived: true
    }
}

const getCharacterAtLocation = (x: number, y: number, characters: Record<string, Character>): Character | undefined => {
    return Object.values(characters).find(character => character.x === x && character.y === y)
}

export { createCharacterInitial, isCharacter, updateCharacter, setPosition, constructCharacter, checkAttackable, getCharacterAtLocation, CHARACTER_INFO_PARSER }
export default Character;
