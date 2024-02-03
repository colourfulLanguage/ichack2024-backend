from pydantic import BaseModel


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

    sing_user_input: SingUserInput | None
    listen_user_input: ListenUserInput | None

    listen_game_init: ListenGameInit | None
    sing_game_init: SingGameInit | None


"""
Websocket messages should always be sent in this form.
"""


class WebsocketSendPayload(BaseModel):

    # LISTEN / SING
    game_type: str

    sing_game_state: SingGameState | None
    listen_game_state: ListenGameState | None
