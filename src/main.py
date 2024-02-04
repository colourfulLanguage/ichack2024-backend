import json

from fastapi import FastAPI, WebSocket
from sing_game import handle_sing_input, new_sing_state
from listen_game import handle_listen_input, new_listen_state
from fastapi.middleware.cors import CORSMiddleware
from getsongs import query_dict
from schemas import (
    WebsocketRecievePayload,
    WebsocketSendPayload,
    ListenGameInit,
    ListenGameState,
    ListenUserInput,
    SingGameInit,
    SingGameState,
    SingUserInput,
)
from starlette.websockets import WebSocketState

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    sing_game_state = {}
    listen_game_state = {}

    while True:
        print(websocket.client_state)
        event = await websocket.receive()
        if websocket.client_state == WebSocketState.DISCONNECTED:
            print(f"Client disconnected [{websocket.client_state}]")
            return

        print(event)
        print("Event received", event["text"])
        payload = json.loads(event["text"])
        print("Payload", payload)
        event_model = WebsocketRecievePayload(**payload)
        print("Event model created")

        # Initialise State
        if event_model.message_type == "INIT":
            print("Initialising")
            if event_model.game_type == "LISTEN":
                print("Initialising Listen")
                listen_game_state = await new_listen_state(
                    websocket, event_model.listen_game_init
                )
            if event_model.game_type == "SING":
                print("Initialising Sing")
                sing_game_state = await new_sing_state(
                    websocket, event_model.sing_game_init
                )

        # Handle input and update state.
        if event_model.message_type == "UPDATE":
            print("Updating")
            if event_model.game_type == "LISTEN":
                print("Updating Listen")
                # UPDATE STATE BASED ON INPUT
                listen_game_state = await handle_listen_input(
                    websocket, listen_game_state, event_model.listen_user_input
                )
            if event_model.game_type == "SING":
                print("Updating sing")
                # UPDATE STATE BASED ON INPUT
                sing_game_state = await handle_sing_input(
                    websocket, sing_game_state, event_model.sing_user_input
                )


@app.get("/song_names")
async def song_names():
    return {"names": list(query_dict.values())}


@app.get("/ping")
async def ping():
    app.post("Backend says pong")


origins = [
    "http://localhost:3000",  # Adjust the port if your frontend runs on a different one
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows specified origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)
