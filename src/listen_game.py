from schemas import ListenUserInput, ListenGameState, WebsocketSendPayload
from getsongs import get_song_and_key


async def new_listen_state(websocket, listen_game_init):

    key, bytes_ = get_song_and_key(listen_game_init.song_name)

    key = key[0]

    listen_game_state = ListenGameState(
        song_name=listen_game_init.song_name,
        song_bytes=bytes_,
        song_key=key,
        user_identified_correctly=None,
    )

    payload = WebsocketSendPayload(
        game_type="LISTEN", listen_game_state=listen_game_state, sing_game_state=None
    )
    await websocket.send_json(payload.model_dump_json())

    return listen_game_state


async def handle_listen_input(websocket, listen_user_input, listen_game_state):

    listen_game_state.user_identified_correctly = (
        listen_user_input.user_identified_key == listen_game_state.song_key
    )

    payload = WebsocketSendPayload(
        game_type="LISTEN", listen_game_state=listen_game_state, sing_game_state=None
    )

    await websocket.send_json(payload.model_dump_json())

    return listen_game_state
