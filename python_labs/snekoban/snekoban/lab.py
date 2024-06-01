"""
6.1010 Lab 4:
Snekoban Game
"""

import json
import typing

# NO ADDITIONAL IMPORTS!


def make_new_game(level_description):
    """
    Given a description of a game state, create and return a game
    representation of your choice.
    """
    player = set()
    computers = set()
    walls = set()
    targets = set()

    for i, row_objects in enumerate(level_description):
        for j, cell_objects in enumerate(row_objects):
            position = (i, j)
            for obj in cell_objects:
                if obj == "player":
                    player.add(position)
                elif obj == "computer":
                    computers.add(position)
                elif obj == "wall":
                    walls.add(position)
                elif obj == "target":
                    targets.add(position)
    game_state = {
        "board_dim": (len(level_description), len(level_description[0])),
        "player": player,
        "computers": computers,
        "walls": walls,
        "targets": targets,
    }

    return game_state


def victory_check(game):
    """
    Given a game representation (of the form returned from make_new_game),
    return a Boolean: True if the given game satisfies the victory condition,
    and False otherwise.
    """
    targets = game["targets"]
    computers = game["computers"]
    return targets == computers and bool(targets)


def step_game(game, direction):
    """Given a game representation and direction attempted by player,
    returns game representation that updates object tuple positions"""
    direction_vector = {
        "up": (-1, 0),
        "down": (1, 0),
        "left": (0, -1),
        "right": (0, 1),
    }
    new_game = {
        "board_dim": tuple(game["board_dim"]),
        "player": set(game["player"]),
        "computers": set(game["computers"]),
        "walls": set(game["walls"]),
        "targets": set(game["targets"]),
    }
    move = direction_vector[direction]

    def is_valid_move(position, move):
        future = (position[0] + move[0], position[1] + move[1])
        if position in new_game["computers"]:
            if future in new_game["computers"] or future in new_game["walls"]:
                return False

        return (
            0 < position[0] < game["board_dim"][0] - 1
            and 0 < position[1] < new_game["board_dim"][1] - 1
            and position not in new_game["walls"]
        )

    new_player = set()
    player_pos = new_game["player"].pop()
    new_pos = (player_pos[0] + move[0], player_pos[1] + move[1])
    future = (new_pos[0] + move[0], new_pos[1] + move[1])
    if is_valid_move(new_pos, move):
        new_player.add(new_pos)
        if new_pos in new_game["computers"]:
            new_game["computers"].discard(new_pos)
            new_game["computers"].add(future)
    else:
        new_player.add(player_pos)
    new_game["player"] = new_player
    return new_game


def dump_game(game):
    """
    Given a game representation (of the form returned from make_new_game),
    convert it back into a level description that would be a suitable input to
    make_new_game (a list of lists of lists of strings).

    This function is used by the GUI and the tests to see what your game
    implementation has done, and it can also serve as a rudimentary way to
    print out the current state of your game for testing and debugging on your
    own.
    """
    empty = [
        [list() for j in range(game["board_dim"][1])]
        for i in range(game["board_dim"][0])
    ]
    for tup in game["player"]:
        row, col = tup
        empty[row][col].append("player")
    for tup in game["walls"]:
        row, col = tup
        empty[row][col].append("wall")
    for tup in game["targets"]:
        row, col = tup
        empty[row][col].append("target")
    for tup in game["computers"]:
        row, col = tup
        empty[row][col].append("computer")
    return empty


def hash_game_state(game):
    gamer = game["player"].copy()
    return (frozenset(set(game["computers"])), gamer.pop())


def solve_puzzle(game):
    """
    Given a game representation (of the form returned from make_new_game), find
    a solution.

    Return a list of strings representing the shortest sequence of moves ("up",
    "down", "left", and "right") needed to reach the victory condition.

    If the given level cannot be solved, return None.
    """
    direction_vector = {
        "up": (-1, 0),
        "down": (1, 0),
        "left": (0, -1),
        "right": (0, 1),
    }
    game_state = hash_game_state(game)
    queue = [(game_state, [])]
    visited = set()

    while queue:
        current_game, current_path = queue.pop(0)
        if current_game in visited:
            continue
        visited.add(current_game)
        checker = {
            "board_dim": tuple(game["board_dim"]),
            "walls": set(game["walls"]),
            "targets": set(game["targets"]),
            "computers": set(current_game[0]),
            "player": set([current_game[1]]),
        }
        if victory_check(checker):
            return current_path
        for direction in direction_vector:
            next_game = hash_game_state(step_game(checker, direction))
            if next_game not in visited:
                queue.append((next_game, current_path + [direction]))
    return None


if __name__ == "__main__":
    canon = [
        [["wall"], ["wall"], ["wall"], ["wall"], ["wall"], ["wall"], ["wall"]],
        [["wall"], [], ["wall"], [], [], [], ["wall"]],
        [["wall"], [], [], [], [], [], ["wall"]],
        [["wall"], ["target"], ["computer"], ["player"], [], [], ["wall"]],
        [["wall"], [], [], [], [], [], ["wall"]],
        [["wall"], ["wall"], ["wall"], ["wall"], ["wall"], ["wall"], ["wall"]],
    ]
    # print(f"{make_new_game(canon)=}")
    # print(f"{step_game(make_new_game(canon), 'up')}")
    # print(f"{dump_game(make_new_game(canon))=}")
    # print(f"{canon=}")
    # our_version = make_new_game(canon)
    # print(f"{our_version=}")
    # dumper = dump_game(our_version)
    # print("LLLLL",dumper)

    # our_solved = step_game(our_version, "left")
    # print(f"{our_solved=}")
    # our_past_solved = step_game(our_solved, "up")
    # print(f"{our_past_solved=}")
    # print(f"{solve_puzzle(our_version)=}")
    pass
