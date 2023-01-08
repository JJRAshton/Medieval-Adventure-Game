import Attack, { AttackOptions } from "./attack";
import { Context } from "./context";
import Movement from "./movement";

import { TILE_WIDTH } from "./constants";

export interface GameUISelection {

}

export default class GameUISelectionHandler {
    private _socket: any;
    private context: any;
    private playerID: any;

    public onTurn: boolean;
    public selection: GameUISelection | null;

    /**
     * This is a really overengineered way of a user making a single selection at a time
     */
    constructor(socket: WebSocket, playerID: number, context: Context) {
        this._socket = socket;
        this.onTurn = false;
        this.context = context;
        this.playerID = playerID;
        this.selection = null; // Null when no selection has been made
    }

    reset(): void {
        this.selection = null;
        this.context.render();
    }

    setMovement(movement: Movement): void {
        if (this.onTurn) {
            this.selection = movement;
        }
    }

    setAttackOptions(options: AttackOptions): void {
        if (!(this.selection instanceof Attack)) {
            return;
        }
        if (this.onTurn) {
            if (this.selection instanceof Attack) {
                this.selection.setOptions(options)
            }
            else {
                this.selection = new Attack(options);
            }
            this.context.render();
        }
    }

    handleMouseMove(mouseX: number, mouseY: number, mapWidth: number, mapHeight: number): void {
        if (this.selection instanceof Movement) {
            if (0 < mouseX && mouseX < mapWidth * TILE_WIDTH && 0 < mouseY && mouseY < mapHeight * TILE_WIDTH) {
                this.selection.check(mouseX, mouseY);
            }
        }
        if (this.selection instanceof Attack) {
            // Do nothing for mouse moves if were doing an attack for now
        }
        this.context.render();
    }

    confirmAttack(): void {
        if (!(this.selection instanceof Attack)) {
            return;
        }
        if (this.selection instanceof Attack && this.selection.confirmAttack()) {
            if (this.selection.target === null) {
                // This should not be null as confirmAttack returned true
                throw new Error("Attack.confirmAttack() is broken")
            }
            this._socket.send(JSON.stringify({
                event: "attackRequest",
                playerID: this.playerID,
                enemyID: this.selection.target.id}));
            this.selection = null;
        }
    }
}
