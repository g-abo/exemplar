"""
6.101 Lab 3:
Bacon Number
"""

#!/usr/bin/env python3
import pickle


# NO ADDITIONAL IMPORTS ALLOWED!
def transform_data(raw_data):
    """takes in list of actor, actor, movie tuples
    returns dictionary of actors keys with set values of co-actors
    and dictionary with movie keys with set of coactor tuples"""
    actor_graph = {}
    dict_films = {}
    # Iterate through each record in raw_data
    for actor_id_1, actor_id_2, film_id in raw_data:
        actor_graph.setdefault(actor_id_1, set()).add(actor_id_2)
        actor_graph.setdefault(actor_id_2, set()).add(actor_id_1)
        dict_films.setdefault(film_id, set()).add((actor_id_1, actor_id_2))
    return actor_graph, dict_films


def acted_together(transform_data, actor1, actor2):
    """Returns T or F bools depending if actors are considered to
    have coacted, including self relationship"""
    if actor1 == actor2:
        return True
    return actor2 in transform_data[0][actor1] or actor1 in transform_data[0][actor2]


def actor_path(transformed_data, actor_id_1, goal_test_function):
    """Through BFS, Takes in BFS, actor 1, and boolean function to test each
    node for truth Returns the shortest list path from the start actor, until
    the goal is satisfied"""
    actor_graph, start_actor, goal_test = (
        transformed_data[0],
        actor_id_1,
        goal_test_function,
    )
    if start_actor not in actor_graph:
        return None
    queue = [(start_actor, [start_actor])]
    visited_actors = set()
    while queue:
        current_actor, path = queue.pop(0)
        if goal_test(current_actor):
            return path
        neighbors = actor_graph.get(current_actor, set())
        for neighbor in neighbors:
            if neighbor not in visited_actors:
                queue.append((neighbor, path + [neighbor]))
                visited_actors.add(neighbor)
    return None


def actor_to_actor_path(transformed_data, actor_id_1, actor_id_2):
    """By BFS, Takes in graph, start actor, end actor
    Returns the shortest list from start to end actor"""

    def between_2(actor):
        return actor == actor_id_2

    return actor_path(transformed_data, actor_id_1, between_2)


def bacon_path(transformed_data, actor_id):
    """By BFS, Takes in graph and the end goal actor
    Returns one of the shortest list from kevin to end actor"""
    return actor_to_actor_path(transformed_data, 4724, actor_id)


def actors_with_bacon_number(transformed_data, n):
    """By BFS, Takes in graph and the bacon number of interest, n
    Returns  the set of all actors with bacon number n"""
    empty = set()
    for actor in transformed_data[0]:
        b_path = bacon_path(transformed_data, actor)
        if len(b_path) == n + 1:
            empty.add(actor)
    return empty
def actors_connecting_films(transformed_data, film1, film2):
    """Similar to opposite movie_paths, but uses inter_val to have size of paths
       and set1 as starting point, using optimal paths begining from set1"""
    set1, set2 = set(), set()
    for tups in transformed_data[1][film1]:
        set1.add(tups[0])
        set1.add(tups[1])
    for tups in transformed_data[1][film2]:
        set2.add(tups[0])
        set2.add(tups[1])
    list_paths = []
    def goal(actor_in):
        return actor_in in set2
    for actor in set1:
        list_paths.append(actor_path(transformed_data, actor, goal))
    return min(list_paths, key=lambda x: len(x) if isinstance(x, list) else float('inf'), default=None)
    
    

#########################################################################

if __name__ == "__main__":
    with open("resources/movies.pickle", "rb") as f:
        moviesdb = pickle.load(f)
    with open("resources/tiny.pickle", "rb") as f:
        tinydb = pickle.load(f)
    with open("resources/small.pickle", "rb") as f:
        smalldb = pickle.load(f)
    with open("resources/large.pickle", "rb") as f:
        largedb = pickle.load(f)
    print(smalldb[0][0])
    with open("resources/names.pickle", "rb") as f:
        namesdb = pickle.load(f)
    # assign my_iter to make next work
    my_iter = iter(namesdb.items())
    print(next(my_iter), next(my_iter))
    print(namesdb["Johnny Simmons"])
    # never make a list using[], use list()
    id_list, names_list, mid_list, movies_list = (
        list(namesdb.values()),
        list(namesdb.keys()),
        list(moviesdb.values()),
        list(moviesdb.keys()),
    )
    john_index = id_list.index(14673)
    print(names_list[john_index])
    # ###################################
    # test 1
    trans = transform_data(smalldb)
    boolean = acted_together(trans, namesdb["David Stevens"], namesdb["Barbra Rae"])
    print(boolean)
    # test 2
    boolean = acted_together(
        trans, namesdb["Jean Schmitt"], namesdb["Jean-Marc Roulot"]
    )
    print(boolean)
    # ###################################
    trans = transform_data(largedb)
    print(type(trans))
    deg_6_set = actors_with_bacon_number(trans, 6)
    # print(set([names_list[id_list.index(identity)] for identity in deg_6_set]))
    # ###################################
    # print(f"{namesdb['Daniel Johnson']=}")
    trans = transform_data(largedb)
    path = bacon_path(trans, 1389011)
    # print(path)
    print(
        [
            names_list[id_list.index(identity)]
            for identity in [4724, 13524, 1211, 1318329, 1365222, 1389011]
        ]
    )
    # ###################################
    # print(f"{namesdb['Venice Hayes']=}, {namesdb['Kevin Rice']=} ")
    # path = actor_to_actor_path(trans, 1395629, 58566)
    # print([names_list[id_list.index(identity)] for identity in path])
    # ###################################
    # print(f"{namesdb['Andy Milder']=}, {namesdb['Vjeran Tin Turk']=} ")
    # movies_ = movie_paths(trans, 1043304, 1367972)
    # print([movies_list[mid_list.index(identity)] for identity in movies_])

    # additional code here will be run only when lab.py is invoked directly
    # (not when imported from test.py), so this is a good place to put code
    # used, for example, to generate the results for the online questions.
    pass
