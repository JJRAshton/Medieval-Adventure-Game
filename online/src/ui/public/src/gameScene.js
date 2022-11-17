import { Context } from "./context";
import React from "react";
import Canvas from "./gameCanvas";

const TILE_WIDTH = 64;

export class Game extends Context {

    constructor(socket, mapWidth, mapHeight, playerID, characters) {
        super(socket, "game");
        console.log(mapWidth, mapHeight, playerID, characters);
        this.mapWidth = mapWidth;
        this.mapHeight = mapHeight;
        this.playerID = playerID;
        // Probably should do some parsing of the characters at this stage.
        this.characters = characters;
        this.canvas = <Canvas 
            draw={(ctx) => {this.drawCanvas(ctx)}}
            resize={(canvas) => {this.resize(canvas)}}></Canvas>
        // this.canvas = <canvas ref="canvas" width={mapWidth * TILE_WIDTH} height={mapHeight * TILE_WIDTH}></canvas>
    }

    render(reactRoot) {
        reactRoot.render(
        <div>
            <h2>
                Now in a game!
            </h2>
            { this.canvas }
        </div>
        );
    }

    drawCanvas(ctx) {
        for (var i = 0; i < this.mapWidth; i++) {
            for (var j = 0; j < this.mapWidth; j++) {
                ctx.strokeRect(i * TILE_WIDTH, j * TILE_WIDTH, TILE_WIDTH, TILE_WIDTH);
            }
        }
        ctx.strokeRect(1, 1, this.mapWidth * TILE_WIDTH - 2, this.mapHeight * TILE_WIDTH - 2);
        ctx.beginPath();
    
        ctx.fillStyle = 'red';
        ctx.fill()
    }

    resize(canvas) {
        canvas.width = TILE_WIDTH * this.mapWidth;
        canvas.height = TILE_WIDTH * this.mapHeight;
    }

    handleEvent(contextHandler, socket) {

    }
}