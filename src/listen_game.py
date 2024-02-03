from schemas import ListenUserInput, ListenGameState
from getsongs import get_song_and_key


def new_listen_state(websocket, listen_game_init):

    key, bytes_ = get_song_and_key(listen_game_state.song_name)

    listen_game_state = ListenGameState(
        listen_game_init.song_name, song_bytes=bytes_, song_key=key
    )

    websocket.send(listen_game_state.model_dump_json())

    return listen_game_state


def handle_listen_input(websocket, listen_user_input, listen_game_state):

    listen_game_state.user_identified_correctly = (
        listen_user_input.user_identified_key == listen_game_state.song_key
    )

    websocket.send(listen_game_state.model_dump_json())

    return listen_game_state
