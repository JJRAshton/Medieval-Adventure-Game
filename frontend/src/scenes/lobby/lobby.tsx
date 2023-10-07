import { useEffect, useState } from "react";
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
    const [readied, setReadied] = useState<boolean>(false); // Whether the play has clicked join or is still customising

    const [playerClass, setPlayerClass] = useState<string>('');
    const [weapon, setWeapon] = useState<string>('');
    const [characterName, setCharacterName] = useState<string>('');

    const [classOptions, setClassOptions] = useState<Record<string, string[]>>({
        class1: ["Weapon for class 1"],
        class2: ["Weapon for class 2"]
    });
    
    const transmitJoin = () => {
        socket.send(JSON.stringify({ 
            event: "joinGame" ,
            characterName: characterName,
            playerClass: playerClass,
            weapon: weapon
        }));
    }

    const transmitLeave = () => {
        socket.send(JSON.stringify({ event: "leaveGame" }));
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

            case "classAndWeaponOpions":
                setClassOptions(event.options)
                break;
            default:
        }
    }

    useEffect(() => {
        socket.send(JSON.stringify({ event: "basicClassRequest" }));
    }, [])

    return (
        <div>
            <CharacterCustomistationComponent
                classOptions={classOptions}
                readied={readied}
                characterName={characterName}
                setCharacterName={setCharacterName}
                playerClass={playerClass}
                setPlayerClass={setPlayerClass}
                weapon={weapon}
                setWeapon={setWeapon} />
            <div className="buttons">
                <div className="leaveGame button" onClick={() => {
                    transmitLeave();
                    setReadied(false);
                }}>Leave</div>
                <div className="value">Your ID is: {}</div>
                <div className="joinGame button" onClick={() => {
                    transmitJoin();
                    setReadied(true);
                }}>Join</div>
            </div>
            <div className="state">
                <span className="users">{playerInLobby} online, {playerReady} players are ready</span>
            </div>
        </div>
    );
}

export default Lobby;

export { LobbyProps }