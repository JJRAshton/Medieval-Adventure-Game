import Attack from "./attack";
import Movement from "./movement";

export interface GameUISelection {

}

export default class GameUISelectionHandler {
    private _socket: any;
    private onTurn: boolean;
    private context: any;
    private playerID: any;
    private current: string;
    private selection: GameUISelection | null;

    /**
     * This is a really overengineered way of a user making a single selection at a time
     * TODO: Make the movement part of this as well
     */
    constructor(socket, playerID, context) {
        this._socket = socket;
        this.onTurn = false;
        this.context = context;
        this.playerID = playerID;
        this.current = "None"; // This string thing is kind of ugly, but I can't think of a better way
        this.selection = null; // Null when no selection has been made
    }

    reset() {
        this.current = "None";
        this.selection = null;
        this.context.render();
    }

    setMovement(movement: Movement) {
        if (this.onTurn) {
            this.current = "Movement";
            this.selection = movement;
        }
    }

    setAttackOptions(options) {
        if (this.onTurn) {
            if (this.current == "Attack") {
                this.selection.setOptions(options)
            }
            else {
                this.current = "Attack";
                this.selection = new Attack(options);
            }
            this.context.render();
        }
    }

    handleMouseMove(mouseX, mouseY, tileWidth, mapWidth, mapHeight) {
        if (this.current === "Movement") {
            if (0 < mouseX && mouseX < mapWidth * tileWidth && 0 < mouseY && mouseY < mapHeight * tileWidth) {
                this.selection.check(mouseX, mouseY, tileWidth);
            }
        }
        if (this.current === "Attack") {
            // Do nothing for mouse moves if were doing an attack for now
        }
        this.context.render();
    }

    confirmAttack() {
        if (this.current === "Attack" && this.selection.confirmAttack()) {
            this._socket.send(JSON.stringify({
                event: "attackRequest",
                playerID: this.playerID,
                enemyID: this.selection.target.id}));
            this.current = "None";
            this.selection = null;
        }
    }
}
