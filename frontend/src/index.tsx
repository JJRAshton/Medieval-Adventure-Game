import React from "react";
import { createRoot } from 'react-dom/client';

import './ui.css'
import App from './app';

const websocket = new WebSocket("ws://localhost:8001/");

const container = document.getElementById('reactRoot');
const root = createRoot(container!);

websocket.addEventListener("open", () => {
    root.render(<App websocket={websocket} />);
});