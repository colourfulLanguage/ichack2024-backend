from schemas import SingUserInput, SingGameState


def new_sing_state(sing_game_init):
    state = SingGameState(actual_key="C", user_audio_key=b"")
    return state


def handle_sing_input(sing_user_input, sing_game_state):
    pass
