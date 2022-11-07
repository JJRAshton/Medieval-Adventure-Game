window.addEventListener("DOMContentLoaded", () => {
    const websocket = new WebSocket("ws://localhost:8000/");
  
    document.querySelector(".joinGame").addEventListener("click", () => {
      websocket.send(JSON.stringify({ action: "joinGame" }));
    });
  
    document.querySelector(".leaveGame").addEventListener("click", () => {
      websocket.send(JSON.stringify({ action: "leaveGame" }));
    });
  
    websocket.onmessage = ({ data }) => {
      const event = JSON.parse(data);
      switch (event.type) {
        case "value":
          document.querySelector(".value").textContent = event.value;
          break;
        case "users":
          console.log(event)
          const users = "Users in lobby: "+String(event.inLobby)+", Users ready:"+String(event.ready);
          document.querySelector(".users").textContent = users;
          break;
        default:
          console.error("unsupported event", event);
      }
    };
  });