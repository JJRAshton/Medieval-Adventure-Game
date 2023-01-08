import { Lobby } from "./lobby"
import { Game } from "./gameScene";

import Context from "./context";
import { FC } from "react";


export default class ContextHandler {

    private reactRoot: any;
    private socket: any;

    public context: Context;

    constructor(root: FC<{}>, socket: WebSocket) {
        this.context = new Lobby(socket, root);
        this.reactRoot = root;
        this.socket = socket;
    }

    handleEvent(data: string) {
        const event = JSON.parse(data);

        this.context.handleEvent(this, event);
        this.context.render();
    }
}