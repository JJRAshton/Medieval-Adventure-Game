import React from "react";
import Canvas from "./rendering/gameCanvas";
import Character from "./parsing/character";

import GameUISelectionHandler from "./gameUISelection";

import GameState from "./gameState";
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

    const _parseCharacters = (characters: any) => {
        const characterMap = new Map();
        for (var i = 0; i < characters.length; i++) {
            const character = characters[i];
            socket.send(JSON.stringify({event: "playerInfoRequest", characterID: character[0]}))
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
        state.mapState.resetMap();
        for (let id in charactersInfo) {
            const chr = _getPlayerWithId(id);
            chr.update(charactersInfo[id]);
            state.mapState.set(chr.x, chr.y, chr);
        }
    }

    const selectionHandler = new GameUISelectionHandler(socket, playerID);
    const characters = _parseCharacters(characterJson);
    const state: GameState = new GameState(_getPlayerWithId(playerID), characters, mapWidth, mapHeight);
    const canvas = new Canvas(selectionHandler, socket, state);

    // Processing events from server
    socket.onmessage = ({data}) => {
        const event = JSON.parse(data);

        console.log(event);
        switch (event.responseType) {
            case "turnNotification":
                // These will get sent when the turn changes
                selectionHandler.reset();
                
                selectionHandler.onTurn = event.onTurnID === state.character.id;
                updatePlayers(event.charactersUpdate);
                break;
            case "mapUpdate":
                // These get sent when someone moves, or when something changes
                state.mapState.resetMap();
                event.characters.forEach((characterInfo: [number, [number, number]]) => {
                    const chr = _getPlayerWithId(characterInfo[0]);
                    chr.setPosition(characterInfo[1][0], characterInfo[1][1]);
                    state.mapState.set(chr.x, chr.y, chr);
                }, this)
                break;
            case "playerInfo":
                _getPlayerWithId(event.characterID).construct(event.playerInfo, event.characterID === state.character.id, selectionHandler);
                break;
            case "attackResult":
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
                { canvas.render() }
                <InfoPanel selectionHandler={selectionHandler} socket={socket} gameState={state} />
            </div>
        </div>
    );
}

export default Game;

export { GamePropsData };