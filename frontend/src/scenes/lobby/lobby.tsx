import { useState } from "react";
import CharacterCustomistationComponent, { CharacterClassOption } from "./classSelection";
import { GamePropsData } from "../gameScene/gameScene";

var React = require("react");


interface LobbyProps {
    socket: WebSocket;
    setCurrentScene;
}

const Lobby: React.FC<LobbyProps> = ({ socket, setCurrentScene }) => {

    const [playerInLobby, setPlayersInLobby] = useState<number>(0);
    const [playerReady, setPlayersReady] = useState<number>(0);

    const characterClassOptions: CharacterClassOption[] = [{value: "class1"}, {value: "class2"}];
    const weaponOptions = {
        "class1": ["Weapon for class 1"],
        "class2": ["Weapon for class 2"]
    };
    
    const transmit = (eventType: string) => {
        socket.send(JSON.stringify({ event: eventType }));
    }

    socket.onmessage = ({ data }) => {
        const event = JSON.parse(data);
        switch (event.responseType) {
            case "gameStart":
                // Maybe we still need some sort of context manager, because it's going to be
                // tricky to switch component otherwise?
                console.log("starting game");
                const gameProps: GamePropsData = {
                    characterJson: event.characters,
                    mapWidth: event.mapStatus.mapWidth,
                    mapHeight: event.mapStatus.mapHeight,
                    playerID: event.playerID
                }
                setCurrentScene({inLobby: false, data: gameProps})
                break;
            case "users":
                setPlayersInLobby(event.inLobby);
                setPlayersReady(event.ready);
                break;
            default:
        }
    }

    return (
        <div>
            <CharacterCustomistationComponent characterClassSelection={characterClassOptions} weaponSelection={weaponOptions} />
            <div className="buttons">
                <div className="leaveGame button" onClick={() => transmit("leaveGame")}>Leave</div>
                <div className="value">You're ID is: {}</div>
                <div className="joinGame button" onClick={() => transmit("joinGame")}>Join</div>
            </div>
            <div className="state">
                <span className="users">{playerInLobby} online, {playerReady} players are ready</span>
            </div>
        </div>
    );
}

export default Lobby;

export { LobbyProps }