import { createRoot } from "react-dom/client";
import { ContextHandler } from "./contextHandler";

import './ui.css'

const root = createRoot(document.getElementById("reactRoot"));
const websocket = new WebSocket("ws://localhost:8001/");

websocket.addEventListener("open", () => {
    const contextHandler = new ContextHandler(root, websocket);
    websocket.onmessage = ({ data }) => {
        // debugServerMessages(data);

        contextHandler.handleEvent(data)
    };
});

function debugServerMessages(data: JSON) {
    console.log("MESSAGE:");
    console.log(data);
}