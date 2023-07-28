import Character from "./parsing/character";

export default class MapState {

    public mapHeight: number;
    public mapWidth: number;
    private _characterGrid: Array<Array<Character>>;

    constructor(mapWidth: number, mapHeight: number, characters: Map<number, Character>) {
        this.mapWidth = mapWidth;
        this.mapHeight = mapHeight;
        this.resetMap();
        characters.forEach((chr: Character, id: number) => {
            this.set(chr.x, chr.y, chr);
        }, this)
    }

    resetMap(): void {
        this._characterGrid = new Array(this.mapWidth);
        for (let col = 0; col < this.mapWidth; col++) {
            this._characterGrid[col] = new Array(this.mapHeight);
        }
    }
    
    /**
     * Gets the player at this location
     */
    get(x: number, y: number): Character | null{
        if (!this._checkCoords(x, y)) {
            return null;
        }
        return this._characterGrid[x][y];
    }
    
    /**
     * Sets the player at this location
     */
    set(x: number, y: number, chr: Character): void {
        if (!this._checkCoords(x, y)) {
            console.log("Invalid player location", x, y)
            return;
        }
        this._characterGrid[x][y] = chr;
    }

    private _checkCoords(x: number, y: number): boolean {
        return 0 <= x
            && x <= this.mapWidth
            && 0 <= y
            && y <= this.mapHeight;
    }
}