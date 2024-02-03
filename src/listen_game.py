from schemas import ListenUserInput, ListenGameState


def new_listen_state(listen_game_init):
    state = ListenGameState(song_name="test", song_bytes=b"")
    return state


def handle_listen_input(listen_user_input, listen_game_state):
    pass
