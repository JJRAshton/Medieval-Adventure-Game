import Attack, { AttackOptions } from "./attack/attack";
import Movement from "./rendering/movement";

import { TILE_WIDTH } from "./constants";
import Character from "./parsing/character";

export interface GameUISelection {

}

export default class GameUISelectionHandler {
    private _socket: any;
    private _playerID: string;

    public selection: GameUISelection | null;
    public mouseX: number;
    public mouseY: number;

    /**
     * This is a really overengineered way of a user making a single selection at a time
     */
    constructor(socket: WebSocket, playerID: string) {
        this._socket = socket;
        this._playerID = playerID;
        this.selection = null; // Null when no selection has been made
    }

    reset(): void {
        this.selection = null;
    }

    setMovement(movement: Movement): void {
        this.selection = movement;
    }

    setAttackOptions(options: AttackOptions): void {
        if (this.selection instanceof Attack) {
            this.selection.setOptions(options)
        }
        else {
            this.selection = new Attack(options);
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
                playerID: this._playerID,
                enemyID: this.selection.target.id}));
            this.selection = null;
        }
    }
}
