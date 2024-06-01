# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 17:58:31 2024

@author: gava1
"""
    for each in mines:
        update_matrix(board, each, '.')
        
        for adj in neighbor_list(each, dimensions):
            val = look_up(board, adj)
            if val != '.':
                update_matrix(board, adj, val + 1)











# def new_game_2d(nrows, ncolumns, mines):
#     """
#     Start a new game.

#     Return a game state dictionary, with the 'dimensions', 'state', 'board' and
#     'visible' fields adequately initialized.

#     Parameters:
#        nrows (int): Number of rows
#        ncolumns (int): Number of columns
#        mines (list): List of mines, given in (row, column) pairs, which are
#                      tuples

#     Returns:
#        A game state dictionary

#     >>> dump(new_game_2d(2, 4, [(0, 0), (1, 0), (1, 1)]))
#     board:
#         ['.', 3, 1, 0]
#         ['.', '.', 1, 0]
#     dimensions: (2, 4)
#     state: ongoing
#     visible:
#         [False, False, False, False]
#         [False, False, False, False]
#     """
#     board = []
#     for r in range(nrows):
#         row = []
#         for c in range(ncolumns):
#             if [r, c] in mines or (r, c) in mines:
#                 row.append(".")
#             else:
#                 row.append(0)
#         board.append(row)
#     visible = []
#     for r in range(nrows):
#         row = []
#         for c in range(ncolumns):
#             row.append(False)
#         visible.append(row)
#     for r in range(nrows):
#         for c in range(ncolumns):
#             if board[r][c] == 0:
#                 neighbor_mines = 0
#                 if 0 <= r - 1 < nrows:
#                     if 0 <= c - 1 < ncolumns:
#                         if board[r - 1][c - 1] == ".":
#                             neighbor_mines += 1
#                 if 0 <= r < nrows:
#                     if 0 <= c - 1 < ncolumns:
#                         if board[r][c - 1] == ".":
#                             neighbor_mines += 1
#                 if 0 <= r + 1 < nrows:
#                     if 0 <= c - 1 < ncolumns:
#                         if board[r + 1][c - 1] == ".":
#                             neighbor_mines += 1
#                 if 0 <= r - 1 < nrows:
#                     if 0 <= c < ncolumns:
#                         if board[r - 1][c] == ".":
#                             neighbor_mines += 1
#                 if 0 <= r < nrows:
#                     if 0 <= c < ncolumns:
#                         if board[r][c] == ".":
#                             neighbor_mines += 1
#                 if 0 <= r + 1 < nrows:
#                     if 0 <= c < ncolumns:
#                         if board[r + 1][c] == ".":
#                             neighbor_mines += 1
#                 if 0 <= r - 1 < nrows:
#                     if 0 <= c + 1 < ncolumns:
#                         if board[r - 1][c + 1] == ".":
#                             neighbor_mines += 1
#                 if 0 <= r < nrows:
#                     if 0 <= c + 1 < ncolumns:
#                         if board[r][c + 1] == ".":
#                             neighbor_mines += 1
#                 if 0 <= r + 1 < nrows:
#                     if 0 <= c + 1 < ncolumns:
#                         if board[r + 1][c + 1] == ".":
#                             neighbor_mines += 1
#                 board[r][c] = neighbor_mines
#     return {
#         "dimensions": (nrows, ncolumns),
#         "board": board,
#         "visible": visible,
#         "state": "ongoing",
#     }

# def dig_2d(game, row, col):
#     """
#     Reveal the cell at (row, col), and, in some cases, recursively reveal its
#     neighboring squares.

#     Update game['visible'] to reveal (row, col).  Then, if (row, col) has no
#     adjacent mines (including diagonally), then recursively reveal (dig up) its
#     eight neighbors.  Return an integer indicating how many new squares were
#     revealed in total, including neighbors, and neighbors of neighbors, and so
#     on.

#     The state of the game should be changed to 'defeat' when at least one mine
#     is visible on the board after digging (i.e. game['visible'][mine_location]
#     == True), 'victory' when all safe squares (squares that do not contain a
#     mine) and no mines are visible, and 'ongoing' otherwise.

#     Parameters:
#        game (dict): Game state
#        row (int): Where to start digging (row)
#        col (int): Where to start digging (col)

#     Returns:
#        int: the number of new squares revealed

#     >>> game = {'dimensions': (2, 4),
#     ...         'board': [['.', 3, 1, 0],
#     ...                   ['.', '.', 1, 0]],
#     ...         'visible': [[False, True, False, False],
#     ...                  [False, False, False, False]],
#     ...         'state': 'ongoing'}
#     >>> dig_2d(game, 0, 3)
#     4
#     >>> dump(game)
#     board:
#         ['.', 3, 1, 0]
#         ['.', '.', 1, 0]
#     dimensions: (2, 4)
#     state: victory
#     visible:
#         [False, True, True, True]
#         [False, False, True, True]

#     >>> game = {'dimensions': [2, 4],
#     ...         'board': [['.', 3, 1, 0],
#     ...                   ['.', '.', 1, 0]],
#     ...         'visible': [[False, True, False, False],
#     ...                  [False, False, False, False]],
#     ...         'state': 'ongoing'}
#     >>> dig_2d(game, 0, 0)
#     1
#     >>> dump(game)
#     board:
#         ['.', 3, 1, 0]
#         ['.', '.', 1, 0]
#     dimensions: [2, 4]
#     state: defeat
#     visible:
#         [True, True, False, False]
#         [False, False, False, False]
#     """
#     if game["state"] == "defeat" or game["state"] == "victory":
#         game["state"] = game["state"]  # keep the state the same
#         return 0

#     if game["board"][row][col] == ".":
#         game["visible"][row][col] = True
#         game["state"] = "defeat"
#         return 1

#     num_revealed_mines = 0
#     num_revealed_squares = 0
#     for r in range(game["dimensions"][0]):
#         for c in range(game["dimensions"][1]):
#             if game["board"][r][c] == ".":
#                 if game["visible"][r][c] == True:
#                     num_revealed_mines += 1
#             elif game["visible"][r][c] == False:
#                 num_revealed_squares += 1
#     if num_revealed_mines != 0:
#         # if num_revealed_mines is not equal to zero, set the game state to 
#         # defeat and return 0
#         game["state"] = "defeat"
#         return 0
#     if num_revealed_squares == 0:
#         game["state"] = "victory"
#         return 0

#     if game["visible"][row][col] != True:
#         game["visible"][row][col] = True
#         revealed = 1
#     else:
#         return 0

#     if game["board"][row][col] == 0:
#         nrows, ncolumns = game["dimensions"]
#         if 0 <= row - 1 < nrows:
#             if 0 <= col - 1 < ncolumns:
#                 if game["board"][row - 1][col - 1] != ".":
#                     if game["visible"][row - 1][col - 1] == False:
#                         revealed += dig_2d(game, row - 1, col - 1)
#         if 0 <= row < nrows:
#             if 0 <= col - 1 < ncolumns:
#                 if game["board"][row][col - 1] != ".":
#                     if game["visible"][row][col - 1] == False:
#                         revealed += dig_2d(game, row, col - 1)
#         if 0 <= row + 1 < nrows:
#             if 0 <= col - 1 < ncolumns:
#                 if game["board"][row + 1][col - 1] != ".":
#                     if game["visible"][row + 1][col - 1] == False:
#                         revealed += dig_2d(game, row + 1, col - 1)
#         if 0 <= row - 1 < nrows:
#             if 0 <= col < ncolumns:
#                 if game["board"][row - 1][col] != ".":
#                     if game["visible"][row - 1][col] == False:
#                         revealed += dig_2d(game, row - 1, col)
#         if 0 <= row < nrows:
#             if 0 <= col < ncolumns:
#                 if game["board"][row][col] != ".":
#                     if game["visible"][row][col] == False:
#                         revealed += dig_2d(game, row, col)
#         if 0 <= row + 1 < nrows:
#             if 0 <= col < ncolumns:
#                 if game["board"][row + 1][col] != ".":
#                     if game["visible"][row + 1][col] == False:
#                         revealed += dig_2d(game, row + 1, col)
#         if 0 <= row - 1 < nrows:
#             if 0 <= col + 1 < ncolumns:
#                 if game["board"][row - 1][col + 1] != ".":
#                     if game["visible"][row - 1][col + 1] == False:
#                         revealed += dig_2d(game, row - 1, col + 1)
#         if 0 <= row < nrows:
#             if 0 <= col + 1 < ncolumns:
#                 if game["board"][row][col + 1] != ".":
#                     if game["visible"][row][col + 1] == False:
#                         revealed += dig_2d(game, row, col + 1)
#         if 0 <= row + 1 < nrows:
#             if 0 <= col + 1 < ncolumns:
#                 if game["board"][row + 1][col + 1] != ".":
#                     if game["visible"][row + 1][col + 1] == False:
#                         revealed += dig_2d(game, row + 1, col + 1)

#     num_revealed_mines = 0  # set number of mines to 0
#     num_revealed_squares = 0
#     for r in range(game["dimensions"][0]):
#         # for each r,
#         for c in range(game["dimensions"][1]):
#             # for each c,
#             if game["board"][r][c] == ".":
#                 if game["visible"][r][c] == True:
#                     # if the game visible is True, and the board is '.',
#                     # add 1 to mines revealed
#                     num_revealed_mines += 1
#             elif game["visible"][r][c] == False:
#                 num_revealed_squares += 1
#     bad_squares = num_revealed_mines + num_revealed_squares
#     if bad_squares > 0:
#         game["state"] = "ongoing"
#         return revealed
#     else:
#         game["state"] = "victory"
#         return revealed

# def render_2d_locations(game, all_visible=False):
#     """
#     Prepare a game for display.

#     Returns a two-dimensional array (list of lists) of '_' (hidden squares),
#     '.' (mines), ' ' (empty squares), or '1', '2', etc. (squares neighboring
#     mines).  game['visible'] indicates which squares should be visible.  If
#     all_visible is True (the default is False), game['visible'] is ignored
#     and all cells are shown.

#     Parameters:
#        game (dict): Game state
#        all_visible (bool): Whether to reveal all tiles or just the ones allowed
#                     by game['visible']

#     Returns:
#        A 2D array (list of lists)

#     >>> game = {'dimensions': (2, 4),
#     ...         'state': 'ongoing',
#     ...         'board': [['.', 3, 1, 0],
#     ...                   ['.', '.', 1, 0]],
#     ...         'visible':  [[False, True, True, False],
#     ...                   [False, False, True, False]]}
#     >>> render_2d_locations(game, False)
#     [['_', '3', '1', '_'], ['_', '_', '1', '_']]

#     >>> render_2d_locations(game, True)
#     [['.', '3', '1', ' '], ['.', '.', '1', ' ']]
#     """
#     rowy = game['dimensions'][0]
#     colx = game['dimensions'][1]
#     container = []
#     for y in range(rowy):
#         row = []
#         for x in range(colx):
#             if not game['visible'][y][x] and not all_visible:
#                 row.append("_")
#             elif game['board'][y][x] == 0:
#                 row.append(" ")
#             else:
#                 row.append(str(game['board'][y][x]))
#         container.append(row)
#     return container 
def populate_board(board, dimensions, mines):
    """Populate the board with mines and update neighboring squares.

    Args:
        board (list): N-dimensional board
        dimensions (tuple): Dimensions of the board
        mines (list): Mine locations as a list of tuples

    Returns:
        None
    """
    def is_in_bounds(coords):
        """Return whether the coordinates are within bounds.

        Args:
            coords (tuple): Coordinates of a square

        Returns:
            boolean: True if the coordinates are within bounds, False otherwise
        """
        for coord, dim_size in zip(coords, dimensions):
            if coord < 0 or coord >= dim_size:
                return False
        return True

    def neighbors(coords):
        """Return a list of the neighbors of a square.

        Args:
            coords (tuple): Coordinates for the square

        Returns:
            list: Coordinates of neighbors
        """
        neighborList = []
        cons_neighbors(coords, 0, neighborList)
        return neighborList

    def cons_neighbors(coords, index, neighbors):
        """Construct neighbors recursively.

        Args:
            coords (tuple): Current coordinates being checked
            index (int): Current dimension index
            neighbors (list): List to store neighbor coordinates

        Returns:
            None
        """
        if index == len(coords) - 1:
            for dx in (-1, 0, 1):
                coord = list(coords)
                coord[index] += dx
                if is_in_bounds(coord):
                    neighbors.append(tuple(coord))
        else:
            for dx in (-1, 0, 1):
                coord = list(coords)
                coord[index] += dx
                cons_neighbors(coord, index + 1, neighbors)

    for mine in mines:
        set_coords(board, mine, '.')
        for neighbor in neighbors(mine):
            value = get_coords(board, neighbor)
            if value != '.':
                set_coords(board, neighbor, value + 1)
                
    if game['state'] != 'ongoing':
        return 0

    def is_in_bounds(coords):
        """Check if the coordinates are within bounds."""
        for coord, dim_size in zip(coords, game['dimensions']):
            if coord < 0 or coord >= dim_size:
                return False
        return True
    
    def neighbors(coords):
        """Return neighboring coordinates."""
        offsets = [-1, 0, 1]
        neighbor_list = []
        for offset in offsets:
            neighbor_coords = tuple(coord + offset for coord in coords)
            if is_in_bounds(neighbor_coords):
                neighbor_list.append(neighbor_coords)
        return neighbor_list
    
    def reveal(coords):
        """Reveal square at coords and recursively reveal neighbors."""
        value = game['board']
        visible = game['visible']
    
        if visible[coords] or value[coords] == '.':
            return 0
    
        visible[coords] = True
        revealed_count = 1
    
        if value[coords] == 0:
            for neighbor in neighbors(coords):
                revealed_count += reveal(neighbor)
    
        return revealed_count
    
    revealed_count = reveal(coordinates)

    # Update game state
    if game['board'][coordinates] == '.':
        game['state'] = 'defeat'
    elif all(game['visible'][coords] or game['board'][coords] == '.' for coords in game['allCoords']):
        game['state'] = 'victory'
    
    return revealed_count

# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 13:11:33 2024

@author: gava1
"""

# def neighbor_squares(dims, row, col):
#     """Helper function: returns square's neighbors"""
#     neighbors = []
#     for i in range(-1, 2):
#         for j in range(-1, 2):
#             if (0 <= row + i < dims[0]) and (0 <= col + j < dims[1]):
#                 neighbors.append((row + i, col + j))
#     return neighbors

# print(neighbor_squares((10,20,3), 5, 13,0))

# def neighbor_squares(dims, row, col, zet):
#     """Helper function: returns square's neighbors"""
#     neighbors = []
#     for i in range(-1, 2):
#         for j in range(-1, 2):
#           for z in range(-1,2):  
#                 if (0 <= row + i < dims[0]) and (0 <= col + j < dims[1]) and (0 <= zet + z < dims[2]):
#                     neighbors.append((row + i, col + j, zet + z))
#     return neighbors

# print(neighbor_squares((10,20,3), 5, 13,0))
# ok chat, I dont think that function works. I do like the previous version so we'll stick to that for now, cause its basically a reformating issue: So what I want is a function that conversts a flattened list game representation into a multidimensional array.  So if I have a flattened list like this one: [1, '.', 1, 0, 0, 0, 0, 1, '.', 1, 1, '.', 1, 0, 0, 0],  and we are given a tuple with length of the number of dimensions (i.e if tuple=(2,3) it's a tuple representing a 2 by 3 dimensionality, if tuple= (2,3,2,5) , it is a tupple with 2 by 3 by 2 by 5 dimensionality) and we that original flattened list to be an overral list with tuple[0] rows, tuple[1] columns, tuple[2] inner lists, tuple[3] inner inner list,.... tuple[N dimension aka length of tuple] innermost lists. So our [1, '.', 1, 0, 0, 0, 0, 1, '.', 1, 1, '.', 1, 0, 0, 0] example would be 
def initialize_board(dimensions, elem):
    """Return a new game board.

    Args:
        dimensions (tuple): Dimensions of the board
        elem (any): Initial value of every square on the board

    Returns:
        list: N-dimensional board
    """
    if len(dimensions) == 1:
        return [elem for _ in range(dimensions[0])]
    return [initialize_board(dimensions[1:], elem) for _ in range(dimensions[0])]

def set_coords(board, coords, value):
    """Set the value of a square at the given coordinates on the board.

    Args:
        board (list): N-dimensional board
        coords (tuple): Coordinates of the square
        value (any): Value to set

    Returns:
        None
    """
    if len(coords) == 1:
        board[coords[0]] = value
    else:
        set_coords(board[coords[0]], coords[1:], value)

def get_coords(board, coords):
    """Get the value of a square at the given coordinates on the board.

    Args:
        board (list): N-dimensional board
        coords (tuple): Coordinates of the square

    Returns:
        any: Value of the square
    """
    if len(coords) == 1:
        return board[coords[0]]
    else:
        return get_coords(board[coords[0]], coords[1:])

def populate_board(board, dimensions, mines):
    """Populate the board with mines and update neighboring squares.

    Args:
        board (list): N-dimensional board
        dimensions (tuple): Dimensions of the board
        mines (list): Mine locations as a list of tuples

    Returns:
        None
    """
    def is_in_bounds(coords):
        """Return whether the coordinates are within bounds.

        Args:
            coords (tuple): Coordinates of a square

        Returns:
            boolean: True if the coordinates are within bounds, False otherwise
        """
        for coord, dim_size in zip(coords, dimensions):
            if coord < 0 or coord >= dim_size:
                return False
        return True

    def neighbors(coords):
        """Return a list of the neighbors of a square.

        Args:
            coords (tuple): Coordinates for the square

        Returns:
            list: Coordinates of neighbors
        """
        neighborList = []
        cons_neighbors(coords, 0, neighborList)
        return neighborList

    def cons_neighbors(coords, index, neighbors):
        """Construct neighbors recursively.

        Args:
            coords (tuple): Current coordinates being checked
            index (int): Current dimension index
            neighbors (list): List to store neighbor coordinates

        Returns:
            None
        """
        if index == len(coords) - 1:
            for dx in (-1, 0, 1):
                coord = list(coords)
                coord[index] += dx
                if is_in_bounds(coord):
                    neighbors.append(tuple(coord))
        else:
            for dx in (-1, 0, 1):
                coord = list(coords)
                coord[index] += dx
                cons_neighbors(coord, index + 1, neighbors)

    for mine in mines:
        set_coords(board, mine, '.')
        for neighbor in neighbors(mine):
            value = get_coords(board, neighbor)
            if value != '.':
                set_coords(board, neighbor, value + 1)


def initialize_visibility(dimensions):
    """Initialize the visibility matrix.

    Args:
        dimensions (tuple): Dimensions of the board

    Returns:
        list: N-dimensional visibility matrix
    """
    return initialize_board(dimensions, False)

# Example usage
dimensions, mines = (2, 4), [(0, 0), (1, 0), (1, 1)]
# dimensions = (2, 4, 2)
# mines = [(0, 0, 1), (1, 0, 0), (1, 1, 1)]

board = initialize_board(dimensions, 0)
populate_board(board, dimensions, mines)

visible = initialize_visibility(dimensions)

print("Board:", board)
print("Visible:", visible)

def initialize_board(dimensions, elem):
    """Return a new game board.

    Args:
        dimensions (tuple): Dimensions of the board
        elem (any): Initial value of every square on the board

    Returns:
        list: N-dimensional board
    """
    if len(dimensions) == 1:
        return [elem for _ in range(dimensions[0])]
    return [initialize_board(dimensions[1:], elem) for _ in range(dimensions[0])]

def set_coords(board, coords, value):
    """Set the value of a square at the given coordinates on the board.

    Args:
        board (list): N-dimensional board
        coords (tuple): Coordinates of the square
        value (any): Value to set

    Returns:
        None
    """
    if len(coords) == 1:
        board[coords[0]] = value
    else:
        set_coords(board[coords[0]], coords[1:], value)

def get_coords(board, coords):
    """Get the value of a square at the given coordinates on the board.

    Args:
        board (list): N-dimensional board
        coords (tuple): Coordinates of the square

    Returns:
        any: Value of the square
    """
    if len(coords) == 1:
        return board[coords[0]]
    else:
        return get_coords(board[coords[0]], coords[1:])

def populate_board(board, dimensions, mines):
    """Populate the board with mines and update neighboring squares.

    Args:
        board (list): N-dimensional board
        dimensions (tuple): Dimensions of the board
        mines (list): Mine locations as a list of tuples

    Returns:
        None
    """
    def is_in_bounds(coords):
        """Return whether the coordinates are within bounds.

        Args:
            coords (tuple): Coordinates of a square

        Returns:
            boolean: True if the coordinates are within bounds, False otherwise
        """
        for coord, dim_size in zip(coords, dimensions):
            if coord < 0 or coord >= dim_size:
                return False
        return True

    def neighbors(coords):
        """Return a list of the neighbors of a square.

        Args:
            coords (tuple): Coordinates for the square

        Returns:
            list: Coordinates of neighbors
        """
        neighborList = []
        cons_neighbors(coords, 0, neighborList)
        return neighborList

    def cons_neighbors(coords, index, neighbors):
        """Construct neighbors recursively.

        Args:
            coords (tuple): Current coordinates being checked
            index (int): Current dimension index
            neighbors (list): List to store neighbor coordinates

        Returns:
            None
        """
        if index == len(coords) - 1:
            for dx in (-1, 0, 1):
                coord = list(coords)
                coord[index] += dx
                if is_in_bounds(coord):
                    neighbors.append(tuple(coord))
        else:
            for dx in (-1, 0, 1):
                coord = list(coords)
                coord[index] += dx
                cons_neighbors(coord, index + 1, neighbors)

    for mine in mines:
        set_coords(board, mine, '.')
        for neighbor in neighbors(mine):
            value = get_coords(board, neighbor)
            if value != '.':
                set_coords(board, neighbor, value + 1)


def initialize_visibility(dimensions):
    """Initialize the visibility matrix.

    Args:
        dimensions (tuple): Dimensions of the board

    Returns:
        list: N-dimensional visibility matrix
    """
    return initialize_board(dimensions, False)
    
    
def new_game_nd(dimensions, mines):
    """
    Start a new game.

    Return a game state dictionary, with the 'dimensions', 'state', 'board' and
    'visible' fields adequately initialized.

    Args:
       dimensions (tuple): Dimensions of the board
       mines (list): mine locations as a list of tuples, each an
                     N-dimensional coordinate

    Returns:
       A game state dictionary

    >>> g = new_game_nd((2, 4, 2), [(0, 0, 1), (1, 0, 0), (1, 1, 1)])
    >>> dump(g)
    board:
        [[3, '.'], [3, 3], [1, 1], [0, 0]]
        [['.', 3], [3, '.'], [1, 1], [0, 0]]
    dimensions: (2, 4, 2)
    state: ongoing
    visible:
        [[False, False], [False, False], [False, False], [False, False]]
        [[False, False], [False, False], [False, False], [False, False]]
    """
    board = initialize_board(dimensions, 0)
    visible = initialize_visibility(dimensions)
    populate_board(board, dimensions, mines)
    state = 'ongoing'
    return {'dimensions': dimensions,
            'board': board,
            'visible': visible,
            'state': state}