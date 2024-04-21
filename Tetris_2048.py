################################################################################
#                                                                              #
# The main program of Tetris 2048                                              #
#                                                                              #
################################################################################
import fileinput

import lib.stddraw as stddraw  # for creating an animation with user interactions
from lib.picture import Picture  # used for displaying an image on the game menu
from lib.color import Color  # used for coloring the game menu
import os  # the os module is used for file and directory operations
from game_grid import GameGrid  # the class for modeling the game grid
from tetromino import Tetromino  # the class for modeling the tetrominoes
import random  # used for creating tetrominoes with random types (shapes)

# setting the is_paused, restart and speed of the game
is_paused = False
restart = False
speed_game = 250


# The main function where this program starts execution
def start():
    # global is_paused, restart and score variables
    global is_paused
    global restart
    global score
    score = 0
    game_over = False
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
    grid.score = score
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
        # if the score
        if grid.score > 2048:
            condition = display_ending_menu(grid_h, grid_w, grid.score, "VICTORY!")
            if condition:
                is_paused = False
                restart = False
                current_tetromino, next_tetromino, grid = restart_the_grid(grid_h, grid_w, grid)
                display_game_menu(grid_h, grid_w)
                game_over = False
                stddraw.clearKeysTyped()
            else:
                exit()

        # if the game is over
        if game_over:
            # displaying the ending menu
            condition = display_ending_menu(grid_h, grid_w, grid.score, "GAME OVER!")
            # if the condition is true that means restart the game is true
            if condition:
                # restart the game procedures
                is_paused = False
                restart = False
                # restarting the grid
                current_tetromino, next_tetromino, grid = restart_the_grid(grid_h, grid_w, grid)
                # displaying the game menu
                display_game_menu(grid_h, grid_w)
                game_over = False
                stddraw.clearKeysTyped()
            else:
                # exit the game
                exit()
        # check if user paused the game and click restart
        if restart:
            # restart the game procedures
            is_paused = False
            restart = False
            # restarting the grid
            current_tetromino, next_tetromino, grid = restart_the_grid(grid_h, grid_w, grid)
            # displaying the game menu
            display_game_menu(grid_h, grid_w)
            stddraw.clearKeysTyped()

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

            # create the next tetromino to enter the game grid
            # by using the create_tetromino function defined below
            current_tetromino = next_tetromino
            grid.current_tetromino = next_tetromino
            next_tetromino = create_tetromino()
            grid.next_tetromino = next_tetromino

        # if it is not paused and not restart, display the grid
        if not is_paused or not restart:
            grid.display(speed_game)

        # merging the tiles
        grid.merge_tiles()
        # checking and clearing the full lines
        grid.clear_rows()


# A method to restart the grid
def restart_the_grid(grid_h, grid_w, grid):
    # Restart and remake ol the necessary variables 0 or starting position
    grid.score = 0
    # continue with the game setup as before
    Tetromino.grid_height = grid_h
    Tetromino.grid_width = grid_w
    grid = GameGrid(grid_h, grid_w)
    current_tetromino = create_tetromino()
    grid.current_tetromino = current_tetromino
    next_tetromino = create_tetromino()
    grid.next_tetromino = next_tetromino
    # return the elements
    return current_tetromino, next_tetromino, grid


# A function for creating random shaped tetrominoes to enter the game grid
def create_tetromino():
    # the type (shape) of the tetromino is determined randomly
    tetromino_types = ['I', 'O', 'Z', 'J', 'L', 'S', 'T']
    random_index = random.randint(0, len(tetromino_types) - 1)
    random_type = tetromino_types[random_index]
    # create and return the tetromino
    tetromino = Tetromino(random_type)
    return tetromino


# A method to show the pause menu
def pause_menu(grid_height, grid_width):
    # adjusting the colors and coordinates
    background_color = Color(42, 69, 99)
    img_center_x, img_center_y = (grid_width + 3) / 2, grid_height - 7
    button_color = Color(25, 255, 228)
    text_color = Color(7, 5, 5)
    button_w, button_h = grid_width - 1.5, 2

    stddraw.setPenColor(button_color)
    button_blc_x, button_blc_y = img_center_x - button_w / 2, 4

    # drawing the background and buttons
    stddraw.setPenColor(background_color)
    stddraw.filledRectangle(button_blc_x, button_blc_y, button_w, button_h)
    stddraw.setPenColor(button_color)
    stddraw.filledRectangle(button_blc_x, button_blc_y - 3, button_w, button_h)
    stddraw.filledRectangle(button_blc_x, button_blc_y, button_w, button_h)
    stddraw.setFontFamily("Arial")
    stddraw.setFontSize(25)
    stddraw.setPenColor(text_color)

    # writing the restart on the menu
    text_to_display = "Restart"
    stddraw.text(img_center_x, 2, text_to_display)

    # writing the continue on the menu
    text1_to_display = "Continue"
    stddraw.text(img_center_x, 5, text1_to_display)


# A method to select the speed of the game
def speed_selection_page(grid_height, grid_width):
    global speed_game
    # adjusting the colors and coordinates
    background_color = Color(42, 69, 99)
    button_color = Color(25, 255, 228)
    text_color = Color(7, 5, 5)

    img_center_x, img_center_y = (grid_width + 3) / 2, grid_height - 7
    button_w, button_h = grid_width - 1.5, 2
    button_blc_x, button_blc_y = img_center_x - button_w / 2, 4

    stddraw.setPenColor(background_color)
    stddraw.filledRectangle(button_blc_x, button_blc_y, button_w, button_h)

    img_center_x, img_center_y = (grid_width + 3) / 2, grid_height - 7
    button_w, button_h = grid_width - 8, 2

    # creating the buttons coordinates
    stddraw.setPenColor(button_color)
    button3_blc_x, button3_blc_y = img_center_x - 5 - button_w / 2, 7
    button2_blc_x, button2_blc_y = img_center_x - button_w / 2, 7
    button_blc_x, button_blc_y = img_center_x + 5 - button_w / 2, 7

    # drawing the buttons
    stddraw.filledRectangle(button3_blc_x, button3_blc_y, button_w, button_h)
    stddraw.filledRectangle(button2_blc_x, button2_blc_y, button_w, button_h)
    stddraw.filledRectangle(button_blc_x, button_blc_y, button_w, button_h)

    # setting the font and its size
    stddraw.setFontFamily("Arial")
    stddraw.setFontSize(25)
    stddraw.setPenColor(text_color)

    # displaying slow
    text_to_display = "Slow"
    stddraw.text(img_center_x - 5, 8, text_to_display)

    # displaying medium
    text1_to_display = "Medium"
    stddraw.text(img_center_x, 8, text1_to_display)

    # displaying fast
    text1_to_display = "Fast"
    stddraw.text(img_center_x + 5, 8, text1_to_display)

    # loop the check mouse interaction
    while True:
        # drawing the menu
        stddraw.show(50)

        # checking for the mouse interaction
        if stddraw.mousePressed():
            mouse_x, mouse_y = stddraw.mouseX(), stddraw.mouseY()

            if mouse_x >= button_blc_x and mouse_x < button_blc_x + button_w:
                # if the slow is clicked
                if mouse_y >= button_blc_y and mouse_y <= button_blc_y + button_h:
                    # adjusting the speed
                    speed_game = 50
                    break

            # if the medium is clicked
            if mouse_x >= button2_blc_x and mouse_x < button2_blc_x + button_w:
                if mouse_y >= button2_blc_y and mouse_y <= button2_blc_y + button_h:
                    speed_game = 250
                    # adjusting the speed
                    break

            # if the fast is clicked
            if mouse_x >= button3_blc_x and mouse_x < button3_blc_x + button_w:
                if mouse_y >= button3_blc_y and mouse_y <= button3_blc_y + button_h:
                    # adjusting the speed
                    speed_game = 400
                    break


# A method to update the highscores
def update_the_highscore(score):
    # adjusting the path of the highscores
    current_dir = os.path.dirname(os.path.realpath(__file__))
    scores_file = os.path.join(current_dir, "files", "high_scores.txt")

    # opening the file and reading it
    with open(scores_file, "r") as f:
        lines = [int(line.strip()) for line in f.readlines()]

    # a loop to find the position to write the score
    for i, line_score in enumerate(lines):
        # if the score is greater than the score in the file
        if score > line_score:
            # changing the score at current position
            lines.insert(i, score)
            break
    # if it is the lowest one append it
    else:
        lines.append(score)

    # writing to the file
    with open(scores_file, "w") as f:
        for line in lines:
            f.write(str(line) + "\n")


# A method to display the ending menu
def display_ending_menu(grid_height, grid_width, score, heading):
    background_color = Color(42, 69, 99)
    button_color = Color(25, 255, 228)
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
    # Restart the game rectangle
    stddraw.filledRectangle(button_blc_x, button_blc_y, button_w, button_h - 0.5)
    # Exit the game rectangle
    stddraw.filledRectangle(button_blc_x, button_blc_y - 2, button_w, button_h - 0.5)
    # HighScores rectangle
    stddraw.filledRectangle(button_blc_x, button_blc_y - 4, button_w, button_h - 0.5)
    # add the text on the start game button
    stddraw.setFontFamily("Arial BOLD")
    stddraw.setFontSize(50)
    text_to_display = heading
    # if the heading is VICTORY!
    if heading == "VICTORY!":
        stddraw.setPenColor(Color(255, 215, 0))
    else:
        # otherwise
        stddraw.setPenColor(Color(255, 0, 0))
    stddraw.text(img_center_x, 17.5, text_to_display)
    stddraw.setFontSize(30)
    stddraw.setPenColor(Color(255, 255, 255))
    text_to_display = "Your Score is " + str(score)
    # updating the highscore
    update_the_highscore(score)
    # drawing the score rectangle to display
    stddraw.rectangle(button_blc_x + 1.5, button_blc_y + 2.5, button_w - 3, button_h)
    stddraw.text(img_center_x, 7.5, text_to_display)
    stddraw.setPenColor(Color(0, 0, 0))
    stddraw.setFontSize(25)
    stddraw.setFontFamily("Arial")
    text_to_display = "Restart the Game"
    # writing "Restart the Game" into the rectangle
    stddraw.text(img_center_x, 4.75, text_to_display)
    text_to_display = "Exit the Game"
    # writing "Exit the Game" into the rectangle
    stddraw.text(img_center_x, 2.75, text_to_display)
    text_to_display = "High Scores Table"
    # writing "High Scores Table" into the rectangle
    stddraw.text(img_center_x, 0.75, text_to_display)

    # A loop to check the mouse interaction
    while True:
        stddraw.show(50)

        if stddraw.mousePressed():
            # get the coordinates of the most recent location at which the mouse
            # has been left-clicked
            mouse_x, mouse_y = stddraw.mouseX(), stddraw.mouseY()
            # check if these coordinates are inside the buttons
            if mouse_x >= button_blc_x and mouse_x <= button_blc_x + button_w:
                # checking it pressed on to the displaying the highscores
                if mouse_y >= button_blc_y - 4 and mouse_y <= button_blc_y + button_h - 4.5:
                    # display highscores and return the value
                    return display_high_scores(grid_height, grid_width)
                # checking it pressed on to the restarting the game
                elif mouse_y >= button_blc_y and mouse_y <= button_blc_y + button_h - 0.5:
                    return True
                # checking it pressed on to the exit the game
                elif mouse_y >= button_blc_y - 2 and mouse_y < button_blc_y + button_h - 2.5:
                    return False


# A method to display the highscores
def display_high_scores(grid_height, grid_width):
    # setting the background color and button color
    background_color = Color(42, 69, 99)
    button_color = Color(25, 255, 228)

    # clear the background drawing canvas to background_color
    stddraw.clear(background_color)
    stddraw.setPenColor(Color(255, 255, 255))
    # drawing the border
    stddraw.rectangle(0.5, 0.5, grid_width + 2, grid_height - 2)
    stddraw.setFontSize(35)
    # writing the header
    stddraw.text((grid_width + 2) / 2 + 0.5, grid_height - 3, "High Scores Table")
    # drawing a line under the highscore header
    stddraw.line(2.5, grid_height - 3.75, grid_width + 0.5, grid_height - 3.75)

    current_dir = os.path.dirname(os.path.realpath(__file__))
    # compute the path of the highscores file
    scores_file = os.path.join(current_dir, "files", "high_scores.txt")
    scores = []

    # reading the highest 10 scores
    with open(scores_file, "r") as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            if line:
                score = int(line)
                scores.append(score)
                if len(scores) == 10:
                    break
    # closing the file
    f.close()
    # adjusting the pos_x and pos_y
    pos_x = 7.25
    pos_y = grid_height - 5
    counter = 1
    stddraw.setFontSize(25)
    stddraw.setFontFamily("Arial")
    n = len(scores)

    # writing the highest 10 scores onto the table
    while counter - 1 < n:
        stddraw.text(pos_x, pos_y, str(counter) + ".  " + str(scores[counter - 1]) + " points")
        pos_y -= 1.5
        counter += 1
    stddraw.setPenColor(button_color)
    # Restart rectangle
    stddraw.filledRectangle(1, 1, 3.5, 1.5)
    # exit rectangle
    stddraw.filledRectangle(10.5, 1, 3.5, 1.5)
    stddraw.setPenColor(Color(0, 0, 0))
    # writing restart and exit into the rectangles
    stddraw.text(2.75, 1.75, "Restart")
    stddraw.text(12.25, 1.75, "Exit")

    # a loop to check mouse interaction
    while True:
        stddraw.show(50)
        # get the coordinates of the most recent location at which the mouse
        # has been left-clicked
        mouse_x, mouse_y = stddraw.mouseX(), stddraw.mouseY()
        # check if these coordinates are inside the button
        # if the restart is clicked or not
        if mouse_x >= 1 and mouse_x <= 4.5 and mouse_y >= 1 and mouse_y <= 2.5:
            return True
        # if the exit is clicked or not
        elif mouse_x >= 10.5 and mouse_x <= 14 and mouse_y >= 1 and mouse_y <= 2.5:
            exit()


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
    text_to_display = "Start the Game"
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
                    speed_selection_page(grid_height, grid_width)
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
