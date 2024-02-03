from pydantic import BaseModel


class GameState(BaseModel):
    pass


class SongSelectPayload(BaseModel):

    name: str


def init_game_state() -> GameState:
    state = GameState()
    return state
