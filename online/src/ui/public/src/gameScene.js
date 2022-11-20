import { Context } from "./context";
import React from "react";
import Canvas from "./gameCanvas";
import Character from "./character";

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
        this.moving = false; // Boolean value to record whether we're a path is being traced out
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
        const characterSet = new Set();
        for (var i = 0; i < characters.length; i++) {
            const character = characters[i];
            console.log(character[1, 1])
            characterSet.add(new Character(character[0], character[1][0], character[1][1]))
        }
        return characterSet
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
    }

    // Drawing to the canvas, passed in as a callback
    drawCanvas(ctx) {
        // Draw the grid
        ctx.clearRect(0, 0, this.mapWidth * TILE_WIDTH, this.mapHeight * TILE_WIDTH);
        for (var i = 0; i < this.mapWidth; i++) {
            for (var j = 0; j < this.mapWidth; j++) {
                ctx.strokeRect(i * TILE_WIDTH, j * TILE_WIDTH, TILE_WIDTH, TILE_WIDTH);
            }
        }

        // Draw the characters
        this.characters.forEach((character) => {
            if (character.id === this.playerID) {
                ctx.fillStyle = 'blue';
                if (this.moving) {
                    ctx.fillRect(this.mouseX - TILE_WIDTH / 2, this.mouseY - TILE_WIDTH / 2, TILE_WIDTH - 6, TILE_WIDTH - 6);
                }
                else {
                    ctx.fillRect((character.x * TILE_WIDTH) + 3, (character.y * TILE_WIDTH) + 3, TILE_WIDTH - 6, TILE_WIDTH - 6);
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
        console.log(clickX, clickY);
        if (this.moving) {
            this.moving = false;
        }
        else {
            const [playerX, playerY] = this.getPlayerLocation();
            if (playerX * TILE_WIDTH < clickX && clickX < (playerX + 1) * TILE_WIDTH
                    && playerY * TILE_WIDTH < clickY && clickY < (playerY + 1) * TILE_WIDTH) {
                console.log("clicking player");
                this.moving = true;
            }
        }
    }

    getPlayerLocation() {
        for (const character of this.characters) {
            if (this.playerID === character.id) {
                console.log("playerX: " + character.x + " playerY: " + character.y);
                return [character.x, character.y];
            }
        }
        console.log("WARNING! could not find player with id.")
    }

    // Resizes the canvas, for some reason this has to be passed as a callback
    resize(canvas) {
        canvas.width = TILE_WIDTH * this.mapWidth;
        canvas.height = TILE_WIDTH * this.mapHeight;
    }

    // Processing events from server
    handleEvent(contextHandler, event) {
        switch (event.type) {
            case turnNotification:
                // These will probably get sent when our turn starts or ends
                this.takingTurn = event.onTurn;
                break;
            default:
        }
    }
}