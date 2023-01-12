import Character from "./parsing/character";

export default class GameState {

    public character: Character;
    public characters: Map<number, Character>;

    // This will probably move into a map class once there is more information about the map
    public mapWidth: number;
    public mapHeight: number;

    constructor(character: Character, characters: Map<number, Character>, mapWidth: number, mapHeight: number) {
        this.character = character;
        this.characters = characters;

        this.mapWidth = mapWidth;
        this.mapHeight = mapHeight;
    }
}