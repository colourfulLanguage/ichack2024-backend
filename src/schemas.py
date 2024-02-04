from pydantic import BaseModel
from typing import Optional


# LISTEN SCHEMAS
class ListenUserInput(BaseModel):
    user_identified_key: str


class ListenGameState(BaseModel):
    song_name: str
    song_bytes: str
    song_key: str
    user_identified_correctly: Optional[bool]


class ListenGameInit(BaseModel):
    song_name: str


# SING SCHEMAS
class SingUserInput(BaseModel):
    user_audio_bytes: str


class SingGameState(BaseModel):
    actual_note: str
    actual_bytes: str
    user_note: Optional[str]


class SingGameInit(BaseModel):
    pass


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
