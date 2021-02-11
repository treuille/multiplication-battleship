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


state = st.beta_session_state(initialized=False)


def initialize_state(board_size: int, num_ships: int) -> None:
    """Setup a clean state of the board."""
    state.board_size: int = board_size
    state.num_ships: int = num_ships
    state.guesses: Points = set()
    state.current_guess: Optional[Point] = None
    create_new_random_board()
    state.initialized = True


def guess_is_correct(product_guess):
    """Returns true if the guessed product is correct."""
    return (product_guess ==
            str(state.current_guess[0] * state.current_guess[1]))


#############
# Callbacks #
#############


def reinitialize_state(*_):
    """Callback to reset the state."""
    state.initialized = False


def click_cell(point: Point) -> None:
    """Returns a callback for when the specified cell is clicked."""
    def cell_clicked():
        state.current_guess = point
    return cell_clicked


def product_guessed(product_guess):
    """Callback when the user makes a guess as to the product."""
    if guess_is_correct(product_guess):
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
    st.sidebar.write(f"{len(state.ships - state.guesses)} remaining")


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
    if guessed_everything:
        # Reveal every point on the board
        revealed = {(i, j) for i in range(1, state.board_size + 1)
                for j in range(1, state.board_size + 1)}
    else:
        revealed = state.guesses

    for y in range(1, state.board_size + 1):
     row = st.beta_columns(state.board_size)
     for x, cell in zip(range(1, state.board_size + 1), row):
         point = (x, y)
         if point not in revealed:
             cell.button(f"{x}x{y}", on_click=click_cell(point))
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
    st.sidebar.warning(f"❓ What is {product_str}?")
    product_guess = st.sidebar.text_input(product_str,
        on_change=product_guessed)
    if product_guess and not guess_is_correct(product_guess):
       st.sidebar.error(f"🥺 {product_guess} is not correct")


def main():
    """Execution starts here."""

    BUTTON_1 = "b1"
    BUTTON_2 = "b2"
    NUMBER_INPUT = "number_input"

    if st_event.changed(BUTTON_1):
        st.warning(f"{BUTTON_1} : {st_event.value()}")
    if st_event.changed(BUTTON_2):
        st.warning(f"{BUTTON_2} : {st_event.value()}")
    if st_event.changed(NUMBER_INPUT):
        st.info(f"{NUMBER_INPUT} : {st_event.value()}")
    
    st_event.button(BUTTON_1)
    st_event.button(BUTTON_2)
    st_event.number_input(NUMBER_INPUT)

    if st_event.changed(BUTTON_1):
        st.warning(BUTTON_1)
    if st_event.changed(BUTTON_2):
        st.warning(BUTTON_2)
    if st_event.changed(NUMBER_INPUT):
        st.info(f"{NUMBER_INPUT} : {st_event.value()}")

    return
    # Title
    st.write("# Alta Vista Multiplication Battleship")

    # Control parameters
    BOARD_SIZE_INPUT = "Board size"
    with st.sidebar:
        board_size = st_event.number_input(BOARD_SIZE_INPUT, 5, 20, 9,
                key=BOARD_SIZE_INPUT)
        num_ships = st.sidebar.number_input("Number of ships", 1, 10, 5,
                on_change=reinitialize_state)

    # Intializing the state here. I find doing this here very awkward.
    if not state.initialized:
        initialize_state(board_size, num_ships)

    # Write the number of points remaining
    write_remaining_points()

    # Reset button. The logic is all screwy here!
    st.sidebar.button("Reset", on_click=reinitialize_state)

    # This is just for debug purposes.
    # write_board()

    # Now draw the main UI
    draw_board()
    ask_for_answer()


if __name__ == "__main__":
    main()
