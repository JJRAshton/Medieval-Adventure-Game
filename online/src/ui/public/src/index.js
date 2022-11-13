import { renderLobby } from "./lobby.js";
import { createRoot }  from "react-dom/client";
import './ui.css'

const root = createRoot(document.getElementById("reactRoot"));
const websocket = new WebSocket("ws://localhost:8001/");

websocket.addEventListener("open", (event) => {
    renderLobby(root);
    renderGameScene(root);
    websocket.onmessage = (data) => {
        const event = JSON.parse(data);
        if (event.context === "lobby") {
            if (event.responseType === "gameStart") {
                console.log(event.map);
                addIDs(event.ids);
                root.render(mapRendering);
            }
            console.log("message received " + event);
        }
        if (event.context = "game") {
            
        }
    };
});