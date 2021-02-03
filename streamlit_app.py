import streamlit as st
import random
from typing import Set, Tuple
from streamlit.session_state import SessionState

Point = Tuple[int, int]
Points = Set[Point]

# What I'm trying to do here is have the state reset if either the board
# size of number of ships changed. In order to do so, I've added this
# initialized flag to the state which feels awkward.

# It feels awkward to me that I 
def config_parameter_changed(*_):
    """Callback when board_size or num_ships has changed."""
    # Reset the state to 
    state.initialized = False

def initialize_state(board_size: int, num_ships: int) -> None:
    """Setup a clean state of the board."""
    state.board_size: int = board_size
    state.num_ships: int = num_ships
    state.guesses: Points = set()
    state.current_guess: Optional[Point] = None
    create_new_random_board()
    state.initialized = True

def create_new_random_board() -> None:
    """Adds a new random board to the state."""
    ships = set()
    for ship_len in range(1, state.num_ships + 1):
        ships = add_ship(ship_len, ships, state.board_size)
    state.ships = ships

state = st.beta_session_state(initialized=False)

def get_settings() -> Tuple[int, int]:
    """Gets some settings for the board."""
    return board_size, num_ships


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

def write_board(ships: Points, board_size: int) -> None:
    """Writes out the board to the Streamlit console."""
    st.sidebar.text("\n".join(
        " ".join("X" if (x, y) in ships else "."
            for x in range(1, board_size + 1))
        for y in range(1, board_size + 1)))

def click_cell(point: Point) -> None:
    """Returns a callback for when the specified cell is clicked."""
    def cell_clicked():
        state.current_guess = point
    return cell_clicked

def draw_board(state: SessionState) -> None:
 """Writes out the board to the Streamlit console."""
 for y in range(1, state.board_size + 1):
     row = st.beta_columns(state.board_size)
     for x, cell in zip(range(1, state.board_size + 1), row):
         point = (x, y)
         if point not in state.guesses:
             cell.button(f"{x}x{y}", on_click=click_cell(point))
         elif point in state.ships:
             cell.write("🔥")
         else:
             cell.write("🌊")

def ask_for_answer() -> None:
    """Prompt the user for the answer to the multiplication problem."""
    if state.current_guess == None:
        return
    product_str = f"{state.current_guess[0]}X{state.current_guess[1]}"
    st.info(f"What is {product_str}?")
    guess = st.text_input(product_str)
    if not guess:
        return
    if guess == str(state.current_guess[0] * state.current_guess[1]):
        if state.current_guess in state.ships:
            st.balloons()
        st.success(f"{guess} is correct!")
        state.guesses.add(state.current_guess)
        state.current_guess = None

def main():
    """Execution starts here."""
    st.write("# Battleship")

    board_size = st.sidebar.number_input("Board size", 5, 20, 10,
            on_change=config_parameter_changed)
    num_ships = st.sidebar.number_input("Number of ships", 1, 10, 5,
            on_change=config_parameter_changed)
    if not state.initialized:
        initialize_state(board_size, num_ships)

    write_board(state.ships, state.board_size)
    draw_board(state)
    ask_for_answer()

if __name__ == "__main__":
    main()
