import Attack, { AttackOptions } from "./attack/attack";
import Context from "../context";
import Movement from "./rendering/movement";

import { TILE_WIDTH } from "./constants";
import Character from "./parsing/character";

export interface GameUISelection {

}

export default class GameUISelectionHandler {
    private _socket: any;
    private _context: any;
    private _playerID: any;

    public onTurn: boolean;
    public selection: GameUISelection | null;
    public mouseX: number;
    public mouseY: number;

    private _informationPanelSelection: Character | null;

    /**
     * This is a really overengineered way of a user making a single selection at a time
     */
    constructor(socket: WebSocket, playerID: number, context: Context) {
        this._socket = socket;
        this.onTurn = false;
        this._context = context;
        this._playerID = playerID;
        this.selection = null; // Null when no selection has been made
        this._informationPanelSelection = null;
    }

    reset(): void {
        this.selection = null;
        this._context.render();
    }

    setMovement(movement: Movement): void {
        if (this.onTurn) {
            this.selection = movement;
        }
    }

    setAttackOptions(options: AttackOptions): void {
        if (this.onTurn) {
            if (this.selection instanceof Attack) {
                this.selection.setOptions(options)
            }
            else {
                this.selection = new Attack(options);
            }
            this._context.render();
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
        this._context.render();
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

    /**
     * Currently only implemented to display a character information, potentially may want to reuse
     * to show other information eg weapon/armour info
     * 
     * @param character whose information to display
     */
    public setInformationPanel(character: Character) {
        this._informationPanelSelection = character;
        this._context.render();
    }

    public getInformationPanelSelection(): Character | null {
        return this._informationPanelSelection;
    }
}
