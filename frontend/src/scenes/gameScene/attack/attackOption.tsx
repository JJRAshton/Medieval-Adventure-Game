import React from "react";
import Weapon from "./weapon";
import Attack from "./attack";
import Character, { checkAttackable } from "../parsing/character";

const NOT_AVAILABLE_COLOUR = "#dbbb7c";
const DEFAULT = "#d1941c";
const SELECTED_COLOUR = "#e0a530";

const NOT_AVAILABLE_COLOUR_FONT = "#777";
const AVAILABLE_COLOUR_FONT = "#000";

export default class AttackOption {
    public weapon: Weapon;
    public name: String;
    public range: number;

    constructor(weapon: Weapon, name: String) {
        this.weapon = weapon;
        this.name = name;
        this.range = this.weapon.range;
    }
}

type AttackOptionInterfaceEntryProps = {
    attackOption: AttackOption;
    attackSelected: boolean;
    onTurn: boolean;
    selection;
    setSelection;
    character: Character;
    characters: Record<string, Character>;
}

const AttackOptionInterfaceEntry = (props: AttackOptionInterfaceEntryProps) => {
    const { attackOption, attackSelected, onTurn, selection, setSelection, character, characters } = props;

    // Used to display attack options. Has two modes, either returns min dist to any enemy (if
    // no target is selected), or min dist against the current attack target.
    const getMinDistToTarget = () => {
        if (selection instanceof Attack) {
            if (selection.target !== null) {
                const target = selection.target;
                return Math.max(Math.abs(character.x - target.x), Math.abs(character.y - target.y));
            }
        }
        let minDist = 100 // Big number
        Object.entries(characters).forEach(([id, target]) => {
            if (checkAttackable(character, target) && onTurn) {
                minDist = Math.min(minDist, Math.max(Math.abs(character.x - target.x), Math.abs(character.y - target.y)));
            }
        })
        return minDist;
    }

    const getStyle = (available: boolean, selected: boolean) => {
        let background = NOT_AVAILABLE_COLOUR;
        let color = NOT_AVAILABLE_COLOUR_FONT;
    
        if (available) {
            background = DEFAULT;
            color = AVAILABLE_COLOUR_FONT
        }
        if (selected) {
            background = SELECTED_COLOUR;
            color = AVAILABLE_COLOUR_FONT;
        }
        return {
            display: "flex",
            margin: 0,
            justifyContent: "space-around",
            border: "2px solid",
            padding: "5px",
            cursor: "default",
            marginTop: "auto",
            marginBottom: "auto",
            background,
            color,
        }
    }

    const inRange = attackOption.range >= getMinDistToTarget();

    return <li
            style={getStyle(inRange, attackSelected)}
            key={attackOption.name + "_" + attackOption.weapon.name}
            onClick={() => {
                if (inRange && onTurn) {
                    if (selection instanceof Attack) {
                        setSelection(new Attack({target: selection.target, attackType: attackOption})); // TODO: fix this hack
                    }
                    else {
                        setSelection(new Attack({attackType: attackOption}));
                    }
                }
            }}><div style={{margin: "auto"}}>{attackOption.name}</div><div><img src={attackOption.weapon.imageSource} width={"32px"} height={"32px"}></img></div></li>
}

export { AttackOptionInterfaceEntry }