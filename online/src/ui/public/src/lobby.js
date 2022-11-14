import { Context } from "./context";
import { ContextHandler } from "./contextHandler";
import { Game } from "./gameScene";

var React = require("react");

export class Lobby extends Context {

    constructor(socket) {
        super(socket, "lobby");
        this.socket = socket;
        this.joinGameButton = <div className="leaveGame button" onClick={() => this.transmit("leaveGame")}>Leave</div>
        this.leaveGameButon = <div className="joinGame button" onClick={() => this.transmit("joinGame")}>Join</div>

    }

    render(reactRoot) {
        reactRoot.render(
            <div>
                <div className="buttons">
                    { this.joinGameButton }
                    <div className="value">You're ID is: {}</div>
                    { this.leaveGameButon }
                </div>
                <div className="state">
                    <span className="users">{this.inLobby}</span> online
                </div>
            </div>);
    }

    handleEvent(contextHandler, event) {
        switch (event.responseType) {
            case "gameStart":
                console.log("starting game");
                contextHandler.context = new Game();
                break;
            default:
        if (event.type === "users") {
            this.inLobby = event.inLobby;
        }
        }
        if (event.responseType === "gameStart") {
            console.log("starting game");
            contextHandler.context = new Game();
        }
        console.log("message received " + event);
        return this;
    }

    transmit(eventType) {
        console.log(eventType);
        this.socket.send(JSON.stringify({ action: eventType }));
    }
    
}