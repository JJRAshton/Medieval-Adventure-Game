import { Context } from "./context";
import React from "react";

const TILE_WIDTH = 32;

export class Game extends Context {

    constructor(socket, mapWidth, mapHeight, playerID, characters) {
        super(socket, "game");
        console.log(mapWidth, mapHeight, playerID, characters);
        this.mapWidth = mapWidth;
        this.mapHeight = mapHeight;
        this.playerID = playerID;
        // Probably should do some parsing of the characters at this stage.
        this.characters = characters;
        this.canvas = <canvas id="gameCanvas" width={mapWidth * TILE_WIDTH} height={mapHeight * TILE_WIDTH}></canvas>
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

    handleEvent(contextHandler, socket) {

    }
}