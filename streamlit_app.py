import streamlit as st
import random
from typing import Set, Tuple
from streamlit.session_state import SessionState

Ships = Set[Tuple[int, int]]

state = st.beta_session_state(board_size=None, num_ships=None, ships=None)

def board_size_changed(new_board_size):
    """Callback when the board size has changed."""
    st.write("The board size has changed:", new_board_size)
    if state.board_size != new_board_size:
        state.board_size = new_board_size
        if state.num_ships != None:
            create_new_random_board(state)
 
def num_ships_changed(new_num_ships):
    """Callback when the board size has changed."""
    st.write("The number of ships has changed:", new_num_ships)
    if state.num_ships != new_num_ships:
        state.num_ships = new_num_ships
        if state.board_size != None:
            create_new_random_board(state)

def get_settings():
    """Gets some settings for the board."""
    board_size = st.sidebar.number_input("Board size", 5, 20, 10,
            on_change=board_size_changed)
    num_ships = st.sidebar.number_input("Number of ships", 1, 10, 5)
    return board_size, num_ships

def create_new_random_board(state: SessionState) -> None:
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
    st.text("\n".join(
        " ".join("X" if (x, y) in ships else "."
            for x in range(board_size))
        for y in range(board_size)))


def main():
    """Execution starts here."""
    st.write("# Battleship")
    board_size, num_ships = get_settings()
    board_size_changed(board_size)
    num_ships_changed(num_ships)
    st.write(type(state), state)
    st.write("board size", board_size)
    write_board(state.ships, state.board_size)

if __name__ == "__main__":
    main()
