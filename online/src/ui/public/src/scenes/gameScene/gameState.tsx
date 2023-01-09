import Character from "./parsing/character";

export default class GameState {

    public character: Character;
    public characters: Map<number, Character>;
    public onTurn: boolean;

    constructor(character: Character, characters: Map<number, Character>) {
        this.character = character;
        this.characters = characters;
        this.onTurn = false;
    }
}