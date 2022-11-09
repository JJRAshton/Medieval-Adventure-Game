# I feel like all of this should ultimately become part of the api module,
# once there's a bit more to the lobby management.
import asyncio
import json
import websockets

from api.users import currentUsers
from api.users import User
from api.api_session import APISession

# Potentially these shouldn't yet be api.users.User yet, and get transformed only once a game starts?
playerPool = set()
UUID_TRACKER = 1 # Initialise at 1

def getUserByWS(socket):
    for user in currentUsers:
        if user.socket == socket:
            return user

def broadcast(event):
    websockets.broadcast({user.socket for user in currentUsers}, event)

def users_event():
    return json.dumps({"type": "users", "inLobby": len(currentUsers), "ready": len(playerPool)})

def value_event():
    return json.dumps({"type": "value", "value": UUID_TRACKER})

async def addToLobby(websocket):
    # Eww a global variable, would be nice to get rid of this
    global UUID_TRACKER
    try:
        # Wrap the websocket in a User
        user = User(websocket, UUID_TRACKER)
        print(currentUsers)
        # Send current state to user
        await websocket.send(value_event())
        UUID_TRACKER += 1
        broadcast(users_event())

        # Manage state changes
        async for message in websocket:
            event = json.loads(message)
            print(event)
            if user.session:
                user.sessionRequest(event)
            if event["action"] == "joinGame":
                playerPool.add(user)
                broadcast(users_event())
                if len(playerPool) > 2:
                    APISession(playerPool)
                    # All players should now have been added to the game, so removes them from the pool.
                    playerPool.clear()
            elif event["action"] == "leaveGame":
                playerPool.remove(user)
                broadcast(users_event())
            else:
                print(f"unsupported event: {event}")
    finally:
        # Unregister user
        currentUsers.remove(user)
        websockets.broadcast({user.socket for user in currentUsers}, users_event())

async def main():
    async with websockets.serve(addToLobby, "localhost", 8000):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())