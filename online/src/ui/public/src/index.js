import { createRoot }  from "react-dom/client";
import { ContextHandler } from "./contextHandler.js";

import './ui.css'

const root = createRoot(document.getElementById("reactRoot"));
const websocket = new WebSocket("ws://localhost:8001/");

websocket.addEventListener("open", () => {
    const contextHandler = new ContextHandler(root, websocket);
    websocket.onmessage = ({ data }) => {
        console.log("MESSAGE:");
        console.log(data);
        contextHandler.handleEvent(data)
    };
});