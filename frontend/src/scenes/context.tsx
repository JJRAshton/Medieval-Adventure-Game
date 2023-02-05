import React from "react";
import ContextHandler from "./contextHandler";

export default abstract class Context {
    protected socket: WebSocket;
    protected reactRoot: any;
    private contextString: String;

    constructor(socket: WebSocket, reactRoot: any, contextString: String) {
        this.socket = socket;
        this.reactRoot = reactRoot;
        this.contextString = contextString;
    }

    getString(): String {
        return this.contextString;
    }

    render(): void {
        this.reactRoot.render(<div>Abstract context should not be rendered.</div>);
    }

    abstract handleEvent(contextHandler: ContextHandler, event: any): void;
}