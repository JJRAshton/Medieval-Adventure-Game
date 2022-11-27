import { Context } from "./context";
import React from "react";
import Canvas from "./gameCanvas";
import Character from "./character";
import Movement from "./movement";

const TILE_WIDTH = 64;

export class Game extends Context {

    constructor(socket, mapWidth, mapHeight, playerID, characters) {
        super(socket, "game");
        this.mapWidth = mapWidth;
        this.mapHeight = mapHeight;
        this.playerID = playerID;
        this.characters = this.parseCharacters(characters);
        this.character = this.characters.get(this.playerID);
        this.takingTurn = false; // Boolean value to record whether we're currently making a move
        this.movement = null; // Boolean value to record whether we're a path is being traced out
        this.mouseX, this.mouseY = 0, 0;
        this.canvas = <Canvas
            // Passing in the various call backs as props
            draw={(ctx) => {this.drawCanvas(ctx)}}
            resize={(canvas) => {this.resize(canvas)}}
            handleClick={(x, y) => this.handleClick(x, y)}
            handleMouseMove={(x, y) => this.handleMouseMove(x, y)}
            handleKeyPress={this.handleKeyPress}></Canvas>
    }

    parseCharacters(characters) {
        const characterMap = new Map();
        for (var i = 0; i < characters.length; i++) {
            const character = characters[i];
            this.socket.send(JSON.stringify({event: "playerInfoRequest", characterID: character[0]}))
            characterMap.set(character[0], new Character(character[0], character[1][0], character[1][1]))
        }
        return characterMap
    }

    render(reactRoot) {
        reactRoot.render(
        <div>
            <h2>
                {this.getCurrentMessage()}
            </h2>
            <div style={{
                display: "inline-flex", 
                fontSize: "32"}}>
                { this.canvas }
                <div className="info">
                    <ul className="gameOptions" style={{"listStyle": "none"}}>
                        <li className="button"
                            style={{fontSize: 32}}
                            onClick={()=>this.socket.send(JSON.stringify({
                                event: "endTurnRequest"
                            }))}>End Turn</li>
                    </ul>
                    {this.character.renderAttacks()}
                    {this.character.renderStats()}
                </div>

            </div>
        </div>
        );
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
        if (!(this.movement == null)) {
            if (0 < this.mouseX && this.mouseX < this.mapWidth * TILE_WIDTH && 0 < this.mouseY && this.mouseY < this.mapHeight * TILE_WIDTH) {
                this.movement.check(x, y, TILE_WIDTH);
            }
        }
    }

    // Drawing to the canvas, passed in as a callback
    drawCanvas(ctx) {

        //ctx.clearRect(0, 0, this.mapWidth * TILE_WIDTH, this.mapHeight * TILE_WIDTH);
        ctx.fillStyle = 'rgb(109, 153, 87)';
        ctx.fillRect(0, 0, this.mapWidth * TILE_WIDTH, this.mapHeight * TILE_WIDTH);

        // Draw the move path if its not null
        if (!(this.movement == null)) {
            this.movement.draw(ctx, TILE_WIDTH);
        }

        // Draw the grid
        for (var i = 0; i < this.mapWidth; i++) {
            for (var j = 0; j < this.mapWidth; j++) {
                ctx.strokeRect(i * TILE_WIDTH, j * TILE_WIDTH, TILE_WIDTH, TILE_WIDTH);
            }
        }

        // Draw the characters
        this.characters.forEach((character) => {
            if (character.id === this.playerID) {
                ctx.fillStyle = 'blue';
            }
            else if (character.team == this.character.team) {
                ctx.fillStyle = 'green';
            }
            else {
                ctx.fillStyle = 'red';
            }
            ctx.fillRect((character.x * TILE_WIDTH) + 3, (character.y * TILE_WIDTH) + 3, TILE_WIDTH - 6, TILE_WIDTH - 6);
            ctx.fillStyle = 'black'
            ctx.fillRect((character.x * TILE_WIDTH) + 13, (character.y * TILE_WIDTH) + 13, 8, 8);
            ctx.fillRect(((character.x + 1) * TILE_WIDTH) - 13 - 8, (character.y * TILE_WIDTH) + 13, 8, 8);

            ctx.fillRect((character.x * TILE_WIDTH) + 13, ((character.y + 1) * TILE_WIDTH) - 20, TILE_WIDTH - 6 - 10 - 6, 6);


        })

        // Draw outer boundary
        ctx.strokeRect(1, 1, this.mapWidth * TILE_WIDTH - 2, this.mapHeight * TILE_WIDTH - 2);
        ctx.beginPath();
    
        ctx.fill()
    }

    // Handling click events, passed in as a callback
    handleClick(clickX, clickY) {
        if (!(this.movement == null)) {
            this.socket.send(JSON.stringify(this.movement.getMoveRequest(this.playerID)));
            this.movement = null;
        }
        else {
            if (this.takingTurn) {
                const player = this.characters.get(this.playerID);
                if (player.x * TILE_WIDTH < clickX && clickX < (player.x + 1) * TILE_WIDTH
                        && player.y * TILE_WIDTH < clickY && clickY < (player.y + 1) * TILE_WIDTH) {
                    this.movement = new Movement(player.x, player.y);
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
                this.takingTurn = (event.onTurnID == this.playerID);
                if (!this.takingTurn) {
                    // Reset the planned movement if we're told it's not our turn
                    this.movement = null;
                }
                break;
            case "mapUpdate":
                // These get sent when someone moves, or when something changes
                event.characters.forEach(character => {
                    console.log(character);
                    this.characters.get(character[0]).setPosition(character[1][0], character[1][1]);
                })
                break;
            case "playerInfo":
                this.characters.get(event.characterID).construct(event.playerInfo);
                break;
            default:
                console.log("Unrecognised event" + event)
        }
    }
}