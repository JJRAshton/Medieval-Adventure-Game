import Character from "./parsing/character";

export default class MapState {

    public mapHeight: number;
    public mapWidth: number;
    private _characterGrid: Array<Array<Character>>;

    constructor(mapWidth: number, mapHeight: number, character: Map<number, Character>) {
        this.mapWidth = mapWidth;
        this.mapHeight = mapHeight;
        this.resetMap();
    }

    resetMap(): void {
        this._characterGrid = new Array(this.mapWidth);
        for (let col = 0; col < this.mapWidth; col++) {
            this._characterGrid[col] = new Array(this.mapHeight);
        }
    }
}