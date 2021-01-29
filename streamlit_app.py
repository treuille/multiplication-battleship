import streamlit as st
import random
from typing import Set, Tuple

Ships = Set[Tuple[int, int]]

def get_settings():
    """Gets some settings for the board."""
    board_size = st.sidebar.number_input("Board size", 5, 20, 10)
    return board_size


def add_ship(length: int, ships: Ships) -> Ships:
    """Adds a ship of the specified length to the board."""


def write_board(ships: Ships, board_size: int) -> None:
    """Writes out the board to the Streamlit console."""
    st.text("\n".join(
        " ".join("X" if (x, y) in ships else "."
            for x in range(board_size))
        for y in range(board_size)))


def main():
    """Execution starts here."""
    st.write("# Battleship")
    board_size = get_settings()
    st.write("board size", board_size)

    s : Ships = set([(1, 1), (2, 1)])
    st.write(s)
    write_board(s, board_size)


if __name__ == "__main__":
    main()
