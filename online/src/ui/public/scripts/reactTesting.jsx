const root = ReactDOM.createRoot(document.getElementById("reactRoot"));
const websocket = new WebSocket("ws://localhost:8001/");

websocket.addEventListener("open", (event) => {
    websocket.onmessage = (data) => {
        const joinGameButton = <div className="leaveGame button" onClick={() => transmit("leaveGame")}>Leave</div>
        const leaveGameButon = <div className="joinGame button" onClick={() => transmit("joinGame")}>Join</div>
        const event = JSON.parse(data);
        console.log("message received " + event);
        root.render(
            <div>
                <div className="buttons">
                    {joinGameButton}
                    <div className="value">You're ID is: ?</div>
                    {leaveGameButon}
                </div>
                <div className="state">
                    <span className="users">?</span> online
                </div>
            </div>
        );
    };
})

function transmit(eventType) {
    console.log(eventType)
    websocket.send(JSON.stringify({ action: eventType }))
}

websocket.onmessage = ({ data }) => {
    const event = JSON.parse(data);
    console.log("message received: "+ event);
  };