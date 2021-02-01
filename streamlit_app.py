import streamlit as st
import random
from typing import Set, Tuple
from streamlit.session_state import SessionState

Ships = Set[Tuple[int, int]]

state = st.beta_session_state(initialized=False)

def config_parameter_changed(*_):
    """Callback when board_size or num_ships has changed."""
    # Reset the state to 
    state.initialized = False

def initialize_state(board_size: int, num_ships: int) -> None:
    """Setup a clean state of the board."""
    state.board_size = board_size
    state.num_ships = num_ships
    create_new_random_board()
    state.initialized = True

def get_settings() -> Tuple[int, int]:
    """Gets some settings for the board."""
    board_size = st.sidebar.number_input("Board size", 5, 20, 10,
            on_change=config_parameter_changed)
    num_ships = st.sidebar.number_input("Number of ships", 1, 10, 5,
            on_change=config_parameter_changed)
    return board_size, num_ships

def create_new_random_board() -> None:
    """Adds a new random board to the state."""
    ships = set()
    for ship_len in range(1, state.num_ships + 1):
        ships = add_ship(ship_len, ships, state.board_size)
    state.ships = ships

def add_ship(ship_len: int, ships: Ships, board_size) -> Ships:
    """Adds a ship of the specified length to the board."""
    MAX_ITER = 100

    # Stop trying to add the ship if it takes more than
    # MAX_ITER attempts to find a valid location
    for _ in range(MAX_ITER):
        pos_1 = random.randrange(0, board_size - ship_len)
        pos_2 = random.randrange(0, board_size)
        horizontal = bool(random.randint(0, 1))
        if horizontal:
            new_ship = {(pos_1 + i, pos_2) for i in range(ship_len)}
        else:
            new_ship = {(pos_2, pos_1 + i) for i in range(ship_len)}
        if ships.isdisjoint(new_ship):
            return ships.union(new_ship)
    raise RuntimeError(f"Unable to place ship after {MAX_ITER} iterations.")

def write_board(ships: Ships, board_size: int) -> None:
    """Writes out the board to the Streamlit console."""
    st.sidebar.text("\n".join(
        " ".join("X" if (x, y) in ships else "."
            for x in range(board_size))
        for y in range(board_size)))

def click_cell(x: int, y:int) -> None:
    """Returns a callback for when the specified cell is clicked."""
    def cell_clicked():
        st.sidebar.info(f"Cell `{x}`x`{y}` clicked.")
    return cell_clicked

def draw_board(state: SessionState) -> None:
    """Writes out the board to the Streamlit console."""
    for y in range(1, state.board_size + 1):
        row = st.beta_columns(state.board_size)
        for x, cell in zip(range(1, state.board_size + 1), row):
            cell.button(f"{x}x{y}", on_click=click_cell(x, y))

def main():
    """Execution starts here."""
    st.write("# Battleship")
    board_size, num_ships = get_settings()
    if not state.initialized:
        initialize_state(board_size, num_ships)
    write_board(state.ships, state.board_size)
    draw_board(state)

if __name__ == "__main__":
    main()
