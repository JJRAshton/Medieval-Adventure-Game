import { Context } from "./context";
import React from "react";
import Canvas from "./gameCanvas";
import Character from "./character";
import { CharacterMinimumInfo } from "./character"
import Movement from "./movement";

import attackImageSrc from "./images/attackImage.png";
import GameUISelectionHandler from "./gameUISelection";

import { onCharacter } from "./gameSceneUtil";

import { TILE_WIDTH } from "./constants";
import Attack from "./attack";
import AttackOption from "./attackOption";

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
    
    private mouseX: number;
    private mouseY: number;
    
    private canvas: JSX.Element;

    constructor(socket: WebSocket, reactRoot: React.FC, mapWidth: number, mapHeight: number, playerID: number, characters: JSON) {
        super(socket, reactRoot, "game");
        this.mapWidth = mapWidth;
        this.mapHeight = mapHeight;
        this.playerID = playerID;
        this.selectionHandler = new GameUISelectionHandler(socket, playerID, this);
        console.log("Character type: ", typeof(characters));
        this.characters = this.parseCharacters(characters);
        this.character = this.getPlayerWithId(this.playerID);
        this.takingTurn = false; // Boolean value to record whether we're currently taking a turn
        this.mouseX, this.mouseY = 0, 0;
        this.canvas = <Canvas
            // Passing in the various call backs as props
            draw={(ctx) => {this.drawCanvas(ctx)}}
            resize={(canvas) => {this.resize(canvas)}}
            handleClick={(x, y) => this.handleClick(x, y)}
            handleMouseMove={(x, y) => this.handleMouseMove(x, y)}
            handleKeyPress={this.handleKeyPress}
            setStyle={this.setStyle}></Canvas>
    }

    parseCharacters(characters: any) {
        const characterMap = new Map();
        for (var i = 0; i < characters.length; i++) {
            const character = characters[i];
            this.socket.send(JSON.stringify({event: "playerInfoRequest", characterID: character[0]}))
            characterMap.set(character[0], new Character(character[0], character[1][0], character[1][1]))
        }
        return characterMap
    }

    render() {
        this.reactRoot.render(
        <div>
            <h2>
                <div className="message">{this.getCurrentMessage()}</div>
            </h2>
            <div className="game">
                { this.canvas }
                <div className="info">
                    <div className="infoComponent" style={{width: "100%"}}>{this.getHealthBar()}</div>
                    <div className="infoComponent">{this.character.renderStats()}</div>
                    <div className="attackList"><div>Attacks available</div>{this.character.renderAttacks(this.getMinDistToTarget(), this.getCurrentSelectionOrNull())}</div>
                    <div className="infoComponent">{this.getConfirmButton()}</div>
                    <div className="infoComponent">{this.getEndTurnButton()}</div>
                </div>

            </div>
        </div>);
    }

    // Used to display attack options. Has two modes, either returns min dist to any enemy (if
    // no target is selected), or min dist against the current attack target.
    getMinDistToTarget() {
        if (this.selectionHandler.selection instanceof Attack) {
            if (this.selectionHandler.selection.target !== null) {
                const target = this.selectionHandler.selection.target;
                return Math.max(Math.abs(this.character.x - target.x), Math.abs(this.character.y - target.y));
            }
        }
        let minDist = 100 // Big number
        this.characters.forEach(target => {
            if (this.checkAttackable(target)) {
                minDist = Math.min(minDist, Math.max(Math.abs(this.character.x - target.x), Math.abs(this.character.y - target.y)));
            }
        })
        return minDist;

    }

    /**
     * Used to display attack options. Returns either the currently selected attack option, or null
     * if there isn't one.
     */
    getCurrentSelectionOrNull(): AttackOption | null {
        if (this.selectionHandler.selection instanceof Attack) {
            if (this.selectionHandler.selection.attackType) {
                return this.selectionHandler.selection.attackType;
            }
        }
        return null;
    }

    getHealthBar() {
        return <div className="healthBar" style={{
                    position:"relative",
                    width: "100%",
                    backgroundColor: "red",
                    height: "1.2em",
                    border: "medium solid"}}>
            <div style={{
                width: Math.floor(100 * this.character.health/this.character.maxHealth)+"%",
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
                }}>{this.character.health}/{this.character.maxHealth}</div>
        </div>
    }

    getEndTurnButton() {
        return <div className="button"
            onClick={()=>this.socket.send(JSON.stringify({event: "endTurnRequest"}))}>End Turn</div>
    }

    getConfirmButton() {
        return <div className="button"
        onClick={() => this.selectionHandler.confirmAttack()}>Confirm</div>
    }

    getCurrentMessage() {
        if (this.takingTurn) {
            return "It's your turn"
        }
        return "It's someone else's turn"
    }

    handleKeyPress(event) {
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
    handleMouseMove(x, y) {
        this.mouseX = x;
        this.mouseY = y;
        this.selectionHandler.handleMouseMove(x, y, this.mapWidth, this.mapHeight);
    }

    setStyle() {
        return {cursor: "pointer"}
    }

    // Drawing to the canvas, passed in as a callback
    drawCanvas(ctx) {

        //ctx.clearRect(0, 0, this.mapWidth * TILE_WIDTH, this.mapHeight * TILE_WIDTH);
        ctx.fillStyle = 'rgb(109, 153, 87)';
        ctx.fillRect(0, 0, this.mapWidth * TILE_WIDTH, this.mapHeight * TILE_WIDTH);

        // Draw the move path if its not null
        if (this.selectionHandler.selection instanceof Movement) {
            this.selectionHandler.selection.draw(ctx, TILE_WIDTH);
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
                if (this.checkAttackable(character)) {
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
    handleClick(clickX, clickY) {
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
                        if (this.checkAttackable(player) && onCharacter(clickX, clickY, player)) {
                            this.selectionHandler.setAttackOptions({target: player})
                        }
                    }, this)
                }
            }
        }
    }

    // Resizes the canvas, for some reason this has to be passed as a callback
    resize(canvas) {
        canvas.width = TILE_WIDTH * this.mapWidth;
        canvas.height = TILE_WIDTH * this.mapHeight;
    }

    // Processing events from server
    handleEvent(contextHandler, event) {
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

    checkAttackable(character) {
        return (this.takingTurn
            &&!(character.team === this.character.team)
            && Math.max(Math.abs(this.character.x - character.x), Math.abs(this.character.y - character.y)) <= this.character.range);
        }

    updatePlayers(charactersInfo) {
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