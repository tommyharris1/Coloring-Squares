'''
<Describe your game here. Remove the angle brackets.>

Change log:
  - 0.0.2: Added support for handle_release
  - 0.0.1: Initial version
'''
__VERSION__ = '0.0.2'

import arcade, math, random
from csquares_src import Cisc108Game

'''
COLORING SQUARES - CONTROLS

# Left click on a color in the palette to use that color on the drawing grid. (Press the 'a' or 'b' keys to access extra colors.)
# Right click to toggle "drawing mode" on and off.
# Left click on the trash icon to reset the grid back to white.
# Left click on the eraser to use the eraser.
'''
################################################################################
## Game Constants

WINDOW_WIDTH = 500
WINDOW_HEIGHT = 500
BACKGROUND_COLOR = arcade.color.WHITE
GAME_TITLE = "Coloring Squares"

# The amount of squares in the grid, horizontally and vertically.
GRID_WIDTH = 25
GRID_HEIGHT = 25
# Size of one square on the grid.
SQUARE_SIZE = 20
# Size of boxes for color pallete
BOX_WIDTH = 62.5
# For the color palette
WINDOW_CENTER_X = int(WINDOW_WIDTH/2)

# The different colors that will be accessible on the palette.
RED = arcade.make_soft_square_texture(SQUARE_SIZE, arcade.color.RED, 255, 255)
ORANGE = arcade.make_soft_square_texture(SQUARE_SIZE, arcade.color.ORANGE, 255, 255)
YELLOW = arcade.make_soft_square_texture(SQUARE_SIZE, arcade.color.YELLOW, 255, 255)
GREEN = arcade.make_soft_square_texture(SQUARE_SIZE, arcade.color.GREEN, 255, 255)
BLUE = arcade.make_soft_square_texture(SQUARE_SIZE, arcade.color.BLUE, 255, 255)
PURPLE = arcade.make_soft_square_texture(SQUARE_SIZE, arcade.color.PURPLE, 255, 255)
MAGENTA = arcade.make_soft_square_texture(SQUARE_SIZE, arcade.color.MAGENTA, 255, 255)
BLACK = arcade.make_soft_square_texture(SQUARE_SIZE, arcade.color.BLACK, 255, 255)
WHITE = arcade.make_soft_square_texture(SQUARE_SIZE, arcade.color.WHITE, 255, 255)
APRICOT = arcade.make_soft_square_texture(SQUARE_SIZE, arcade.color.APRICOT, 255, 255)
BROWN = arcade.make_soft_square_texture(SQUARE_SIZE, arcade.color.BROWN, 255, 255)

# All colors in a dictionary
COLORS = {
    'red': RED,
    'orange': ORANGE,
    'yellow': YELLOW,
    'green': GREEN,
    'blue': BLUE,
    'purple': PURPLE,
    'magenta': MAGENTA,
    'black': BLACK,
    'white': WHITE,
    'apricot': APRICOT,
    'brown': BROWN
}
####################################################################
 ##Helper functions
def make_grid_color(width: int, height: int, color: str) -> [[str]]:
    '''
    Make a 2D list (list of lists) of the given width and height,
    where every cell has the given color.
    
    Args:
        width (int): The number of elements in each row.
        height (int): The number of rows.
        color (str): The color string to put in each cell.
    Returns:
        
    '''
    grid = []
    # y will be 0..height
    for y in range(height):
        row = []
        # x will be 0..width
        for x in range(width):
            # Add this cell to the row
            row.append(color)
        # Add this row to the grid
        grid.append(row)
    return grid
################################################################################
## Record definitions

World = {
    # A list of lists of strings representing a 2D grid of colors
    'grid': [[str]],
    # These keep track of the latest mouse position within the grid.
    'current mouse x': int,
    'current mouse y': int,
    # The current list we are displaying to the player.
    'values': [int],
    # The index that the player should click
    'target': int,
    # The index that the player is hovering over
    'hovering': int,
    # Indicates whether drawing mode is on or off
    'draw': bool,
    # Indicates the current color being used on the grid
    'color': str
}

INITIAL_WORLD = {
    'grid': make_grid_color(GRID_WIDTH, GRID_HEIGHT, 'white'),
    'current mouse x': None,
    'current mouse y': None,
    'values': [1],
    'target': 0,
    'hovering': None,
    'draw': False,
    'color': 'red'
}
################################################################################
# Drawing functions
def make_grid_white(world: World):
    '''
    Function for resetting the grid back to white.
    
    Args:
        world (World): The current world to draw.
    '''
    world['grid'] = make_grid_color(GRID_WIDTH, GRID_HEIGHT, 'white')

def draw_world(world: World):
    """
    Describes what is drawn in the world each time.
    
    Args:
        world (World): The current world to draw
    """
    draw_grid(world['grid'])
    draw_boxes(world['values'], world['hovering'])
def draw_grid(grid: [[str]]):
    '''
    Draw the 2D list of colors horizontally and vertically, turning
    the string colors into the actual colored squares.
    
    Args:
        grid ([[str]]): The list of lists (a 2-Dimensional list) of colors.
        world: The current world
    '''
    # We need to know the x and y to draw at.
    # We could have also used the built-in enumerate function to get
    # the x/y indexes of each cell.
    # But instead, we'll use the counting pattern to calculate the x and y.
    y = 0
    for row in grid:
        x = 0
        for cell_color in row:
            square_image = COLORS[cell_color]
            arcade.draw_xywh_rectangle_textured(x*SQUARE_SIZE, y*SQUARE_SIZE,
                                                SQUARE_SIZE, SQUARE_SIZE,
                                                square_image)
            x += 1
        y += 1

################################################################################
# World manipulating functions

def update_world(world: World):
    """
    Describes what happens every update in the world.
    
    Args:
        world (World): The current world to update.
    """
    # We get the current mouse position
    grid_x = world['current mouse x']
    grid_y = world['current mouse y']
    # Is the mouse on a grid cell?
    if grid_x != None and grid_y != None:
        advance_grid_cell_color(world['grid'], grid_x, grid_y, world)
        
def advance_grid_cell_color(grid: [[str]], grid_x: int, grid_y: int, world: World):
    '''
    Determines which color to switch to when initiated by the user.
    
    Args:
        grid ([[str]]): The list of lists (a 2-Dimensional list) of colors.
        grid_x (int): The horizontal value for the grid color.
        grid_y (int): The vertical value for the grid color.
        world: (World): The current world to update.
    '''
    # Look up the old color (note that it's row/column, so y comes first)
    old_color = grid[grid_y][grid_x]
    # Advance that color in the sequence
    new_color = world['color']
    # Mutate the grid by updating the list of list's value with the new color.
    grid[grid_y][grid_x] = new_color
def handle_key(world: World, key: int):
    """
    Describe how the game responds to keyboard input.
    This function will not be used.
    
    Args:
        world (World): Current state of the world.
        key (int): The ASCII value of the pressed keyboard key (use ord and chr).
    """
    if key == ord('a'):
        world['color'] = 'apricot'
    elif key == ord('b'):
        world['color'] = 'brown'
def handle_mouse(world: World, x: int, y: int, button: str):
    """
    Describe how the game responds to mouse clicks.
    This function will be used for toggling "drawing mode" and
    selecting colors in the palette.
    
    Args:
        world (World): Current state of the world.
        x (int): The x-coordinate of the mouse when the button was clicked.
        y (int): The y-coordinate of the mouse when the button was clicked.
        button (str): The button that was clicked ('left', 'right', 'middle')
    """
# Toggle drawing mode
    if button == 'right':
        if world['draw'] == False:
            world['draw'] = True
        else:
            world['draw'] = False
# Selecting colors in the palette
    if button == 'left' and 440.5 < y < 500:
        if x > 0 and x < BOX_WIDTH:
            world['color'] = 'red'
        elif x > BOX_WIDTH and x < BOX_WIDTH*2:
            world['color'] = 'orange'
        elif x > BOX_WIDTH*2 and x < BOX_WIDTH*3:
            world['color'] = 'yellow'
        elif x > BOX_WIDTH*3 and x < BOX_WIDTH*4:
            world['color'] = 'green'
        elif x > BOX_WIDTH*4 and x < BOX_WIDTH*5:
            world['color'] = 'blue'
        elif x > BOX_WIDTH*5 and x < BOX_WIDTH*6:
            world['color'] = 'purple'
        elif x > BOX_WIDTH*6 and x < BOX_WIDTH*7:
            world['color'] = 'magenta'
        elif x > BOX_WIDTH*7 and x < BOX_WIDTH*8:
            world['color'] = 'black'
# For resetting and erasing
    if button == 'left' and 0 < y < 59.5:
        if x > 0 and x < BOX_WIDTH:
            make_grid_white(world)
        elif x > BOX_WIDTH*7 and x < BOX_WIDTH*8:
            world['color'] = 'white'
def handle_motion(world: World, x: int, y: int):
    """
    Moving over a square changes its color.
    
    Args:
        world (World): Current state of the world.
        x (int): The x-coordinate of where the mouse was moved to.
        y (int): The x-coordinate of where the mouse was moved to.
    """
    # First we translate from the position within the window to the
    #   position within the grid of circles
    if world['draw'] == True:
        grid_x = screen_to_grid(x, WINDOW_WIDTH, GRID_WIDTH)
        grid_y = screen_to_grid(y, WINDOW_HEIGHT, GRID_HEIGHT)
    # If we're out of bounds, then we set the values to None
        if grid_x < 0 or grid_x >= GRID_WIDTH:
            grid_x = None
        if grid_y < 0 or grid_y >= GRID_HEIGHT:
            grid_y = None
    # Then we update our world to keep track of the latest mouse
    # movements within the grid.
        world['current mouse x'] = grid_x
        world['current mouse y'] = grid_y
def screen_to_grid(coordinate: float, screen_size: int, grid_size: int) -> int:
    '''
    Converts a coordinate (either the x part or the y part) from a position
    within the window to the equivalent position within the grid. It does this by
    scaling the between the two different sizes.
    
    Think about this as a number line. If you have the coordinate 50 on that
    number line, and the number line's maximum value was 100 (screen_size),
    then scaling that a number line with the maximum value of 20 (grid_size) would
    give you the new coordinate 10.
    
    Args:
        coordinate (float): Either an X or Y value in a coordinate system.
        screen_size (int): The number of values in the original coordinate system.
        grid_width (int): The number of values in the target coordinate system.
    Returns:
        int: The scaled value in the other coordinate system.
    '''
    return int(coordinate * grid_size / screen_size)
    
def advance_color() -> str:
    '''
    Consumes a color (string) and produces the starting color, which is red.
    
    Returns:
        str: The starting color in the sequence
    '''
    return 'red'
def handle_release(world: World, key: int):
    """
    Describe how the game responds to releasing a keyboard key.
    This function will not be used.
    
    Args:
        world (World): Current state of the world.
        key (int): The ASCII value of the released keyboard key (use ord and chr).
    """

########################################################################################3
# Additional functions for the color palette
def draw_box_red(filled: bool, value: int, x: int, y: int, size: int):
    '''
    Draws a red box for the palette.
    
    Args:
        filled (bool): Whether or not to fill the box.
        value (int): The value that should be shown inside this box.
        x (int): The x-coordinate to draw at.
        y (int): The y-coordinate to draw at.
        size (int): The height and width of the box.
    '''
    arcade.draw_xywh_rectangle_filled(x, y, size, size+15, arcade.color.RED)
    arcade.draw_xywh_rectangle_outline(x, y, size, size+15, arcade.color.BLACK)

def draw_box_orange(filled: bool, value: int, x: int, y: int, size: int):
    '''
    Draws an orange box for the palette.
    
    Args:
        filled (bool): Whether or not to fill the box.
        value (int): The value that should be shown inside this box.
        x (int): The x-coordinate to draw at.
        y (int): The y-coordinate to draw at.
        size (int): The height and width of the box.
    '''
    arcade.draw_xywh_rectangle_filled(x, y, size, size+15, arcade.color.ORANGE)
    arcade.draw_xywh_rectangle_outline(x, y, size, size+15, arcade.color.BLACK)

def draw_box_yellow(filled: bool, value: int, x: int, y: int, size: int):
    '''
    Draws a yellow box for the palette.
    
    Args:
        filled (bool): Whether or not to fill the box.
        value (int): The value that should be shown inside this box.
        x (int): The x-coordinate to draw at.
        y (int): The y-coordinate to draw at.
        size (int): The height and width of the box.
    '''
    arcade.draw_xywh_rectangle_filled(x, y, size, size+15, arcade.color.YELLOW)
    arcade.draw_xywh_rectangle_outline(x, y, size, size+15, arcade.color.BLACK)

def draw_box_green(filled: bool, value: int, x: int, y: int, size: int):
    '''
    Draws a green box for the palette.
    
    Args:
        filled (bool): Whether or not to fill the box.
        value (int): The value that should be shown inside this box.
        x (int): The x-coordinate to draw at.
        y (int): The y-coordinate to draw at.
        size (int): The height and width of the box.
    '''
    arcade.draw_xywh_rectangle_filled(x, y, size, size+15, arcade.color.GREEN)
    arcade.draw_xywh_rectangle_outline(x, y, size, size+15, arcade.color.BLACK)

def draw_box_blue(filled: bool, value: int, x: int, y: int, size: int):
    '''
    Draws a blue box for the palette.
    
    Args:
        filled (bool): Whether or not to fill the box.
        value (int): The value that should be shown inside this box.
        x (int): The x-coordinate to draw at.
        y (int): The y-coordinate to draw at.
        size (int): The height and width of the box.
    '''
    arcade.draw_xywh_rectangle_filled(x, y, size, size+15, arcade.color.BLUE)
    arcade.draw_xywh_rectangle_outline(x, y, size, size+15, arcade.color.BLACK)

def draw_box_purple(filled: bool, value: int, x: int, y: int, size: int):
    '''
    Draws a purple box for the palette.
    
    Args:
        filled (bool): Whether or not to fill the box.
        value (int): The value that should be shown inside this box.
        x (int): The x-coordinate to draw at.
        y (int): The y-coordinate to draw at.
        size (int): The height and width of the box.
    '''
    arcade.draw_xywh_rectangle_filled(x, y, size, size+15, arcade.color.PURPLE)
    arcade.draw_xywh_rectangle_outline(x, y, size, size+15, arcade.color.BLACK)

def draw_box_magenta(filled: bool, value: int, x: int, y: int, size: int):
    '''
    Draws a magenta box for the palette.
    
    Args:
        filled (bool): Whether or not to fill the box.
        value (int): The value that should be shown inside this box.
        x (int): The x-coordinate to draw at.
        y (int): The y-coordinate to draw at.
        size (int): The height and width of the box.
    '''
    arcade.draw_xywh_rectangle_filled(x, y, size, size+15, arcade.color.MAGENTA)
    arcade.draw_xywh_rectangle_outline(x, y, size, size+15, arcade.color.BLACK)

def draw_box_black(filled: bool, value: int, x: int, y: int, size: int):
    '''
    Draws a black box for the palette.
    
    Args:
        filled (bool): Whether or not to fill the box.
        value (int): The value that should be shown inside this box.
        x (int): The x-coordinate to draw at.
        y (int): The y-coordinate to draw at.
        size (int): The height and width of the box.
    '''
    arcade.draw_xywh_rectangle_filled(x, y, size, size+15, arcade.color.BLACK)
    arcade.draw_xywh_rectangle_outline(x, y, size, size+15, arcade.color.BLACK)

def draw_boxes(values: [int], hovering: int):
    '''
    Draws all the boxes for the color palette.
    
    Args:
        values ([int]): The list of values to draw.
        hovering (int): The index of the value to fill in with color.
    '''
    index = 0
    for box_value in values:
        # If the current index is our hovering one, we pass in True
        draw_box_red(hovering==index, box_value, 0, 440.5, BOX_WIDTH)
        draw_box_orange(hovering==index, box_value, 62.5, 440.5, BOX_WIDTH)
        draw_box_yellow(hovering==index, box_value, 125, 440.5, BOX_WIDTH)
        draw_box_green(hovering==index, box_value, 187.5, 440.5, BOX_WIDTH)
        draw_box_blue(hovering==index, box_value, 250, 440.5, BOX_WIDTH)
        draw_box_purple(hovering==index, box_value, 312.5, 440.5, BOX_WIDTH)
        draw_box_magenta(hovering==index, box_value, 375, 440.5, BOX_WIDTH)
        draw_box_black(hovering==index, box_value, 437.5, 440.5, BOX_WIDTH)
        arcade.draw_texture_rectangle(40, 40, 59.5, 62.5, arcade.load_texture('garbage.png'))
        arcade.draw_texture_rectangle(460, 40, 59.5, 62.5, arcade.load_texture('eraser.png'))
        index = index + 1

############################################################################
# Set up the game
# Don't need to change any of this

if __name__ == '__main__':
    Cisc108Game(World, WINDOW_WIDTH, WINDOW_HEIGHT, GAME_TITLE, INITIAL_WORLD,
                draw_world, update_world, handle_key, handle_mouse,
                handle_motion, handle_release)
    arcade.set_background_color(BACKGROUND_COLOR)
    arcade.run()
