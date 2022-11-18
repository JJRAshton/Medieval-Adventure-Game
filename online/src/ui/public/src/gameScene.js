import { Context } from "./context";
import React from "react";
import Canvas from "./gameCanvas";

const TILE_WIDTH = 64;

export class Game extends Context {

    constructor(socket, mapWidth, mapHeight, playerID, characters) {
        super(socket, "game");
        this.mapWidth = mapWidth;
        this.mapHeight = mapHeight;
        this.playerID = playerID;
        // Probably should do some parsing of the characters at this stage.
        this.characters = characters;
        this.canvas = <Canvas 
            draw={(ctx) => {this.drawCanvas(ctx)}}
            resize={(canvas) => {this.resize(canvas)}}
            handleClick={this.handleClick}></Canvas>
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
        this.canvas.getBoundingClientRect
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

    handleClick(x, y) {
        //console.log(event.pageX, event.pageY);
        console.log(x, y);
        //console.log(this.canvas.getBoundingClientRect());
    }

    resize(canvas) {
        canvas.width = TILE_WIDTH * this.mapWidth;
        canvas.height = TILE_WIDTH * this.mapHeight;
    }

    handleEvent(contextHandler, socket) {

    }
}