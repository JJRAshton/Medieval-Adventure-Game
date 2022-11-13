var React = require("react");

const joinGameButton = <div className="leaveGame button" onClick={() => transmit("leaveGame")}>Leave</div>;
const leaveGameButon = <div className="joinGame button" onClick={() => transmit("joinGame")}>Join</div>;

export function renderLobby(reactRoot) {
    reactRoot.render(
        <div>
            <div className="buttons">
                { joinGameButton }
                <div className="value">You're ID is: {}</div>
                { leaveGameButon }
            </div>
            <div className="state">
                <span className="users">?</span> online
            </div>
        </div>);
}

function transmit(eventType) {
    console.log(eventType);
    websocket.send(JSON.stringify({ action: eventType }));
}
