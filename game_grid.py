import lib.stddraw as stddraw  # used for displaying the game grid
from lib.color import Color  # used for coloring the game grid
from point import Point  # used for tile positions
import numpy as np  # fundamental Python module for scientific computing


# A class for modeling the game grid
class GameGrid:

    # A constructor for creating the game grid based on the given arguments
    def __init__(self, grid_h, grid_w):
        # set the dimensions of the game grid as the given arguments
        self.grid_height = grid_h
        self.grid_width = grid_w
        # create a tile matrix to store the tiles locked on the game grid
        self.tile_matrix = np.full((grid_h, grid_w), None)
        # create the tetromino that is currently being moved on the game grid
        self.current_tetromino = None
        # create the next tetromino to hold the next tetromino
        self.next_tetromino = None
        # the game_over flag shows whether the game is over or not
        self.game_over = False
        # set the color used for the empty grid cells
        self.empty_cell_color = Color(206, 195, 181)
        # set the colors used for the grid lines and the grid boundaries
        self.line_color = Color(187, 174, 161)
        self.boundary_color = Color(132, 122, 113)
        # thickness values used for the grid lines and the grid boundaries
        self.line_thickness = 0.002
        self.box_thickness = 10 * 0.001
        # score variable to hold the score
        self.score = 0

    # A method for displaying the game grid
    def display(self, speed=250):
        # clear the background to empty_cell_color
        stddraw.clear(self.empty_cell_color)
        # draw the game grid
        self.draw_grid()
        # draw the current/active tetromino if it is not None
        # (the case when the game grid is updated)
        if self.current_tetromino is not None:
            self.current_tetromino.draw()
        # draw a box around the game grid
        self.draw_boundaries()
        # draw the right panel
        self.draw_right_panel()
        # show the resulting drawing with a pause duration = 250 ms
        stddraw.show(speed)

    # A method for drawing the cells and the lines of the game grid
    def draw_grid(self):
        # for each cell of the game grid
        for row in range(self.grid_height):
            for col in range(self.grid_width):
                # if the current grid cell is occupied by a tile
                if self.tile_matrix[row][col] is not None:
                    # draw this tile
                    self.tile_matrix[row][col].draw(Point(col, row))
        # draw the inner lines of the game grid
        stddraw.setPenColor(self.line_color)
        stddraw.setPenRadius(self.line_thickness)
        # x and y ranges for the game grid
        start_x, end_x = -0.5, self.grid_width - 0.5
        start_y, end_y = -0.5, self.grid_height - 0.5
        for x in np.arange(start_x + 1, end_x, 1):  # vertical inner lines
            stddraw.line(x, start_y, x, end_y)
        for y in np.arange(start_y + 1, end_y, 1):  # horizontal inner lines
            stddraw.line(start_x, y, end_x, y)
        stddraw.setPenRadius()  # reset the pen radius to its default value

    # A method to draw right panel, that contains score, controls and next piece
    def draw_right_panel(self):
        # set pen color and draw the rectangle
        stddraw.setPenColor(Color(167, 160, 151))
        stddraw.filledRectangle(11.5, -0.5, 4, self.grid_height)

        # writing the next and the score headers
        stddraw.setPenColor(Color(255, 255, 255))
        stddraw.setFontSize(35)
        stddraw.setFontFamily("Arial Bold")
        stddraw.text(13.5, 4.5, "NEXT")
        stddraw.text(13.5, 18, "SCORE")
        stddraw.setFontSize(40)
        stddraw.text(13.5, 17, str(self.score))

        # writing the instructions onto the the right panel
        stddraw.setFontSize(22)
        stddraw.setFontFamily("Arial")
        stddraw.text(13.5, 8.75, "Rotate = Space")
        stddraw.text(13.5, 9.5, "Hard Drop = H")
        stddraw.text(13.5, 10.25, "Pause Menu = P")

        # drawing the next tetromino at the bottom right
        n = len(self.next_tetromino.tile_matrix)

        for row in range(n):
            for col in range(n):
                if self.next_tetromino.tile_matrix[row][col] is not None:
                    # getting the position of the cell
                    position = self.get_right_cell_position(row, col)
                    # drawing it
                    self.next_tetromino.tile_matrix[row][col].draw(position)

    # A method to get the position of the next tetromino to draw it
    def get_right_cell_position(self, row, col):
        n = len(self.tile_matrix)  # n = number of rows = number of columns
        position = Point()
        # horizontal position of the cell
        position.x = 12.75 + col
        # vertical position of the cell
        position.y = 3.5 - row
        return position

    # A method for drawing the boundaries around the game grid
    def draw_boundaries(self):
        # draw a bounding box around the game grid as a rectangle
        stddraw.setPenColor(self.boundary_color)  # using boundary_color
        # set the pen radius as box_thickness (half of this thickness is visible
        # for the bounding box as its lines lie on the boundaries of the canvas)
        stddraw.setPenRadius(self.box_thickness)
        # the coordinates of the bottom left corner of the game grid
        pos_x, pos_y = -0.5, -0.5
        stddraw.rectangle(pos_x, pos_y, self.grid_width, self.grid_height)
        stddraw.setPenRadius()  # reset the pen radius to its default value

    # A method used checking whether the grid cell with the given row and column
    # indexes is occupied by a tile or not (i.e., empty)
    def is_occupied(self, row, col):
        # considering the newly entered tetrominoes to the game grid that may
        # have tiles with position.y >= grid_height
        if not self.is_inside(row, col):
            return False  # the cell is not occupied as it is outside the grid
        # the cell is occupied by a tile if it is not None
        return self.tile_matrix[row][col] is not None

    # A method for checking whether the cell with the given row and col indexes
    # is inside the game grid or not
    def is_inside(self, row, col):
        if row < 0 or row >= self.grid_height:
            return False
        if col < 0 or col >= self.grid_width:
            return False
        return True

    # A method that locks the tiles of a landed tetromino on the grid checking
    # if the game is over due to having any tile above the topmost grid row.
    # (This method returns True when the game is over and False otherwise.)
    def update_grid(self, tiles_to_lock, blc_position):
        # necessary for the display method to stop displaying the tetromino
        self.current_tetromino = None
        # lock the tiles of the current tetromino (tiles_to_lock) on the grid
        n_rows, n_cols = len(tiles_to_lock), len(tiles_to_lock[0])
        for col in range(n_cols):
            for row in range(n_rows):
                # place each tile (occupied cell) onto the game grid
                if tiles_to_lock[row][col] is not None:
                    # compute the position of the tile on the game grid
                    pos = Point()
                    pos.x = blc_position.x + col
                    pos.y = blc_position.y + (n_rows - 1) - row
                    if self.is_inside(pos.y, pos.x):
                        self.tile_matrix[pos.y][pos.x] = tiles_to_lock[row][col]
                    # the game is over if any placed tile is above the game grid
                    else:
                        self.game_over = True
        # return the value of the game_over flag
        return self.game_over

    # A method to clear full rows
    def clear_rows(self):
        rows_to_clear = []

        # Check for full rows and add them to rows_to_clear
        for row in range(self.grid_height):
            if all(self.tile_matrix[row]):
                rows_to_clear.append(row)

        # Clear full rows and add their sum to the score
        for row in rows_to_clear:
            row_sum = sum(tile.number for tile in self.tile_matrix[row])
            self.score += row_sum
            self.tile_matrix[row] = [None] * self.grid_width  # Clear the row

            for col in range(self.grid_width):
                for r in range(row, self.grid_height - 1):
                    # drop the tiles
                    self.tile_matrix[r][col] = self.tile_matrix[r + 1][col]

    # A method to merge tiles vertically on the game grid and update the score
    def merge_tiles(self):
        # looping through the whole array
        for col in range(self.grid_width):
            for row in range(self.grid_height - 1):
                # if the current and tile above it not none
                if self.tile_matrix[row][col] is not None and self.tile_matrix[row + 1][col] is not None:
                    # if the current and tile above is equal
                    if self.tile_matrix[row][col].number == self.tile_matrix[row + 1][col].number:
                        # Merge the tiles
                        self.tile_matrix[row][col].number *= 2
                        # Make the above tile none
                        self.tile_matrix[row + 1][col] = None
                        # a loop to drop the tiles above the merging
                        for r in range(row + 1, self.grid_height - 1):
                            if self.tile_matrix[r][col] is None and self.tile_matrix[r + 1][col] is not None:
                                self.tile_matrix[r][col] = self.tile_matrix[r + 1][col]
                                self.tile_matrix[r + 1][col] = None

                        merged_tile_num = self.tile_matrix[row][col].number
                        # updating the background and foreground colors based on the number
                        if merged_tile_num == 4:
                            self.tile_matrix[row][col].set_background_color(Color(236, 224, 200))
                        elif merged_tile_num == 8:
                            self.tile_matrix[row][col].set_background_color(Color(243, 177, 121))
                            self.tile_matrix[row][col].set_foreground_color(Color(255, 255, 255))
                        elif merged_tile_num == 16:
                            self.tile_matrix[row][col].set_background_color(Color(245, 149, 99))
                            self.tile_matrix[row][col].set_foreground_color(Color(255, 255, 255))
                        elif merged_tile_num == 32:
                            self.tile_matrix[row][col].set_background_color(Color(249, 123, 98))
                            self.tile_matrix[row][col].set_foreground_color(Color(255, 255, 255))
                        elif merged_tile_num == 64:
                            self.tile_matrix[row][col].set_background_color(Color(246, 93, 59))
                            self.tile_matrix[row][col].set_foreground_color(Color(255, 255, 255))
                        elif merged_tile_num == 128:
                            self.tile_matrix[row][col].set_background_color(Color(238, 203, 102))
                            self.tile_matrix[row][col].set_foreground_color(Color(255, 255, 255))
                        elif merged_tile_num == 256:
                            self.tile_matrix[row][col].set_background_color(Color(237, 204, 99))
                            self.tile_matrix[row][col].set_foreground_color(Color(255, 255, 255))
                        elif merged_tile_num == 512:
                            self.tile_matrix[row][col].set_background_color(Color(239, 202, 88))
                            self.tile_matrix[row][col].set_foreground_color(Color(255, 255, 255))
                        elif merged_tile_num == 1024:
                            self.tile_matrix[row][col].set_background_color(Color(237, 198, 67))
                            self.tile_matrix[row][col].set_foreground_color(Color(255, 255, 255))
                        elif merged_tile_num == 2048:
                            self.tile_matrix[row][col].set_background_color(Color(237, 198, 67))
                            self.tile_matrix[row][col].set_foreground_color(Color(255, 255, 255))

                        # Update score
                        self.score += self.tile_matrix[row][col].number  # Example scoring mechanism


    def has_value(self,value):
        for col in range(self.grid_width):
            for row in range(self.grid_height - 1):
                if self.tile_matrix[row][col] is not None:
                    num = self.tile_matrix[row][col].number 
                    if num == value:
                        return True
        return False