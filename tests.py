'''
Tests for my CISC108 final project.

Change log:
  - 0.0.1: Initial version
'''

__VERSION__ = '0.0.1'

from cisc108 import assert_equal
from cisc108_game import assert_type

################################################################################
# Game import
# Rename this to the name of your project file.
from project_starter import *


################################################################################
## Testing <name of function>

# Describe this test here, then run whatever code is necessary to
# perform the tests

## Testing make_grid_color
assert_equal(make_grid_color(5, 3, 'black'), [['black', 'black', 'black', 'black', 'black'], ['black', 'black', 'black', 'black', 'black'], ['black', 'black', 'black', 'black', 'black']])
assert_equal(make_grid_color(10, 2, 'orange'), [['orange', 'orange', 'orange', 'orange', 'orange', 'orange', 'orange', 'orange', 'orange', 'orange'], ['orange', 'orange', 'orange', 'orange', 'orange', 'orange', 'orange', 'orange', 'orange', 'orange']])
assert_equal(make_grid_color(2, 4, 'magenta'), [['magenta', 'magenta'], ['magenta', 'magenta'], ['magenta', 'magenta'], ['magenta', 'magenta']])

## Testing update_world
# Testing an initial world
W0 = {
    'grid': make_grid_color(GRID_WIDTH, GRID_HEIGHT, 'white'),
    'current mouse x': None,
    'current mouse y': None,
    'values': [1],
    'target': 0,
    'hovering': None,
    'draw': False,
    'color': 'red'}
assert_equal(W0, {'grid': make_grid_color(GRID_WIDTH, GRID_HEIGHT, 'white'), 'current mouse x': None, 'current mouse y': None, 'values': [1], 'target': 0, 'hovering': None, 'draw': False, 'color': 'red'})

# Drawing mode is on
W1 = {
    'grid': make_grid_color(GRID_WIDTH, GRID_HEIGHT, 'white'),
    'current mouse x': None,
    'current mouse y': None,
    'values': [1],
    'target': 0,
    'hovering': None,
    'draw': True,
    'color': 'green'}
assert_equal(W1, {'grid': make_grid_color(GRID_WIDTH, GRID_HEIGHT, 'white'), 'current mouse x': None, 'current mouse y': None, 'values': [1], 'target': 0, 'hovering': None, 'draw': True, 'color': 'green'})

## Testing screen_to_grid
assert_equal(screen_to_grid(76.9, 23, 50), 167)
assert_equal(screen_to_grid(144.0, 43, 19), 63)
assert_equal(screen_to_grid(23.4, 31, 103), 77)

## Testing advance_color
assert_equal(advance_color(), 'red')