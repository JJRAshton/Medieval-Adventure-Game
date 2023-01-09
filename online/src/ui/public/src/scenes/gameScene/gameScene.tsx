import Context from "../context";
import React from "react";
import Canvas from "./rendering/gameCanvas";
import Character from "./parsing/character";
import Movement from "./rendering/movement";

import attackImageSrc from "../../images/attackImage.png";
import GameUISelectionHandler from "./gameUISelection";

import { onCharacter } from "./gameSceneUtil";

import { TILE_WIDTH } from "./constants";
import Attack from "./attack/attack";
import ContextHandler from "../contextHandler";
import GameState from "./gameState";
import InfoPanel from "./rendering/infoPanel";

const ATTACK_IMAGE = new Image();
ATTACK_IMAGE.src = attackImageSrc;

export class Game extends Context {
    private mapWidth: number;
    private mapHeight: number;
    private playerID: number;
    private selectionHandler: GameUISelectionHandler;
    private characters: Map<number, Character>;
    private character: Character;
    private takingTurn: boolean;
    private _state: GameState;
    private _infoPanel: InfoPanel;
    
    private mouseX: number;
    private mouseY: number;
    
    private canvas: JSX.Element;

    constructor(socket: WebSocket, reactRoot: React.FC, mapWidth: number, mapHeight: number, playerID: number, characters: JSON) {
        super(socket, reactRoot, "game");
        this.mapWidth = mapWidth;
        this.mapHeight = mapHeight;
        this.playerID = playerID;
        this.selectionHandler = new GameUISelectionHandler(socket, playerID, this);
        this.characters = this._parseCharacters(characters);
        this.character = this.getPlayerWithId(this.playerID);
        this._state = new GameState(this.character, this.characters);
        this._infoPanel = new InfoPanel(this.selectionHandler, socket, this._state);
        this.takingTurn = false; // Boolean value to record whether we're currently taking a turn
        this.mouseX, this.mouseY = 0, 0;
        this.canvas = <Canvas
            // Passing in the various call backs as props
            draw={(ctx: CanvasRenderingContext2D) => {this.drawCanvas(ctx)}}
            resize={(canvas: HTMLCanvasElement) => {this.resize(canvas)}}
            handleClick={(x: number, y: number) => this.handleClick(x, y)}
            handleMouseMove={(x: number, y: number) => this.handleMouseMove(x, y)}
            handleKeyPress={this.handleKeyPress}
            setStyle={this.setStyle}></Canvas>
    }

    private _parseCharacters(characters: any): Map<number, Character> {
        const characterMap = new Map();
        for (var i = 0; i < characters.length; i++) {
            const character = characters[i];
            this.socket.send(JSON.stringify({event: "playerInfoRequest", characterID: character[0]}))
            characterMap.set(character[0], new Character(character[0], character[1][0], character[1][1]))
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
                { this.canvas }
                { this._infoPanel.render() }

            </div>
        </div>);
    }

    getCurrentMessage(): string {
        if (this.takingTurn) {
            return "It's your turn"
        }
        return "It's someone else's turn"
    }

    handleKeyPress(event: { keyCode: number; }): void {
        switch (event.keyCode) {
            // Handling wasd and arrow keys, probably wont be used now
            case 38:
            case 87:
                // Up
                console.log("up");
                break;
            case 40:
            case 83:
                // Down
                console.log("down");
                break;
            case 37:
            case 65:
                // Left
                console.log("left");
                break;
            case 39:
            case 68:
                // Right
                console.log("right");
                break;
            default:
                break;
        }
    }

    // Handling mouse movements inside the canvas
    handleMouseMove(x: number, y: number): void {
        this.mouseX = x;
        this.mouseY = y;
        this.selectionHandler.handleMouseMove(x, y, this.mapWidth, this.mapHeight);
    }

    setStyle(): any {
        return {cursor: "pointer"}
    }

    // Drawing to the canvas, passed in as a callback
    drawCanvas(ctx: CanvasRenderingContext2D): void {

        //ctx.clearRect(0, 0, this.mapWidth * TILE_WIDTH, this.mapHeight * TILE_WIDTH);
        ctx.fillStyle = 'rgb(109, 153, 87)';
        ctx.fillRect(0, 0, this.mapWidth * TILE_WIDTH, this.mapHeight * TILE_WIDTH);

        // Draw the move path if its not null
        if (this.selectionHandler.selection instanceof Movement) {
            this.selectionHandler.selection.draw(ctx);
        }

        // Draw the grid
        for (var i = 0; i < this.mapWidth; i++) {
            for (var j = 0; j < this.mapWidth; j++) {
                ctx.strokeRect(i * TILE_WIDTH, j * TILE_WIDTH, TILE_WIDTH, TILE_WIDTH);
            }
        }

        // Draw the characters
        this.characters.forEach((character) => {
            if (character.imageLoaded) {
                ctx.drawImage(character.image, character.x * TILE_WIDTH, character.y * TILE_WIDTH, TILE_WIDTH, TILE_WIDTH);
                if (this.takingTurn && this._state.character.checkAttackable(character)) {
                    if (this.selectionHandler.selection instanceof Attack 
                            && this.selectionHandler.selection.target
                            && this.selectionHandler.selection.target.id === character.id) {
                        ctx.drawImage(ATTACK_IMAGE, character.x * TILE_WIDTH + 2, character.y * TILE_WIDTH + 2, TILE_WIDTH - 4, TILE_WIDTH - 4);
                    }
                    else {
                        ctx.drawImage(ATTACK_IMAGE, character.x * TILE_WIDTH, character.y * TILE_WIDTH, TILE_WIDTH / 2, TILE_WIDTH / 2);
                    }
                }
            }
        }, this);

        // Draw outer boundary
        ctx.strokeRect(1, 1, this.mapWidth * TILE_WIDTH - 2, this.mapHeight * TILE_WIDTH - 2);
        ctx.beginPath();
    
        ctx.fill()
    }

    // Handling click events in the canvas, passed in as a callback
    handleClick(clickX: number, clickY: number): void {
        // Handling movement
        if (this.selectionHandler.selection instanceof Movement) {
            this.socket.send(JSON.stringify(this.selectionHandler.selection.getMoveRequest(this.playerID)));
            this.selectionHandler.reset();
        }
        else {
            if (this.takingTurn) {
                if (onCharacter(clickX, clickY, this.character)) {
                    this.selectionHandler.setMovement(new Movement(this.character.x, this.character.y));
                }
                else {
                    this.characters.forEach(player => {
                        // Inefficient way of finding players, they should probably be stored in 2d array
                        if (this._state.character.checkAttackable(player) && onCharacter(clickX, clickY, player)) {
                            this.selectionHandler.setAttackOptions({target: player})
                        }
                    }, this)
                }
            }
        }
    }

    // Resizes the canvas, for some reason this has to be passed as a callback
    resize(canvas: HTMLCanvasElement) {
        canvas.width = TILE_WIDTH * this.mapWidth;
        canvas.height = TILE_WIDTH * this.mapHeight;
    }

    // Processing events from server
    override handleEvent(contextHandler: ContextHandler, event: any): void {
        console.log(event);
        switch (event.responseType) {
            case "turnNotification":
                // These will get sent when the turn changes
                this.selectionHandler.reset();
                this.takingTurn = event.onTurnID == this.playerID;
                this.selectionHandler.onTurn = this.takingTurn;
                this.updatePlayers(event.charactersUpdate);
                break;
            case "mapUpdate":
                // These get sent when someone moves, or when something changes
                event.characters.forEach(character => {
                    this.getPlayerWithId(character[0]).setPosition(character[1][0], character[1][1]);
                })
                break;
            case "playerInfo":
                this.getPlayerWithId(event.characterID).construct(event.playerInfo, event.characterID === this.character.id, this.selectionHandler);
                break;
            default:
                console.log("Unrecognised event" + event)
        }
    }

    private updatePlayers(charactersInfo: any): void {
        for (let id in charactersInfo) {
            this.getPlayerWithId(parseInt(id)).update(charactersInfo[id]);
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