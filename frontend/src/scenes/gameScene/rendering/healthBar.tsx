import React from "react";

import Character from "../parsing/character";
import Renderable from "./renderable";


export class HealthBar implements Renderable {
    _character: Character;

    constructor(character: Character) {
        this._character = character;
    }

    public render(): JSX.Element {
        return <div className="healthBar" style={{
            position: "relative",
            width: "100%",
            backgroundColor: "red",
            height: "1.2em",
            border: "medium solid"}}>
            <div style={{
                width: Math.floor(100 * this._character.health/this._character.maxHealth)+"%",
                height: "100%",
                background: "green",
                borderRadius: "0px",
                }}/>
            <div style={{
                position: "absolute",
                top: "50%",
                left: "50%",
                transform: "translate(-50%, -50%)",
                fontSize: "1em",
                borderRadius: "0px",
                }}>{this._character.health}/{this._character.maxHealth}</div>
        </div>
    }

    
}