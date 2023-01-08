import React from "react";

const NOT_AVAILABLE_COLOUR = "#dbbb7c";
const DEFAULT = "#d1941c";
const SELECTED_COLOUR = "#e0a530";

const NOT_AVAILABLE_COLOUR_FONT = "#777";
const AVAILABLE_COLOUR_FONT = "#000";

export default class AttackOption {

    constructor(weapon, name, selectionHandler) {
        this.weapon = weapon;
        this.name = name;
        this.range = this.weapon.range;
        this.selectionHandler = selectionHandler;
    }

    selectAttackOption(inRange) {
        if (inRange) {
            this.selectionHandler.setAttackOptions({attackType: this})
        }
    }

    getStyle(available, selected) {
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
            padding: 0,
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

    renderAttackOptionElement(inRange, selected) {
        return <li
            style={this.getStyle(inRange, selected)}
            key={this.name+"_"+this.weapon.name}
            onClick={() => {this.selectAttackOption(inRange)}}><div style={{margin: "auto"}}>{this.name}</div><div><img src={this.weapon.imageSource} width={"32px"} height={"32px"}></img></div></li>
    }
}