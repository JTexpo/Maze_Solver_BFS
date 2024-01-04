import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")

import unittest
from maze_solver_bfs.maze_solver import (
    get_clear_board,
    find_maze_space,
    check_wasd,
    solve_maze,
)


class MazeSolver(unittest.TestCase):
    # get_blank_board
    # ---------------
    def test_get_clear_board(self):
        # Arrange
        board = [[0, 0], [0, 0]]

        # Act
        generated_board = get_clear_board(width=2, height=2)

        # Assert
        self.assertTrue(board[0][0] == generated_board[0][0])
        self.assertTrue(board[0][1] == generated_board[0][1])
        self.assertTrue(board[1][0] == generated_board[1][0])
        self.assertTrue(board[1][1] == generated_board[1][1])

    # find_maze_space
    # ---------------
    def test_find_maze_space(self):
        # Arrange
        board = [[0, 1], [0, 0]]

        # Act
        space_x, space_y = find_maze_space(maze=board, space_id=1)

        # Assert
        self.assertTrue(space_x == 1)
        self.assertTrue(space_y == 0)

    # check_wasd
    # ---------------
    def test_check_wasd(self):
        # Arrange
        board = get_clear_board(width=3, height=3)

        # Act
        north_check, south_check, east_check, west_check = check_wasd(
            maze=board, x_cord=1, y_cord=1
        )

        # Assert
        self.assertTrue(north_check == True)
        self.assertTrue(south_check == True)
        self.assertTrue(east_check == True)
        self.assertTrue(west_check == True)

    def test_check_wasd_corner_top_left(self):
        # Arrange
        board = get_clear_board(width=3, height=3)

        # Act
        north_check, south_check, east_check, west_check = check_wasd(
            maze=board, x_cord=0, y_cord=0
        )

        # Assert
        self.assertTrue(north_check == False)
        self.assertTrue(south_check == True)
        self.assertTrue(east_check == True)
        self.assertTrue(west_check == False)

    def test_check_wasd_corner_bottom_right(self):
        # Arrange
        board = get_clear_board(width=3, height=3)

        # Act
        north_check, south_check, east_check, west_check = check_wasd(
            maze=board, x_cord=2, y_cord=2
        )

        # Assert
        self.assertTrue(north_check == True)
        self.assertTrue(south_check == False)
        self.assertTrue(east_check == False)
        self.assertTrue(west_check == True)

    def test_check_wasd_trapped(self):
        # Arrange
        board = [[1, 1, 2], [1, 0, 4], [3, 1, 1]]

        # Act
        north_check, south_check, east_check, west_check = check_wasd(
            maze=board, x_cord=1, y_cord=1
        )

        # Assert
        self.assertTrue(north_check == False)
        self.assertTrue(south_check == False)
        self.assertTrue(east_check == False)
        self.assertTrue(west_check == False)

    def test_solve_maze(self):
        # Arrange
        board = [[0, 1, 0, 2], [0, 0, 0, 0], [0, 1, 0, 0], [3, 1, 0, 0]]

        # Act
        solved_maze = solve_maze(maze=board)[-1]

        # Assert
        expected = [[0, 1, 0, 2], [4, 4, 4, 4], [4, 1, 0, 0], [3, 1, 0, 0]]

        self.assertTrue(expected[0][0] == solved_maze[0][0])
        self.assertTrue(expected[0][1] == solved_maze[0][1])
        self.assertTrue(expected[0][2] == solved_maze[0][2])
        self.assertTrue(expected[0][3] == solved_maze[0][3])
        self.assertTrue(expected[1][0] == solved_maze[1][0])
        self.assertTrue(expected[1][1] == solved_maze[1][1])
        self.assertTrue(expected[1][2] == solved_maze[1][2])
        self.assertTrue(expected[1][3] == solved_maze[1][3])
        self.assertTrue(expected[2][0] == solved_maze[2][0])
        self.assertTrue(expected[2][1] == solved_maze[2][1])
        self.assertTrue(expected[2][2] == solved_maze[2][2])
        self.assertTrue(expected[2][3] == solved_maze[2][3])
        self.assertTrue(expected[3][0] == solved_maze[3][0])
        self.assertTrue(expected[3][1] == solved_maze[3][1])
        self.assertTrue(expected[3][2] == solved_maze[3][2])
        self.assertTrue(expected[3][3] == solved_maze[3][3])


if __name__ == "__main__":
    unittest.main()
