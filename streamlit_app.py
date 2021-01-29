import streamlit as st
import random
from typing import Set, Tuple

Ships = Set[Tuple[int, int]]

def get_settings():
    """Gets some settings for the board."""
    board_size = st.sidebar.number_input("Board size", 5, 20, 10)
    num_ships = st.sidebar.number_input("Number of ships", 1, 10, 5)
    return board_size, num_ships


def add_ship(ship_len: int, ships: Ships, board_size) -> Ships:
    """Adds a ship of the specified length to the board."""
    MAX_ITER = 100

    # Stop trying to add the ship if it takes more than
    # MAX_ITER attempts to find a valid location
    for _ in range(MAX_ITER):
        start_pos_1 = random.randrange(0, board_size - ship_len)
        start_pos_2 = random.randrange(0, board_size)
        horizontal = bool(random.randint(0, 1))
        new_ship : Ships = set()
        for i in range(ship_len):
            if horizontal:
                i, j = start_pos_1 + i, start_pos_2
            else:
                j, i = start_pos_1 + i, start_pos_2
            new_ship.add((i, j))
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
    st.write("board size", board_size)

    ships : Ships = set()
    st.write(ships)
    write_board(ships, board_size)
    for ship_len in range(1, num_ships + 1):
        ships = add_ship(ship_len, ships, board_size)
        write_board(ships, board_size)

if __name__ == "__main__":
    main()
