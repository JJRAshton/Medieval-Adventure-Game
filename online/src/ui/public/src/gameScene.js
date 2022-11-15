import { Context } from "./context";
import { React } from "react";

export class Game extends Context {

    constructor() {
        super("game");
    }

    render(reactRoot) {
        reactRoot.render(<div>Now in a game!</div>);
    }



}