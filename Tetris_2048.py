################################################################################
#                                                                              #
# The main program of Tetris 2048 Base Code                                    #
#                                                                              #
################################################################################

import lib.stddraw as stddraw  # for creating an animation with user interactions
from lib.picture import Picture  # used for displaying an image on the game menu
from lib.color import Color  # used for coloring the game menu
import os  # the os module is used for file and directory operations
from game_grid import GameGrid  # the class for modeling the game grid
from tetromino import Tetromino  # the class for modeling the tetrominoes
import random  # used for creating tetrominoes with random types (shapes)

is_paused = False
restart = False
speed_game = 250

# The main function where this program starts execution
def start():
    global is_paused
    global restart
    global score
    score = 0
    # set the dimensions of the game grid
    grid_h, grid_w = 20, 12
    # set the size of the drawing canvas (the displayed window)
    canvas_h, canvas_w = 40 * grid_h, 40 * grid_w + 110
    stddraw.setCanvasSize(canvas_w, canvas_h)
    # set the scale of the coordinate system for the drawing canvas
    stddraw.setXscale(-0.5, grid_w - 0.5 + 4)
    stddraw.setYscale(-0.5, grid_h - 0.5)

    # set the game grid dimension values stored and used in the Tetromino class
    Tetromino.grid_height = grid_h
    Tetromino.grid_width = grid_w
    # create the game grid
    grid = GameGrid(grid_h, grid_w)
    # create the first tetromino to enter the game grid
    # by using the create_tetromino function defined below
    current_tetromino = create_tetromino()
    grid.current_tetromino = current_tetromino
    next_tetromino = create_tetromino()
    grid.next_tetromino = next_tetromino

    # display a simple menu before opening the game
    # by using the display_game_menu function defined below
    display_game_menu(grid_h, grid_w)

    # the main game loop
    while True:
        # check for any user interaction via the keyboard
        if restart:
            is_paused = False
            restart = False
            # Restart and remake ol the necessary variables 0 or starting position
            score = 0
            # continue with the game setup as before
            Tetromino.grid_height = grid_h
            Tetromino.grid_width = grid_w
            grid = GameGrid(grid_h, grid_w)
            current_tetromino = create_tetromino()
            grid.current_tetromino = current_tetromino
            next_tetromino = create_tetromino()
            grid.next_tetromino = next_tetromino
            display_game_menu(grid_h, grid_w)

        if stddraw.hasNextKeyTyped():  # check if the user has pressed a key
            key_typed = stddraw.nextKeyTyped()
            if key_typed == "p":
                is_paused = True
                print("stopped")
                display_game_menu(grid_h, grid_w)
                # if the left arrow key has been pressed
            elif key_typed == "left":
                # move the active tetromino left by one
                current_tetromino.move(key_typed, grid, False)
            # if the right arrow key hahs been pressed
            elif key_typed == "right":
                # move the active tetromino right by one
                current_tetromino.move(key_typed, grid, False)
            # if the down arrow key has been pressed
            elif key_typed == "down":
                # move the active tetromino down by one
                # (soft drop: causes the tetromino to fall down faster)
                current_tetromino.move(key_typed, grid, False)
            elif key_typed == "space":
                current_tetromino.rotate_clockwise(grid)
            elif key_typed == "h":
                current_tetromino.move("h", grid, True)
            # clear the queue of the pressed keys for a smoother interaction
            stddraw.clearKeysTyped()

        # move the active tetromino down by one at each iteration (auto fall)
        success = current_tetromino.move("down", grid, False)

        # lock the active tetromino onto the grid when it cannot go down anymore
        if not success:
            # get the tile matrix of the tetromino without empty rows and columns
            # and the position of the bottom left cell in this matrix
            tiles, pos = current_tetromino.get_min_bounded_tile_matrix(True)
            # update the game grid by locking the tiles of the landed tetromino
            game_over = grid.update_grid(tiles, pos)
            # end the main game loop if the game is over
            if game_over:
                break
            # create the next tetromino to enter the game grid
            # by using the create_tetromino function defined below
            current_tetromino = next_tetromino
            grid.current_tetromino = next_tetromino
            next_tetromino = create_tetromino()
            grid.next_tetromino = next_tetromino

        # display the game grid with the current tetromino
        if not is_paused or not restart:

            grid.display(speed_game)

        grid.merge_tiles()
        grid.clear_rows()

    # print a message on the console when the game is over
    print("Game over")


# A function for creating random shaped tetrominoes to enter the game grid
def create_tetromino():
    # the type (shape) of the tetromino is determined randomly
    tetromino_types = ['I', 'O', 'Z', 'J', 'L', 'S', 'T']
    random_index = random.randint(0, len(tetromino_types) - 1)
    random_type = tetromino_types[random_index]
    # create and return the tetromino
    tetromino = Tetromino(random_type)
    return tetromino


def pause_menu(grid_height, grid_width):
    background_color = Color(42, 69, 99)
    img_center_x, img_center_y = (grid_width + 3) / 2, grid_height - 7
    button_color = Color(25, 255, 228)
    text_color = Color(7, 5, 5)
    button_w, button_h = grid_width - 1.5, 2

    stddraw.setPenColor(button_color)
    button2_blc_x, button2_blc_y = img_center_x - button_w / 2, 1
    button_blc_x, button_blc_y = img_center_x - button_w / 2, 4

    stddraw.setPenColor(background_color)
    stddraw.filledRectangle(button_blc_x, button_blc_y, button_w, button_h)
    stddraw.setPenColor(button_color)
    stddraw.filledRectangle(button_blc_x, button_blc_y - 3, button_w, button_h)
    stddraw.filledRectangle(button_blc_x, button_blc_y, button_w, button_h)
    stddraw.setFontFamily("Arial")
    stddraw.setFontSize(25)
    stddraw.setPenColor(text_color)

    text_to_display = "Restart"
    stddraw.text(img_center_x, 2, text_to_display)

    text1_to_display = "Continue"
    stddraw.text(img_center_x, 5, text1_to_display)


def speed_selection_page(grid_height,grid_width):
    global speed_game
    background_color = Color(42, 69, 99)
    button_color = Color(25, 255, 228)
    text_color = Color(7, 5, 5)

    img_center_x, img_center_y = (grid_width + 3) / 2, grid_height - 7
    button_w, button_h = grid_width - 1.5, 2
    button_blc_x, button_blc_y = img_center_x - button_w / 2, 4

    stddraw.setPenColor(background_color)
    stddraw.filledRectangle(button_blc_x, button_blc_y, button_w, button_h)


    img_center_x, img_center_y = (grid_width + 3) / 2, grid_height - 7
    button_w, button_h = grid_width -8, 2

    stddraw.setPenColor(button_color)
    button3_blc_x, button3_blc_y = img_center_x  - 5 - button_w / 2, 7
    button2_blc_x, button2_blc_y = img_center_x - button_w / 2, 7
    button_blc_x, button_blc_y = img_center_x +5 - button_w / 2, 7

    stddraw.filledRectangle(button3_blc_x, button3_blc_y, button_w, button_h)
    stddraw.filledRectangle(button2_blc_x, button2_blc_y, button_w, button_h)
    stddraw.filledRectangle(button_blc_x, button_blc_y, button_w, button_h)

    stddraw.setFontFamily("Arial")
    stddraw.setFontSize(25)
    stddraw.setPenColor(text_color)

    text_to_display = "Slow"
    stddraw.text(img_center_x - 5, 8, text_to_display)

    text1_to_display = "Medium"
    stddraw.text(img_center_x, 8, text1_to_display)

    text1_to_display = "Fast"
    stddraw.text(img_center_x + 5, 8, text1_to_display)

    while True:
        stddraw.show(50)

        if stddraw.mousePressed():
            mouse_x,mouse_y = stddraw.mouseX(), stddraw.mouseY()

            if mouse_x >= button_blc_x and mouse_x < button_blc_x + button_w:
                if mouse_y >= button_blc_y and mouse_y <= button_blc_y + button_h:
                    print("slow")
                    speed_game = 50
                    break

            if mouse_x >= button2_blc_x and mouse_x < button2_blc_x + button_w:
                if mouse_y >= button2_blc_y and mouse_y <= button2_blc_y + button_h:
                    print("slow")
                    speed_game = 250
                    break

            if mouse_x >= button3_blc_x and mouse_x < button3_blc_x + button_w:
                if mouse_y >= button3_blc_y and mouse_y <= button3_blc_y + button_h:
                    print("slow")
                    speed_game = 400
                    break
            


# A function for displaying a simple menu before starting the game
def display_game_menu(grid_height, grid_width):
    global is_paused
    global restart
    # the colors used for the menu
    background_color = Color(42, 69, 99)
    button_color = Color(25, 255, 228)
    text_color = Color(31, 160, 239)
    # clear the background drawing canvas to background_color
    stddraw.clear(background_color)
    # get the directory in which this python code file is placed
    current_dir = os.path.dirname(os.path.realpath(__file__))
    # compute the path of the image file
    img_file = current_dir + "/images/menu_image.png"
    # the coordinates to display the image centered horizontally
    img_center_x, img_center_y = (grid_width + 3) / 2, grid_height - 7
    # the image is modeled by using the Picture class
    image_to_display = Picture(img_file)
    # add the image to the drawing canvas
    stddraw.picture(image_to_display, img_center_x, img_center_y)
    # the dimensions for the start game button
    button_w, button_h = grid_width - 1.5, 2
    # the coordinates of the bottom left corner for the start game button
    button_blc_x, button_blc_y = img_center_x - button_w / 2, 4
    button2_blc_x, button2_blc_y = img_center_x - button_w / 2, 1
    # add the start game button as a filled rectangle
    stddraw.setPenColor(button_color)
    stddraw.filledRectangle(button_blc_x, button_blc_y, button_w, button_h)
    # add the text on the start game button
    stddraw.setFontFamily("Arial")
    stddraw.setFontSize(25)
    stddraw.setPenColor(text_color)
    text_to_display = "Click Here to Start the Game"
    stddraw.text(img_center_x, 5, text_to_display)
    # the user interaction loop for the simple menu

    if is_paused:
        pause_menu(grid_height, grid_width)

    while True:
        # display the menu and wait for a short time (50 ms)
        stddraw.show(50)

        # check if the mouse has been left-clicked on the start game button
        if stddraw.mousePressed():
            # get the coordinates of the most recent location at which the mouse
            # has been left-clicked
            mouse_x, mouse_y = stddraw.mouseX(), stddraw.mouseY()
            # check if these coordinates are inside the button
            if mouse_x >= button_blc_x and mouse_x <= button_blc_x + button_w:
                if mouse_y >= button_blc_y and mouse_y <= button_blc_y + button_h:
                    speed_selection_page(grid_height,grid_width)
                    break
                # Restart
                elif mouse_y >= button2_blc_y and mouse_y < button2_blc_y + button_h:
                    score = 0
                    restart = True
                    break


# start() function is specified as the entry point (main function) from which
# the program starts execution
if __name__ == '__main__':
    start()
