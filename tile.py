import lib.stddraw as stddraw  # used for drawing the tiles to display them
from lib.color import Color  # used for coloring the tiles
import random


# A class for modeling numbered tiles as in 2048
class Tile:
    # Class variables shared among all Tile objects
    # ---------------------------------------------------------------------------
    # the value of the boundary thickness (for the boxes around the tiles)
    boundary_thickness = 0.004
    # font family and font size used for displaying the tile number
    font_family, font_size = "Arial", 15

    # A constructor that creates a tile with 2 as the number on it
    def __init__(self):
        # set the number on this tile randomly to the 2 or 4
        self.number = random.choice([2, 4])
        # set the colors of this tile
        if self.number == 2:
            # if the number is 2, adjust the background
            self.background_color = Color(238, 228, 218)
        else:
            # if the number is 4, adjust the background
            self.background_color = Color(236, 224, 200)

        self.foreground_color = Color(0, 0, 0)  # foreground (number) color
        self.box_color = Color(141, 131, 121)  # box (boundary) color

    # a method to change color of the background
    def set_background_color(self, color):
        self.background_color = color

    # a method to change color of the foreground
    def set_foreground_color(self, color):
        self.foreground_color = color

    # A method for drawing this tile at a given position with a given length
    def draw(self, position, length=1):  # length defaults to 1
        # draw the tile as a filled square
        stddraw.setPenColor(self.background_color)
        stddraw.filledSquare(position.x, position.y, length / 2)
        # draw the bounding box around the tile as a square
        stddraw.setPenColor(self.box_color)
        stddraw.setPenRadius(Tile.boundary_thickness)
        stddraw.square(position.x, position.y, length / 2)
        stddraw.setPenRadius()  # reset the pen radius to its default value
        # draw the number on the tile
        stddraw.setPenColor(self.foreground_color)
        stddraw.setFontFamily(Tile.font_family)
        stddraw.setFontSize(Tile.font_size)
        stddraw.text(position.x, position.y, str(self.number))