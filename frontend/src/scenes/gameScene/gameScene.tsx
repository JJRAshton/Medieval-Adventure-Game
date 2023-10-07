import React, { useEffect, useState } from "react";
import Canvas from "./rendering/gameCanvas";
import Character, { constructCharacter, createCharacterInitial, setPosition, updateCharacter } from "./parsing/character";

import GameUISelectionHandler, { GameUISelection } from "./gameUISelection";

import InfoPanel from "./rendering/infoPanel";

interface GameProps {
    socket: WebSocket;
    data: GamePropsData;
}

interface GamePropsData {
    characterJson: JSON;
    mapWidth: number;
    mapHeight: number;
    playerID: string;
}

const Game: React.FC<GameProps> = ({socket, data}) => {
    const { characterJson, mapWidth, mapHeight, playerID } = data;

    const _parseCharacters = (characters: JSON) => {
        let newCharacters = {}
        Object.values(characters).forEach((initialCharacterJSON: JSON) => {
            const id = initialCharacterJSON[0];
            newCharacters[id] = createCharacterInitial(initialCharacterJSON);
        });
        return newCharacters;
    }

    const _getPlayerWithId = (id: string) => {
        const character = characters[id];
        if (!character) {
            console.log(characters)
            throw new Error("Critical error: Did not recognise character with ID: " + id + ".");
        }
        return character;
    }

    const updatePlayers = (charactersInfo) => {
        for (let id in charactersInfo) {
            const chr = _getPlayerWithId(id);
            characters[id] = updateCharacter(chr, charactersInfo[id].Health, charactersInfo[id].coords);
        }
        setCharacters(characters);
    }

    const selectionHandler = new GameUISelectionHandler(socket, playerID);

    const [characters, setCharacters] = useState<Record<string, Character>>(_parseCharacters(characterJson));
    const [character, setCharacter] = useState<Character>(_getPlayerWithId(playerID));
    const [onTurn, setOnTurn] = useState<boolean>(false);
    const [selection, setSelection] = useState<GameUISelection | null>(null);
    const [infoPanelSelection, setInfoPanelSelection] = useState<Character | null>(null);

    useEffect(() => {
        Object.entries(characters).forEach(([id, character]) => {
            if (!character.infoReceived) {
                socket.send(JSON.stringify({event: "playerInfoRequest", characterID: id}))
            }
        });
    }, [characters]);

    const mapSize = {mapWidth,  mapHeight}

    // Processing events from server
    socket.onmessage = ({data}) => {
        const event = JSON.parse(data);

        console.log(event);
        switch (event.responseType) {
            case "turnNotification":
                // These will get sent when the turn changes
                selectionHandler.reset();
                
                setOnTurn(event.onTurnID === character.id);
                updatePlayers(event.charactersUpdate);
                break;
            case "mapUpdate":
                // These get sent when someone moves, or when something changes
                const newCharacters = {...characters};
                event.characters.forEach((characterInfo: [string, [number, number]]) => {
                    newCharacters[characterInfo[0]] = setPosition(characters[characterInfo[0]], characterInfo[1][0], characterInfo[1][1]);                    
                })
                setCharacters(newCharacters)
                break;
            case "playerInfo":
                const newCharacter = constructCharacter(_getPlayerWithId(event.characterID), event.playerInfo, true, selectionHandler);
                if (character && event.characterID === character.id) {
                    setCharacter(newCharacter);
                }
                const characterForPlayerInfoUpdate = {...characters};
                characterForPlayerInfoUpdate[event.characterID] = newCharacter;
                setCharacters(characterForPlayerInfoUpdate);
                break;
            case "attackResult":
                // Are we intentionally doing nothing with this?
                break;
            default:
                console.log("Unrecognised even with type " + event.responseType)
        }
    }

    return (
        <div>
            <h2>
                <div className="message">{onTurn ? "It's your turn" : "It's someone else's turn"}</div>
            </h2>
            <div className="game">
                <Canvas mapSize={mapSize} selectionHandler={selectionHandler} characters={characters} character={character} socket={socket} onTurn={onTurn} setInfoPanelSelection={setInfoPanelSelection} infoPanelSelection={infoPanelSelection} />
                <InfoPanel selectionHandler={selectionHandler} socket={socket} character={character} characters={characters} onTurn={onTurn} infoPanelSelection={infoPanelSelection} />
            </div>
        </div>
    );
}

export default Game;

export { GamePropsData };