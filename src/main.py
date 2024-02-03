from fastapi import FastAPI, WebSocket
from game_state import GameState, SongSelectPayload

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.websocket("/recieve_audio")
async def recieve_audio(websocket: WebSocket):
    pass


@app.get("/game_state")
async def get_game_state():
    pass


@app.post("/game_state")
async def post_game_state(game_state: GameState):
    pass


@app.post("/song_select")
async def post_song_select(song_select: SongSelectPayload):
    pass
