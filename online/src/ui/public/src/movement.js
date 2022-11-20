export default class Movement {

    // Basically a stack that can also draw itself
    constructor(xStart, yStart) {
        // The moveStack
        this.moveStack = [];
        this.moveStack.push([xStart, yStart]);
    }

    draw(ctx, tileWidth) {
        // Draw on the path being plotted
        ctx.fillStyle = 'yellow';

        this.moveStack.forEach((tile) => {
            ctx.fillRect(tile[0] * tileWidth, tile[1] * tileWidth , tileWidth, tileWidth);
        })
    }

    check(mouseX, mouseY, tileWidth) {
        // See if something should be added to the move stack based on the new mouse position
        const x = Math.floor(mouseX / tileWidth);
        const y = Math.floor(mouseY / tileWidth);

        // No peek in javascript :(
        const currentLocation = this.moveStack[this.moveStack.length - 1];
        if (Math.abs(x - currentLocation[0]) <= 1 && Math.abs(y - currentLocation[1]) <= 1 ) {
            if (!this.contains(x, y)) { // .includes doesn't work, I think its checking each element
                this.moveStack.push([x, y])
            }
        }

    }

    contains(x, y) {
        // Javascript was written deliberately to make this difficult
        console.log(this.moveStack);
        for (let i = this.moveStack.length - 1; i > -1; i--) {
            var move = this.moveStack[i];
            console.log(move);
            if (move[0] === x && move[1] === y) {
                return true;
            }
        }
        return false;
    }
}