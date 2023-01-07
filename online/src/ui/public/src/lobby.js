import { Context } from "./context";
import { ContextHandler } from "./contextHandler";
import { Game } from "./gameScene";

var React = require("react");

export class Lobby extends Context {

    constructor(socket, reactRoot) {
        super(socket, reactRoot, "lobby");
        this.joinGameButton = <div className="leaveGame button" onClick={() => this.transmit("leaveGame")}>Leave</div>
        this.leaveGameButon = <div className="joinGame button" onClick={() => this.transmit("joinGame")}>Join</div>

    }

    render() {
        this.reactRoot.render(
            <div>
                <div className="buttons">
                    { this.joinGameButton }
                    <div className="value">You're ID is: {}</div>
                    { this.leaveGameButon }
                </div>
                <div className="state">
                    <span className="users">{this.inLobby} online, {this.ready} players are ready</span>
                </div>
            </div>);
    }

    handleEvent(contextHandler, event) {
        switch (event.responseType) {
            case "gameStart":
                console.log("starting game");
                const mapStatus = event.mapStatus;
                const playerID = event.playerID;
                const characters = event.characters;
                contextHandler.context = new Game(
                    this.socket,
                    this.reactRoot,
                    mapStatus.mapWidth,
                    mapStatus.mapHeight,
                    playerID,
                    characters);
                break;
            case "users":
                this.inLobby = event.inLobby;
                this.ready = event.ready;
                break;
            default:
        }
    }

    transmit(eventType) {
        this.socket.send(JSON.stringify({ event: eventType }));
    }
    
}