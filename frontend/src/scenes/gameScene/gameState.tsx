import MapState from "./MapState";
import Character from "./parsing/character";

export default class GameState {

    public character: Character;
    public characters: Map<number, Character>;

    public mapState: MapState;

    constructor(character: Character, characters: Map<number, Character>, mapWidth: number, mapHeight: number) {
        this.character = character;
        this.characters = characters;

        this.mapState = new MapState(mapWidth, mapHeight, characters);
    }
}