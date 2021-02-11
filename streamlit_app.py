import streamlit as st
import random
from typing import Set, Tuple
from streamlit.session_state import SessionState

# This package simulates an alternative event model
import st_event

#########
# Types #
#########


Point = Tuple[int, int]
Points = Set[Point]


#########
# State #
#########

# I like how in this version we don't neet to set an initialized flag
state = st.beta_session_state()


def initialize_state(board_size: int, num_ships: int) -> None:
    """Setup a clean state of the board."""
    state.board_size: int = board_size
    state.num_ships: int = num_ships
    state.guesses: Points = set()
    state.current_guess: Optional[Point] = None
    create_new_random_board()


def guess_is_correct(product_guess):
    """Returns true if the guessed product is correct."""
    return (product_guess ==
            str(state.current_guess[0] * state.current_guess[1]))


###########
# Signals #
###########

# When we need to reset the game state
RESET_STATE = "reset state"

# When one of the buttons has been clicked
CELL_CLICKED = "cell clicked"

# When the user has guessed the answer
GUESSED_ANSWER = "guesssed answer"

def handle_signals():
    if st_event.signal(CELL_CLICKED):
        state.current_guess = st_event.context()
    elif st_event.signal(GUESSED_ANSWER) and guess_is_correct(st_event.value()):
        if state.current_guess in state.ships:
            st.balloons()
        state.guesses.add(state.current_guess)
        state.current_guess = None


#########
# Board #
#########


def create_new_random_board() -> None:
    """Adds a new random board to the state."""
    ships = set()
    for ship_len in range(1, state.num_ships + 1):
        ships = add_ship(ship_len, ships, state.board_size)
    state.ships = ships


def add_ship(ship_len: int, ships: Points, board_size) -> Points:
    """Adds a ship of the specified length to the board."""
    MAX_ITER = 100

    # Stop trying to add the ship if it takes more than
    # MAX_ITER attempts to find a valid location
    for _ in range(MAX_ITER):
        pos_1 = random.randrange(1, board_size - ship_len + 1)
        pos_2 = random.randrange(1, board_size + 1)
        horizontal = bool(random.randint(0, 1))
        if horizontal:
            new_ship = {(pos_1 + i, pos_2) for i in range(ship_len)}
        else:
            new_ship = {(pos_2, pos_1 + i) for i in range(ship_len)}
        if ships.isdisjoint(new_ship):
            return ships.union(new_ship)
    raise RuntimeError(f"Unable to place ship after {MAX_ITER} iterations.")


##############
# Main Logic #
##############


def write_remaining_points() -> None:
    """Write down the number of ships remining."""
    # if hasattr(state, "ships") and hasattr(state, "guesses"):
    st.write(f"{len(state.ships - state.guesses)} remaining")


def write_board() -> None:
    """Writes out the board to the Streamlit console."""
    st.sidebar.text("\n".join(
        " ".join("X" if (x, y) in state.ships else "."
            for x in range(1, state.board_size + 1))
        for y in range(1, state.board_size + 1)))
        

def draw_board() -> None:
    """Writes out the board to the Streamlit console."""
    # First see if the whole board has been guesesed 
    guessed_everything = state.ships <= state.guesses

    for y in range(1, state.board_size + 1):
        row = st.beta_columns(state.board_size)
        for x, cell in zip(range(1, state.board_size + 1), row):
            point = (x, y)
            if (not guessed_everything) and (point not in state.guesses):
                with cell:
                    st_event.button(f"{x}x{y}", signal=CELL_CLICKED, 
                            context=point)
            elif point in state.ships:
                cell.write("🔥")
            else:
                cell.write("🌊")

    if guessed_everything:
            st.success("Great job!")


def ask_for_answer() -> None:
    """Prompt the user for the answer to the multiplication problem."""
    if state.current_guess == None:
        return

    product_str = f"{state.current_guess[0]}X{state.current_guess[1]}"
    with st.sidebar:
        st.warning(f"❓ What is {product_str}?")
        product_guess = st_event.text_input(product_str, signal=GUESSED_ANSWER)
        if product_guess and not guess_is_correct(product_guess):
           st.error(f"🥺 {product_guess} is not correct")


def main():
    """Execution starts here."""
    # Title
    st.write("# Alta Vista Multiplication Battleship")

    # Control parameters
    with st.sidebar:
        board_size = st_event.number_input("Board size", 5, 20, 9,
                signal=RESET_STATE)
        num_ships = st_event.number_input("Number of ships", 1, 10, 5,
                signal=RESET_STATE)

    # Reinitialize the state
    if st_event.no_signal() or st_event.signal(RESET_STATE):
        initialize_state(board_size, num_ships)

    # Draw the rest of the sidebar GUI
    with st.sidebar: 
        # Write the number of points remaining
        write_remaining_points()

        # Reset button. The logic is all screwy here!
        st_event.button("Reset", signal=RESET_STATE)

        # This is just for debug purposes.
        write_board()

    # Handle all signals except for RESET_STATE
    handle_signals()

    # Now draw the main UI
    draw_board()
    ask_for_answer()


if __name__ == "__main__":
    main()
