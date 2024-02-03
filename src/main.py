from fastapi import FastAPI, WebSocket
from sing_game import handle_sing_input, new_sing_state
from listen_game import handle_listen_input, new_listen_state
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

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    listen_game_state = None
    sing_game_state = None

    while True:
        print("Waiting")
        event = await websocket.receive()
        print("Recieved")
        print(event)
        if event["type"] == "websocket.disconnect":
            print("Disconnected")
            return

        event_model = WebsocketRecievePayload(**event)

        # Initialise State
        if event_model.message_type == "INIT":
            if event_model.game_type == "LISTEN":
                listen_game_state = new_listen_state(event_model.listen_game_init)
            if event_model.game_type == "SING":
                sing_game_state = new_sing_state(event_model.sing_game_init)

        # Handle input and update state.
        if event_model.message_type == "UPDATE":
            if event_model.game_type == "LISTEN":

                # UPDATE STATE BASED ON INPUT
                listen_game_state = handle_listen_input(
                    listen_game_state, event_model.listen_user_input
                )
            if event_model.game_type == "SING":

                # UPDATE STATE BASED ON INPUT
                sing_game_state = handle_sing_input(
                    sing_game_state, event_model.sing_user_input
                )


@app.get("/ping")
async def ping():
    app.post("Backend says pong")
