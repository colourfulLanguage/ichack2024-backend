from pydantic import BaseModel


class GameState(BaseModel):
    pass


class SongSelectPayload(BaseModel):

    name: str
