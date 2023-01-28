import Context from "../context";
import React from "react";
import Canvas from "./rendering/gameCanvas";
import Character from "./parsing/character";

import GameUISelectionHandler from "./gameUISelection";

import ContextHandler from "../contextHandler";
import GameState from "./gameState";
import InfoPanel from "./rendering/infoPanel";

export class Game extends Context {

    private selectionHandler: GameUISelectionHandler;
    private characters: Map<number, Character>;
    private _state: GameState;
    
    private _infoPanel: InfoPanel;
    private _canvas: Canvas;

    constructor(socket: WebSocket, reactRoot: React.FC, mapWidth: number, mapHeight: number, playerID: number, characters: JSON) {
        super(socket, reactRoot, "game");
        this.selectionHandler = new GameUISelectionHandler(socket, playerID, this);
        this.characters = this._parseCharacters(characters);
        this._state = new GameState(this.getPlayerWithId(playerID), this.characters, mapWidth, mapHeight);
        this._infoPanel = new InfoPanel(this.selectionHandler, socket, this._state);
        this._canvas = new Canvas(this.selectionHandler, socket, this._state);
    }

    private _parseCharacters(characters: any): Map<number, Character> {
        const characterMap = new Map();
        for (var i = 0; i < characters.length; i++) {
            const character = characters[i];
            this.socket.send(JSON.stringify({event: "playerInfoRequest", characterID: character[0]}))
            const chr = new Character(character[0], character[1][0], character[1][1]);
            characterMap.set(character[0], chr)
        }
        return characterMap
    }

    render(): void {
        this.reactRoot.render(
        <div>
            <h2>
                <div className="message">{this.getCurrentMessage()}</div>
            </h2>
            <div className="game">
                { this._canvas.render() }
                { this._infoPanel.render() }
            </div>
        </div>);
    }

    getCurrentMessage(): string {
        if (this.selectionHandler.onTurn) {
            return "It's your turn"
        }
        return "It's someone else's turn"
    }

    // Processing events from server
    override handleEvent(contextHandler: ContextHandler, event: any): void {
        console.log(event);
        switch (event.responseType) {
            case "turnNotification":
                // These will get sent when the turn changes
                this.selectionHandler.reset();
                
                this.selectionHandler.onTurn = event.onTurnID === this._state.character.id;
                this.updatePlayers(event.charactersUpdate);
                break;
            case "mapUpdate":
                // These get sent when someone moves, or when something changes
                this._state.mapState.resetMap();
                event.characters.forEach((characterInfo: [number, [number, number]]) => {
                    const chr = this.getPlayerWithId(characterInfo[0]);
                    chr.setPosition(characterInfo[1][0], characterInfo[1][1]);
                    this._state.mapState.set(chr.x, chr.y, chr);
                }, this)
                break;
            case "playerInfo":
                this.getPlayerWithId(event.characterID).construct(event.playerInfo, event.characterID === this._state.character.id, this.selectionHandler);
                break;
            default:
                console.log("Unrecognised event" + event)
        }
    }

    private updatePlayers(charactersInfo: any): void {
        console.log(charactersInfo);
        this._state.mapState.resetMap();
        for (let id in charactersInfo) {
            const chr = this.getPlayerWithId(parseInt(id));
            chr.update(charactersInfo[id]);
            this._state.mapState.set(chr.x, chr.y, chr);
        }
    }

    /**
     * Throws an error if the id is not recognised
     * @param id of the player
     * @returns the player
     */
    private getPlayerWithId(id: number): Character {
        const character = this.characters.get(id);
        if (!character) {
            throw new Error("Critical error: Did not recognise character with ID: " + id + ".");
        }
        return character;
    }
}