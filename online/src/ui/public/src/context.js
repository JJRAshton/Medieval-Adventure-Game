var React = require("react");

export class Context {

    constructor(socket, contextString) {
        this.socket = socket;
        this.contextString = contextString;
    }

    getString() {
        return this.contextString;
    }

    render(reactRoot) {
        reactRoot.render(<div>Abstract context should not be rendered.</div>);
    }
}