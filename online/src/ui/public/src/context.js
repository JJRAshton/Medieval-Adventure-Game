import React from "react";

export class Context {

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
}