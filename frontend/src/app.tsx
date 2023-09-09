import React, { useState } from "react";

import './ui.css'
import Lobby from "./scenes/lobby/lobby";
import Game from "./scenes/gameScene/gameScene";

interface CurrentScene {
    inLobby: boolean;
    data: any;
}

const App: React.FC<{websocket: WebSocket}> = ({ websocket }) => {

    const [currentScene, setCurrentScene] = useState<CurrentScene>({inLobby: true, data: null});

    return (
      <div className="App">
        {currentScene.inLobby ? <Lobby socket={websocket} setCurrentScene={setCurrentScene} /> : <Game socket={websocket} data={currentScene.data} />}
      </div>
    );
  }

function debugServerMessages(data: JSON) {
    console.log("MESSAGE: ", console.log(data));
}
export default App;