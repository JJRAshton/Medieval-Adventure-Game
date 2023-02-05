import React from "react";
import Attack from "../attack/attack";
import AttackOption from "../attack/attackOption";
import GameState from "../gameState";
import GameUISelectionHandler from "../gameUISelection";
import AttackOptionInterface from "./availableAttacks";
import { HealthBar } from "./healthBar";
import Renderable from "./renderable";
import SelectionInfo from "./selectionInfo";
import StatInfo from "./statInfo";

export default class InfoPanel {

    private _selectionHandler: GameUISelectionHandler;
    private _socket: WebSocket;
    private _gameState: GameState;
    private _healthBar: HealthBar;
    private _statsInterface: StatInfo;
    private _attacksInterface: AttackOptionInterface;
    private _selectionInfo: SelectionInfo;

    constructor(selectionHandler: GameUISelectionHandler, socket: WebSocket, gameState: GameState) {
        this._selectionHandler = selectionHandler;
        this._socket = socket;
        this._gameState = gameState;

        this._healthBar = new HealthBar(this._gameState.character);
        this._attacksInterface = new AttackOptionInterface(this._gameState.character);
        this._statsInterface = new StatInfo(this._gameState.character);
        this._selectionInfo = new SelectionInfo(selectionHandler);
    }

    public render(): JSX.Element {
        return <div className="info">
            <div className="infoComponent" style={{width: "100%"}}>{this._healthBar.render()}</div>
            <div className="infoComponent">{this._statsInterface.render()}</div>
            <div className="attackList"><div>Attacks available</div>{this._attacksInterface.render(this._getMinDistToTarget(), this._getCurrentSelectionOrNull())}</div>
            <div className="infoCompenet">{this._selectionInfo.render()}</div>
            <div className="infoComponent">{this._getConfirmButton()}</div>
            <div className="infoComponent">{this._getEndTurnButton()}</div>
        </div>
    }

    // Used to display attack options. Has two modes, either returns min dist to any enemy (if
    // no target is selected), or min dist against the current attack target.
    private _getMinDistToTarget(): number {
        if (this._selectionHandler.selection instanceof Attack) {
            if (this._selectionHandler.selection.target !== null) {
                const target = this._selectionHandler.selection.target;
                return Math.max(Math.abs(this._gameState.character.x - target.x), Math.abs(this._gameState.character.y - target.y));
            }
        }
        let minDist = 100 // Big number
        this._gameState.characters.forEach(target => {
            if (this._gameState.character.checkAttackable(target) && this._selectionHandler.onTurn) {
                minDist = Math.min(minDist, Math.max(Math.abs(this._gameState.character.x - target.x), Math.abs(this._gameState.character.y - target.y)));
            }
        })
        return minDist;

    }

    /**
     * Used to display attack options. Returns either the currently selected attack option, or null
     * if there isn't one.
     */
    private _getCurrentSelectionOrNull(): AttackOption | null {
        if (this._selectionHandler.selection instanceof Attack) {
            if (this._selectionHandler.selection.attackType) {
                return this._selectionHandler.selection.attackType;
            }
        }
        return null;
    }

    private _getEndTurnButton(): JSX.Element {
        return <div className="button"
            onClick={()=>this._socket.send(JSON.stringify({event: "endTurnRequest"}))}>End Turn</div>
    }

    private _getConfirmButton(): JSX.Element {
        return <div className="button"
        onClick={() => this._selectionHandler.confirmAttack()}>Confirm</div>
    }
}