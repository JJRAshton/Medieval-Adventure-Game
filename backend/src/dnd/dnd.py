import asyncio
import json
import copy
import websockets

from typing import Set
from websockets.legacy.server import WebSocketServerProtocol as WebSocket

from .api.users import currentUsers
from .api.users import User
from .api.api_session import APISession

from .backend.processing.entities.stats.entity_factory import ENTITY_STAT_PROVIDER
from .backend.processing.entities.classes.player_class import ALL

# Potentially these shouldn't yet be api.users.User, and get transformed only once a game starts?
playerPool: Set[User] = set()
uuid_tracker: int = 1

def getUserByWS(socket: WebSocket):
    for user in currentUsers:
        if user.socket == socket:
            return user

def broadcast(event: str) -> None:
    websockets.broadcast({user.socket for user in currentUsers}, event) # type: ignore

def users_event() -> str:
    return json.dumps({"responseType": "users", "inLobby": len(currentUsers), "ready": len(playerPool)})

def value_event() -> str:
    return json.dumps({"responseType": "value", "value": uuid_tracker})

async def addToLobby(websocket: WebSocket):
    global uuid_tracker
    user = User(websocket, uuid_tracker)
    try:
        # Wrap the websocket in a User
        print(f"New connection, there are new {len(currentUsers)} users in the lobby")
        # Send current state to user
        await websocket.send(value_event())
        uuid_tracker += 1
        broadcast(users_event())
        print(users_event())

        # Manage state changes
        async for message in websocket:
            event = json.loads(message)
            if user.session is not None:
                user.sessionRequest(event)
            elif event["event"] == "basicClassRequest":
                # This should probably shouldn't be here
                print(event)
                class_options = {}
                for player_class in ALL:
                    df = ENTITY_STAT_PROVIDER.weapons
                    available_weapons = df[(df.Type.isin(player_class.weapons))].index.tolist()
                    class_options[player_class.name] = available_weapons

                websockets.broadcast({user.socket}, json.dumps({"responseType": "classAndWeaponOptions", "options": class_options}))
            elif event["event"] == "joinGame":
                print(event)
                if ("characterName" in event and "playerClass" in event and "weapon" in event):
                    user.set_character_preferences(event["characterName"], event["playerClass"], event["weapon"])
                else:
                    print(f"Invalid customisation options: {event}")
                playerPool.add(user)
                broadcast(users_event())
                if len(playerPool) > 1:
                    APISession(copy.copy(playerPool))
                    # All players should now have been added to the game, so removes them from the pool.
                    playerPool.clear()
            elif event["event"] == "leaveGame":
                user.clear_character_preferences()
                if user in playerPool:
                    playerPool.remove(user)
                    broadcast(users_event())
            else:
                print(f"Unsupported event: {event}")
    finally:
        # Unregister user
        if user in playerPool:
            playerPool.remove(user)
        currentUsers.remove(user)
        websockets.broadcast({user.socket for user in currentUsers}, users_event())

async def main():
    async with websockets.serve(addToLobby, "localhost", 8001):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
