import { Lobby } from "./lobby"
import { Game } from "./gameScene";

import { Context } from "./context";


export class ContextHandler {
    private context: Context;
    private reactRoot: any;
    private socket: any;

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