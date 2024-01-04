from typing import List, Tuple
from copy import deepcopy

BLANK_SPACE_ID = 0
WALL_SPACE_ID = 1
START_SPACE_ID = 2
END_SPACE_ID = 3
SOLUTION_SPACE_ID = 4

PREV_UP_ID = -1
PREV_DOWN_ID = -2
PREV_LEFT_ID = -3
PREV_RIGHT_ID = -4


def get_clear_board(width: int, height: int) -> List[List[int]]:
    """
    Return a clear board with the specified width and height.

    Parameters:
        width (int): The width of the board.
        height (int): The height of the board.

    Returns:
        List[List[int]]: A 2D list representing the clear board.
    """
    return [[0 for _ in range(width)] for _ in range(height)]


def find_maze_space(maze: List[List[int]], space_id: int) -> Tuple[int, int]:
    """
    Find the first occurrence of a given space id in a maze and return its coordinates.

    Parameters:
        maze (List[List[int]]): A 2D list representing a maze where each element is an integer representing a space.
        space_id (int): The id of the space to search for.

    Returns:
        Tuple[int, int]: A tuple containing the x and y coordinates of the first occurrence of the space_id in the maze.
    """
    for y in range(len(maze)):
        for x in range(len(maze[y])):
            if maze[y][x] == space_id:
                return x, y
    return -1, -1


def check_wasd(
    maze: List[List[int]],
    x_cord: int,
    y_cord: int,
    valid_ids: List[int] = [BLANK_SPACE_ID, END_SPACE_ID],
) -> tuple[bool, bool, bool, bool]:
    """
    Check the surrounding cells of a given coordinate in the maze.

    Args:
        maze (List[List[int]]): The maze represented as a 2D list of integers.
        x_cord (int): The x-coordinate of the cell to check.
        y_cord (int): The y-coordinate of the cell to check.
        valid_ids (List[int], optional): A list of valid IDs for the cells. Defaults to [BLANK_SPACE_ID, END_SPACE_ID].

    Returns:
        tuple[bool, bool, bool, bool]: A tuple of boolean values indicating if the north, south, east, and west cells are valid.
    """

    # NORTH
    # -----
    north_check = False if y_cord == 0 else (maze[y_cord - 1][x_cord] in valid_ids)

    # SOUTH
    # -----
    south_check = (
        False if y_cord == len(maze) - 1 else (maze[y_cord + 1][x_cord] in valid_ids)
    )

    # EAST
    # ----
    east_check = (
        False
        if x_cord == len(maze[y_cord]) - 1
        else (maze[y_cord][x_cord + 1] in valid_ids)
    )

    # WEST
    # ----
    west_check = False if x_cord == 0 else (maze[y_cord][x_cord - 1] in valid_ids)

    return north_check, south_check, east_check, west_check


def solve_maze(
    maze: List[List[int]],
    start_space_id: int = START_SPACE_ID,
    end_space_id: int = END_SPACE_ID,
    prev_up_id: int = PREV_UP_ID,
    prev_down_id: int = PREV_DOWN_ID,
    prev_left_id: int = PREV_LEFT_ID,
    prev_right_id: int = PREV_RIGHT_ID,
    history:bool=False,
) -> List[List[List[int]]]:
    """
    Solve a maze using a breadth-first search algorithm.

    Parameters:
    - maze: A 2D list representing the maze. Each element in the list is an integer representing a space in the maze.
    - start_space_id: An optional integer representing the ID of the start space in the maze. Defaults to START_SPACE_ID.
    - end_space_id: An optional integer representing the ID of the end space in the maze. Defaults to END_SPACE_ID.
    - prev_up_id: An optional integer representing the ID of the previous space when moving up. Defaults to PREV_UP_ID.
    - prev_down_id: An optional integer representing the ID of the previous space when moving down. Defaults to PREV_DOWN_ID.
    - prev_left_id: An optional integer representing the ID of the previous space when moving left. Defaults to PREV_LEFT_ID.
    - prev_right_id: An optional integer representing the ID of the previous space when moving right. Defaults to PREV_RIGHT_ID.
    - history: An optional boolean indicating whether to keep track of the maze history during the search. Defaults to False.

    Returns:
    - history_maze: A list of 2D lists representing the maze at each step of the search. If a solution is found, the final maze with the path from start to end will be included.

    """
    # Initalizations
    # --------------
    start_x, start_y = find_maze_space(maze, start_space_id)
    end_x, end_y = find_maze_space(maze, end_space_id)

    # if the board is missing a start or end space, return an empty list
    if start_x == -1 or start_y == -1 or end_x == -1 or end_y == -1:
        return [maze]

    queue_tiles = [{"x": start_x, "y": start_y}]
    winning_tile = {}
    active_maze = deepcopy(maze)
    solved_maze = deepcopy(maze)
    history_maze = []

    # Breadth First Search
    # --------------------
    while queue_tiles and not winning_tile:
        # creating a queue for the next wave of nodes to be apart of
        next_queue = []

        # Preserving the maze if requested
        if history:
            history_maze.append(deepcopy(active_maze))

        # Itterating over all of the queue'd tiles to generate the next batch of movement
        for tile in queue_tiles:
            north_check, south_check, east_check, west_check = check_wasd(
                maze=active_maze, x_cord=tile["x"], y_cord=tile["y"]
            )
            # NOTE : This code was done origionally with pointers, but Python didn't seem to like that
            # It used to be a class consisting of the X , Y and Previous Node
            # This caused on larger maps for Python to consume large amounts of CPU holding onto many dead-end
            # nodes. To resolve this issue, I have the board getting marked with the path.
            # Think of this like leaving bread crumbs vs holding the hand of the person before and infront of you
            # This change was able to signifigantly increase the speed at which the Breadth First Search is able to preform
            
            # NORTH
            # -----
            if north_check:
                next_queue.append({"x": tile["x"], "y": tile["y"] - 1})
                if tile["x"] == end_x and tile["y"] - 1 == end_y:
                    winning_tile = deepcopy(tile)
                active_maze[tile["y"]-1][tile["x"]] = prev_down_id

            # SOUTH
            # -----
            if south_check:
                next_queue.append({"x": tile["x"], "y": tile["y"] + 1})
                if tile["x"] == end_x and tile["y"] + 1 == end_y:
                    winning_tile = deepcopy(tile)
                active_maze[tile["y"]+1][tile["x"]] = prev_up_id

            # EAST
            # ----
            if east_check:
                next_queue.append({"x": tile["x"] + 1, "y": tile["y"]})
                if tile["x"] + 1 == end_x and tile["y"] == end_y:
                    winning_tile = deepcopy(tile)
                active_maze[tile["y"]][tile["x"]+1] = prev_left_id
            
            # WEST
            # ----
            if west_check:
                next_queue.append({"x": tile["x"] - 1, "y": tile["y"]})
                if tile["x"] - 1 == end_x and tile["y"] == end_y:
                    winning_tile = deepcopy(tile)
                active_maze[tile["y"]][tile["x"]-1] = prev_right_id
        
        queue_tiles = deepcopy(next_queue)

    # This loop unwinds the winning path. Since we know what node got to the end, we look at which nodes got to that
    if winning_tile:
        current_tile_x, current_tile_y = winning_tile["x"], winning_tile["y"]
        while maze[current_tile_y][current_tile_x] != START_SPACE_ID:
            solved_maze[current_tile_y][current_tile_x] = SOLUTION_SPACE_ID
            if active_maze[current_tile_y][current_tile_x] == prev_up_id:
                current_tile_y -= 1
            elif active_maze[current_tile_y][current_tile_x] == prev_down_id:
                current_tile_y += 1
            elif active_maze[current_tile_y][current_tile_x] == prev_left_id:
                current_tile_x -= 1
            elif active_maze[current_tile_y][current_tile_x] == prev_right_id:
                current_tile_x += 1

        history_maze.append(deepcopy(solved_maze))

    return history_maze
