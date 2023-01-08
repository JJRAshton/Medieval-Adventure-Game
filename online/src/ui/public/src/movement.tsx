import { TILE_WIDTH } from "./constants";
import { GameUISelection } from "./gameUISelection";

export default class Movement implements GameUISelection {
    private moveStack: Array<Array<any>>;

    // Basically a stack that can also draw itself
    constructor(xStart: number, yStart: number) {
        // The moveStack
        this.moveStack = [];
        this.moveStack.push([xStart, yStart]);
    }

    draw(ctx) {
        // Draw on the path being plotted
        ctx.fillStyle = 'yellow';

        this.moveStack.forEach((tile) => {
            ctx.fillRect(tile[0] * TILE_WIDTH, tile[1] * TILE_WIDTH , TILE_WIDTH, TILE_WIDTH);
        })
    }

    check(mouseX: number, mouseY: number) {
        // See if something should be added to the move stack based on the new mouse position
        const x = Math.floor(mouseX / TILE_WIDTH);
        const y = Math.floor(mouseY / TILE_WIDTH);

        // No peek in javascript :(
        const currentLocation = this.moveStack[this.moveStack.length - 1];
        if (Math.abs(x - currentLocation[0]) <= 1 && Math.abs(y - currentLocation[1]) <= 1 ) {
            if (!this.contains(x, y)) { // .includes doesn't work, I think its checking each element
                if (Math.abs(mouseX - (x + 1 / 2) * TILE_WIDTH) + Math.abs(mouseY - (y + 1 / 2) * TILE_WIDTH) < TILE_WIDTH / 2) {
                    this.moveStack.push([x, y]);
                }
            }
        }
    }

    contains(x, y) {
        // Javascript was written deliberately to make this difficult
        for (let i = this.moveStack.length - 1; i > -1; i--) {
            var move = this.moveStack[i];
            if (move[0] === x && move[1] === y) {
                return true;
            }
        }
        return false;
    }

    getMoveRequest(playerID: number) {
        return {event: "moveRequest", playerID, route: this.moveStack};
    }
}