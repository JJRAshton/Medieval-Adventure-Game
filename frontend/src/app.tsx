import React from "react";

import './ui.css'
import Lobby from "./scenes/lobby/lobby";

const App: React.FC<{websocket: WebSocket}> = ({ websocket }) => {
    return (
      <div className="App">
        <Lobby socket={websocket} />
      </div>
    );
  }

function debugServerMessages(data: JSON) {
    console.log("MESSAGE: ", console.log(data));
}
export default App;