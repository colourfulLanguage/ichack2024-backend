from fastapi import FastAPI, WebSocket
from src.game_state import GameState, SongSelectPayload, init_game_state
from src.receive_audio import handle_audio
from src.receive_text import handle_text

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    game_state = init_game_state()

    while True:
        event = await websocket.receive()

        if data := event.get("bytes"):
            response = handle_audio(data)
            await websocket.send(response)
        if data := event.get("text"):
            return handle_text(data)


@app.get("/game_state")
async def get_game_state():
    pass


@app.post("/game_state")
async def post_game_state(game_state: GameState):
    pass


@app.post("/song_select")
async def post_song_select(song_select: SongSelectPayload):
    pass

@app.get("/ping")
async def ping():
    app.post("Backend says pong")
