import React from "react";
import AttackOption from "../attack/attackOption";
import Character from "../parsing/character";

/**
 * Not a true renderable as it requires (indirect) knowledge of game state
 */
export default class AttackOptionInterface {

    private _player: Character;

    constructor(player: Character) {
        this._player = player;
    }

    public render(minDistToTarget: number, currentSelectionOrNull: AttackOption | null) {
        if (this._player.infoReceived) {
            let children: Array<JSX.Element> = [];
            this._player.attacks.forEach((attack) => {
                children.push(attack.renderAttackOptionElement(attack.range >= minDistToTarget, attack === currentSelectionOrNull))
            });
            return <ul className="attack"
                style={{
                    listStyleType: "none",
                    padding: 0,
                    margin: 0,
                }}>{children}</ul>
        }
        else {
            return <div className="attack stats">Could not load attacks</div>
        }
    }
}