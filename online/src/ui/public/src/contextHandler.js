import { Lobby } from "./lobby.js"
import { Game } from "./gameScene.js";

import { Context } from "./context.js";


export class ContextHandler {

    constructor(root, socket) {
        this.context = new Lobby(socket, root);
        this.reactRoot = root;
        this.socket = socket;
    }

    handleEvent(data) {
        const event = JSON.parse(data);

        this.context.handleEvent(this, event);
        this.context.render();
    }
}