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
        // Probably should do some parsing of the characters at this stage.
        this.characters = this.parseCharacters(characters);
        this.currentMessage = "Currently in a game with " + characters.length + " players";
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
            characterMap.set(character[0], new Character(character[0], character[1][0], character[1][1]))
        }
        return characterMap
    }

    render(reactRoot) {
        reactRoot.render(
        <div>
            <h2>
                {this.currentMessage}
            </h2>
            <div style={{
                display: "inline-flex", 
                fontSize: "32"}}>
                { this.canvas }
                <ul className="gameOptions" style={{"listStyle": "none"}}>
                    <li className="button" style={{fontSize: 32}}>Attack</li>
                    <li className="button" style={{fontSize: 32}}>Move</li>
                </ul>
            </div>
        </div>
        );
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

        ctx.clearRect(0, 0, this.mapWidth * TILE_WIDTH, this.mapHeight * TILE_WIDTH);

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
                if (!(this.movement == null)) {
                    ctx.fillRect(this.mouseX - TILE_WIDTH / 2, this.mouseY - TILE_WIDTH / 2, TILE_WIDTH - 6, TILE_WIDTH - 6);
                }
                else {
                    ctx.fillRect((character.x * TILE_WIDTH) + 3, character.y * TILE_WIDTH + 3, TILE_WIDTH - 6, TILE_WIDTH - 6);
                }
            }
            else {
                ctx.fillStyle = 'green';
                ctx.fillRect((character.x * TILE_WIDTH) + 3, (character.y * TILE_WIDTH) + 3, TILE_WIDTH - 6, TILE_WIDTH - 6);
            }
        })

        // Draw outer boundary
        ctx.strokeRect(1, 1, this.mapWidth * TILE_WIDTH - 2, this.mapHeight * TILE_WIDTH - 2);
        ctx.beginPath();
    
        // ctx.fillRect((this.playerX * TILE_WIDTH) + 3, (this.playerY * TILE_WIDTH) + 3, TILE_WIDTH - 6, TILE_WIDTH - 6)
        ctx.fill()
    }

    // Handling click events, passed in as a callback
    handleClick(clickX, clickY) {
        if (!(this.movement == null)) {
            this.socket.send(JSON.stringify(this.movement.getMoveRequest(this.playerID)));
            this.movement = null;
        }
        else {
            const player = this.characters.get(this.playerID);
            if (player.x * TILE_WIDTH < clickX && clickX < (player.x + 1) * TILE_WIDTH
                    && player.y * TILE_WIDTH < clickY && clickY < (player.y + 1) * TILE_WIDTH) {
                this.movement = new Movement(player.x, player.y);
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
                // These will probably get sent when our turn starts or ends
                this.takingTurn = event.onTurn;
                if (!this.takingTurn) {
                    // Reset the planned movement if we're told it's not our turn
                    this.movement = null;
                }
                break;
            case "mapUpdate":
                event.characters.forEach(character => {
                    console.log(character);
                    this.characters.get(character[0]).setPosition(character[1][0], character[1][1]);
                })
                break;
            default:
        }
    }
}