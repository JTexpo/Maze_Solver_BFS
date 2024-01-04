from typing import List
import asyncio
from copy import deepcopy

from js import document
from pyodide.ffi import create_proxy
import pyscript

from maze_solver_bfs.maze_solver import (
    BLANK_SPACE_ID,
    WALL_SPACE_ID,
    START_SPACE_ID,
    END_SPACE_ID,
    SOLUTION_SPACE_ID,
    PREV_DOWN_ID,
    PREV_LEFT_ID,
    PREV_RIGHT_ID,
    PREV_UP_ID,
    solve_maze,
    get_clear_board,
)

LINE_WIDTH = 5
SPACING = 10

board = get_clear_board(SPACING,SPACING)
solve_board = False

DRAW_MODE_KEY = 0
ERASE_MODE_KEY = 1
START_MODE_KEY = 2
END_MODE_KEY = 3

MODE = START_MODE_KEY

COLOUR_MAPPING = {
    BLANK_SPACE_ID: "white",
    WALL_SPACE_ID: "black",
    START_SPACE_ID: "green",
    END_SPACE_ID: "red",
    SOLUTION_SPACE_ID: "orange",
    PREV_DOWN_ID: "blue",
    PREV_RIGHT_ID: "blue",
    PREV_LEFT_ID: "blue",
    PREV_UP_ID: "blue",
}


def toggle_mode(mode: int):
    global MODE
    MODE = mode


def clear_board():
    global LINE_WIDTH, SPACING, board
    canvas = document.getElementById("maze")
    ctx = canvas.getContext("2d")

    ctx.fillStyle = "black"
    ctx.fillRect(0, 0, canvas.width, canvas.height)
    ctx.fillStyle = "white"
    ctx.fillRect(
        LINE_WIDTH,
        LINE_WIDTH,
        canvas.width - LINE_WIDTH * 2,
        canvas.height - LINE_WIDTH * 2,
    )

    ctx.fillStyle = "black"
    for index in range(1, SPACING):
        ctx.fillRect(
            index * (canvas.width / SPACING) - LINE_WIDTH,
            0,
            LINE_WIDTH * 2,
            canvas.height,
        )
        ctx.fillRect(
            0,
            index * (canvas.height / SPACING) - LINE_WIDTH,
            canvas.width,
            LINE_WIDTH * 2,
        )

    board = get_clear_board(SPACING, SPACING)


def draw_board(board: List[List[int]]):
    global LINE_WIDTH, SPACING, COLOUR_MAPPING

    canvas = document.getElementById("maze")
    ctx = canvas.getContext("2d")

    for y, row in enumerate(board):
        for x, value in enumerate(row):
            ctx.fillStyle = COLOUR_MAPPING[value]

            ctx.fillRect(
                x * (canvas.width / SPACING) + LINE_WIDTH,
                y * (canvas.height / SPACING) + LINE_WIDTH,
                canvas.width / SPACING - LINE_WIDTH * 2,
                canvas.height / SPACING - LINE_WIDTH * 2,
            )


def solve():
    global solve_board
    solve_board = True


async def main():
    global solve_board, board

    while True:
        if solve_board:
            solved_boards = solve_maze(maze=board, history=True)
            for board_step in solved_boards:
                draw_board(board_step)
                await asyncio.sleep(0.15)
            solve_board = False

        await asyncio.sleep(0.5)


def _on_click(element):
    global board, SPACING, MODE, DRAW_MODE_KEY, ERASE_MODE_KEY, START_MODE_KEY, END_MODE_KEY, BLANK_SPACE_ID, WALL_SPACE_ID, START_SPACE_ID, END_SPACE_ID

    canvas = document.getElementById("maze")
    
    # DRAW
    # ----
    if MODE == DRAW_MODE_KEY:
        board[int(element.offsetY // (canvas.width / SPACING))][
            int(element.offsetX // (canvas.width / SPACING))
        ] = WALL_SPACE_ID
    
    # ERASE
    # -----
    elif MODE == ERASE_MODE_KEY:
        board[int(element.offsetY // (canvas.width / SPACING))][
            int(element.offsetX // (canvas.width / SPACING))
        ] = BLANK_SPACE_ID
    
    # PLACE START
    # -----------
    elif MODE == START_MODE_KEY:
        for y_index, row in enumerate(board):
            for x_idnex, value in enumerate(row):
                if value == START_SPACE_ID:
                    board[y_index][x_idnex] = BLANK_SPACE_ID
        board[int(element.offsetY // (canvas.width / SPACING))][
            int(element.offsetX // (canvas.width / SPACING))
        ] = START_SPACE_ID

    # PLACE END
    # ---------
    elif MODE == END_MODE_KEY:
        for y_index, row in enumerate(board):
            for x_idnex, value in enumerate(row):
                if value == END_SPACE_ID:
                    board[y_index][x_idnex] = BLANK_SPACE_ID
        board[int(element.offsetY // (canvas.width / SPACING))][
            int(element.offsetX // (canvas.width / SPACING))
        ] = END_SPACE_ID

    draw_board(board)

clear_board()
board = [
    [START_SPACE_ID,WALL_SPACE_ID,BLANK_SPACE_ID,BLANK_SPACE_ID,BLANK_SPACE_ID,BLANK_SPACE_ID,BLANK_SPACE_ID,WALL_SPACE_ID,BLANK_SPACE_ID,BLANK_SPACE_ID],
    [BLANK_SPACE_ID,WALL_SPACE_ID,WALL_SPACE_ID,BLANK_SPACE_ID,WALL_SPACE_ID,WALL_SPACE_ID,BLANK_SPACE_ID,BLANK_SPACE_ID,BLANK_SPACE_ID,WALL_SPACE_ID],
    [BLANK_SPACE_ID,BLANK_SPACE_ID,BLANK_SPACE_ID,BLANK_SPACE_ID,BLANK_SPACE_ID,WALL_SPACE_ID,WALL_SPACE_ID,WALL_SPACE_ID,BLANK_SPACE_ID,WALL_SPACE_ID],
    [WALL_SPACE_ID,WALL_SPACE_ID,WALL_SPACE_ID,WALL_SPACE_ID,BLANK_SPACE_ID,WALL_SPACE_ID,BLANK_SPACE_ID,BLANK_SPACE_ID,BLANK_SPACE_ID,WALL_SPACE_ID],
    [BLANK_SPACE_ID,WALL_SPACE_ID,BLANK_SPACE_ID,BLANK_SPACE_ID,BLANK_SPACE_ID,WALL_SPACE_ID,WALL_SPACE_ID,BLANK_SPACE_ID,WALL_SPACE_ID,WALL_SPACE_ID],
    [BLANK_SPACE_ID,BLANK_SPACE_ID,BLANK_SPACE_ID,WALL_SPACE_ID,WALL_SPACE_ID,WALL_SPACE_ID,BLANK_SPACE_ID,BLANK_SPACE_ID,WALL_SPACE_ID,BLANK_SPACE_ID],
    [BLANK_SPACE_ID,WALL_SPACE_ID,WALL_SPACE_ID,WALL_SPACE_ID,BLANK_SPACE_ID,WALL_SPACE_ID,WALL_SPACE_ID,WALL_SPACE_ID,WALL_SPACE_ID,BLANK_SPACE_ID],
    [BLANK_SPACE_ID,BLANK_SPACE_ID,BLANK_SPACE_ID,BLANK_SPACE_ID,BLANK_SPACE_ID,WALL_SPACE_ID,BLANK_SPACE_ID,BLANK_SPACE_ID,BLANK_SPACE_ID,BLANK_SPACE_ID],
    [WALL_SPACE_ID,WALL_SPACE_ID,BLANK_SPACE_ID,WALL_SPACE_ID,BLANK_SPACE_ID,BLANK_SPACE_ID,BLANK_SPACE_ID,WALL_SPACE_ID,BLANK_SPACE_ID,WALL_SPACE_ID],
    [BLANK_SPACE_ID,BLANK_SPACE_ID,BLANK_SPACE_ID,WALL_SPACE_ID,BLANK_SPACE_ID,WALL_SPACE_ID,WALL_SPACE_ID,WALL_SPACE_ID,BLANK_SPACE_ID,END_SPACE_ID],
]
draw_board(board)
on_click = create_proxy(_on_click)
document.getElementById("maze").addEventListener("mousedown", on_click)
pyscript.run_until_complete(main())
