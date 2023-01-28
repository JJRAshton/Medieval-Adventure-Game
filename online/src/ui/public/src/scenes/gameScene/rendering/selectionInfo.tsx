import React from "react";
import GameUISelectionHandler from "../gameUISelection";
import Character from "../parsing/character";
import { HealthBar } from "./healthBar";
import Renderable from "./renderable";

export default class SelectionInfo implements Renderable {
    private _selectionHandler: GameUISelectionHandler;

    constructor(selctionHandler: GameUISelectionHandler) {
        this._selectionHandler = selctionHandler;
    }

    render(): JSX.Element {
        let player: Character | null = this._selectionHandler.getInformationPanelSelection();
        if (player === null) {
            // Only render if a selection has been made for now
            return <div>No player selected</div>
        }
        
        return (
        <div style={{border: "solid", padding: "10px", marginBottom: "10px"}}>
            <div className="stats">
                <table className="statTable">
                    <tbody>
                        <tr>
                            <td>Name</td>
                            <td>a name</td>
                        </tr>
                        <tr>
                            <td>Side</td>
                            <td>{(player.team === 1) ? "Friendly " : "Enemy"}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
            <div className="stats">
                { new HealthBar(player).render() }
            </div>
        </div>)
    }
}