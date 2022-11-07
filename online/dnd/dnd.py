#!/usr/bin/env python

import asyncio
import json
import websockets

class User:
    def __init__(self, ws, uuid):
        self.uuid = uuid
        self.ws = ws
        self.ready = False

    def __str__(self):
        return f"User with id: {self.uuid}"

def getUserByWS(ws):
    for user in users:
        if user.ws == ws:
            return user

users = set()
UUID_TRACKER = 1

def users_event():
    return json.dumps({"type": "users", "inLobby": len(users), "ready": len([user for user in users if user.ready])})

def value_event():
    return json.dumps({"type": "value", "value": 7})

async def counter(websocket):
    global UUID_TRACKER
    try:
        # Register user
        users.add(User(websocket, UUID_TRACKER))
        UUID_TRACKER += 1
        print(users)
        print(users_event())
        websockets.broadcast({user.ws for user in users}, users_event())
        # Send current state to user
        await websocket.send(value_event())
        # Manage state changes
        async for message in websocket:
            event = json.loads(message)
            print(event)
            if event["action"] == "joinGame":
                getUserByWS(websocket).ready = True
                websockets.broadcast({user.ws for user in users}, users_event())
            elif event["action"] == "leaveGame":
                getUserByWS(websocket).ready = False
                websockets.broadcast({user.ws for user in users}, users_event())
            else:
                print(f"unsupported event: {event}")
    finally:
        # Unregister user
        users.remove(getUserByWS(websocket))
        websockets.broadcast({user.ws for user in users}, users_event())

async def main():
    async with websockets.serve(counter, "localhost", 8000):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())