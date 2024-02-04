from pydantic import BaseModel
from typing import Optional

# LISTEN SCHEMAS
class ListenUserInput(BaseModel):
    user_identified_key: str


class ListenGameState(BaseModel):
    song_name: str
    song_bytes: bytes
    song_key: str
    user_identified_correctly: bool | None


class ListenGameInit(BaseModel):
    song_name: str


# SING SCHEMAS
class SingUserInput(BaseModel):
    user_audio_bytes: bytes


class SingGameState(BaseModel):
    audio_key: dict
    actual_note: str
    user_note: str | None


class SingGameInit(BaseModel):
    audio_key: dict
    actual_note: str


"""
Websocket messages should always come in this form.
"""


class WebsocketRecievePayload(BaseModel):

    # LISTEN / SING
    game_type: str
    # INIT / UPDATE
    message_type: str

    sing_user_input: Optional[SingUserInput]
    listen_user_input: Optional[ListenUserInput]

    listen_game_init: Optional[ListenGameInit]
    sing_game_init: Optional[SingGameInit]


"""
Websocket messages should always be sent in this form.
"""


class WebsocketSendPayload(BaseModel):

    # LISTEN / SING
    game_type: str

    sing_game_state: Optional[SingGameState]
    listen_game_state: Optional[ListenGameState]
