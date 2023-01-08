import React from "react";
import { ContextHandler } from "./contextHandler";

export abstract class Context {

    constructor(socket, reactRoot, contextString) {
        this.socket = socket;
        this.reactRoot = reactRoot;
        this.contextString = contextString;
    }

    getString() {
        return this.contextString;
    }

    render() {
        this.reactRoot.render(<div>Abstract context should not be rendered.</div>);
    }

    abstract handleEvent(contextHandler: ContextHandler, event: any);
}