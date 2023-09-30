import React, { useEffect, useState } from "react";
import Canvas from "./rendering/gameCanvas";
import Character from "./parsing/character";

import GameUISelectionHandler from "./gameUISelection";

import InfoPanel from "./rendering/infoPanel";
import MapState from "./MapState";

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

    const _parseCharacters = (characters: any) => {
        const characterMap = new Map();
        for (var i = 0; i < characters.length; i++) {
            const character = characters[i];
            const chr = new Character(character[0], character[1][0], character[1][1]);
            characterMap.set(character[0], chr)
        }
        return characterMap
    }
    
    const _getPlayerWithId = (id: string) => {
        const character = characters.get(id);
        if (!character) {
            throw new Error("Critical error: Did not recognise character with ID: " + id + ".");
        }
        return character;
    }

    const updatePlayers = (charactersInfo: any) => {
        console.log(charactersInfo);
        mapState.resetMap();
        for (let id in charactersInfo) {
            const chr = _getPlayerWithId(id);
            chr.update(charactersInfo[id]);
            mapState.set(chr.x, chr.y, chr);
        }
    }

    const selectionHandler = new GameUISelectionHandler(socket, playerID);

    const [characters, setCharacters] = useState<Map<string, Character>>(_parseCharacters(characterJson));
    const [character, setCharacter] = useState<Character>(_getPlayerWithId(playerID));

    useEffect(() => {
        characters.forEach((character, id) => {
            if (!character.infoReceived) {
                socket.send(JSON.stringify({event: "playerInfoRequest", characterID: id}))
            }
        });
    }, [characters]);

    // const state: GameState = new GameState(_getPlayerWithId(playerID), characters, mapWidth, mapHeight);
    const mapState: MapState = new MapState(mapWidth, mapHeight, characters)

    // Processing events from server
    socket.onmessage = ({data}) => {
        const event = JSON.parse(data);

        console.log(event);
        switch (event.responseType) {
            case "turnNotification":
                // These will get sent when the turn changes
                selectionHandler.reset();
                
                selectionHandler.onTurn = event.onTurnID === character.id;
                updatePlayers(event.charactersUpdate);
                break;
            case "mapUpdate":
                // These get sent when someone moves, or when something changes
                mapState.resetMap();
                event.characters.forEach((characterInfo: [string, [number, number]]) => {
                    const chr = _getPlayerWithId(characterInfo[0]);
                    chr.setPosition(characterInfo[1][0], characterInfo[1][1]);
                    mapState.set(chr.x, chr.y, chr);
                }, this)
                break;
            case "playerInfo":
                if (character && event.characterID === character.id) {
                    setCharacter({ ..._getPlayerWithId(event.characterID).construct(event.playerInfo, true, selectionHandler)});
                }
                _getPlayerWithId(event.characterID).construct(event.playerInfo, event.characterID === character.id, selectionHandler);
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
                <div className="message">{selectionHandler.onTurn ? "It's your turn" : "It's someone else's turn"}</div>
            </h2>
            <div className="game">
                <Canvas mapState={mapState} selectionHandler={selectionHandler} characters={characters} character={character} socket={socket} />
                <InfoPanel selectionHandler={selectionHandler} socket={socket} character={character} characters={characters} mapState={mapState} />
            </div>
        </div>
    );
}

export default Game;

export { GamePropsData };