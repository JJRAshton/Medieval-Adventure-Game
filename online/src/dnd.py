#!/usr/bin/env python

import asyncio
import json
import websockets

class User:
    def __init__(self, ws, uuid):
        self.uuid = uuid
        self.ws = ws
        self.ready = False
        users.add(self)

    def __str__(self):
        return f"User with id: {self.uuid}"

def getUserByWS(ws):
    for user in users:
        if user.ws == ws:
            return user

def broadcast(event):
    websockets.broadcast({user.ws for user in users}, event)


users = set()
protoGame = set()
UUID_TRACKER = 1 # Initialise at 1

def users_event():
    return json.dumps({"type": "users", "inLobby": len(users), "ready": len(protoGame)})

def value_event():
    return json.dumps({"type": "value", "value": UUID_TRACKER})

async def addToLobby(websocket):
    # Eww a global variable, would be nice to get rid of this
    global UUID_TRACKER
    try:
        # Wrap the websocket in a User
        user = User(websocket, UUID_TRACKER)
        print(users)
        # Send current state to user
        await websocket.send(value_event())
        UUID_TRACKER += 1
        broadcast(users_event())

        # Manage state changes
        async for message in websocket:
            event = json.loads(message)
            print(event)
            if event["action"] == "joinGame":
                protoGame.add(user)
                broadcast(users_event())
                if len(protoGame()) > 2:
                    PlayerPool(protoGame)
            elif event["action"] == "leaveGame":
                protoGame.remove(user)
                broadcast(users_event())
            else:
                print(f"unsupported event: {event}")
    finally:
        # Unregister user
        users.remove(user)
        websockets.broadcast({user.ws for user in users}, users_event())

async def main():
    async with websockets.serve(addToLobby, "localhost", 8000):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())