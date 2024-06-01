"""
6.101 Lab 5:
Recipes
"""

import pickle
import sys

sys.setrecursionlimit(20_000)
# NO ADDITIONAL IMPORTS!


def atomic_ingredient_costs(recipes):
    """
    Given a recipes list, make and return a dictionary mapping each atomic food item
    name to its cost.
    """
    atom_costs = {}

    for rec in recipes:
        if rec[0] == "atomic":
            __, name, cost = rec
            atom_costs[name] = cost

    return atom_costs


def compound_ingredient_possibilities(recipes):
    """
    Given recipes, a list containing compound and atomic food items, make and
    return a dictionary that maps each compound food item name to a list
    of all the ingredient lists associated with that name.
    """
    comp = {}

    for rec in recipes:
        if rec[0] == "compound":
            _, name, recipes = rec
            if name not in comp:
                comp[name] = []
            comp[name].append(recipes)

    return comp


def lowest_coster(recipes, food_item, forbidden=None):
    """
    Given a recipes list, the name of a particular food item, and an optional iterable of food items to ignore,
    return the minimum cost required to make that food item (by purchasing all necessary atomic items)
    along with the list of atomic ingredients and their costs.
    """
    atom_costs = atomic_ingredient_costs(recipes)
    comp = compound_ingredient_possibilities(recipes)

    def calculate_cost_and_ingredients(food_item, forbidden=None):
        if food_item not in atom_costs and food_item not in comp:
            return None, None

        if forbidden and food_item in forbidden:
            return None, None

        if food_item in atom_costs:
            return atom_costs[food_item], [(food_item, 1)]

        min_cost = float("inf")
        min_ingredients = None
        for recipe in comp.get(food_item, []):
            total_cost = 0
            ingredients = []
            valid_recipe = True
            for ingredient, quantity in recipe:
                if (
                    (forbidden and ingredient in forbidden)
                    or ingredient not in atom_costs
                    and ingredient not in comp
                ):
                    valid_recipe = False
                    break

                ingredient_cost, ingredient_list = calculate_cost_and_ingredients(
                    ingredient, forbidden
                )
                if ingredient_cost is None:
                    valid_recipe = False
                    break

                total_cost += quantity * ingredient_cost
                ingredients.extend(
                    [
                        (atom, quantity * atom_cost)
                        for atom, atom_cost in ingredient_list
                    ]
                )

            if valid_recipe and total_cost < min_cost:
                min_cost = total_cost
                min_ingredients = ingredients

        if min_cost == float("inf"):
            min_cost = None
            min_ingredients = None

        return min_cost, min_ingredients

    atom_costs = atomic_ingredient_costs(recipes)
    comp = compound_ingredient_possibilities(recipes)
    min_cost, min_ingredients = calculate_cost_and_ingredients(food_item, forbidden)
    return min_cost, min_ingredients


def lowest_cost(recipes, food_item, forbidden=None):
    return lowest_coster(recipes, food_item, forbidden)[0]


def cheapest_flat_recipe(recipes, food_item, forbidden=None):
    """
    Given a recipes list and the name of a food item, return a dictionary
    (mapping atomic food items to quantities) representing the cheapest full
    recipe for the given food item.

    Returns None if there is no possible recipe.
    """
    min_cost, min_ingredients = lowest_coster(recipes, food_item, forbidden)
    if min_cost is None or min_ingredients is None:
        return None

    atomic_quantities = {}

    for ingredient, quantity in min_ingredients:
        if ingredient in atomic_quantities:
            atomic_quantities[ingredient] += quantity
        else:
            atomic_quantities[ingredient] = quantity

    return atomic_quantities


def combined_flat_recipes(flat_recipes):
    """
    Given a list of lists of dictionaries, where each inner list represents all
    the flat recipes for a certain ingredient, compute and return a list of flat
    recipe dictionaries that represent all the possible combinations of
    ingredient recipes.
    """
    if not flat_recipes:
        return [{}]

    first_list = flat_recipes[0]

    remaining_combinations = combined_flat_recipes(flat_recipes[1:])

    combined_recipes = []

    for recipe in first_list:
        for remaining_combination in remaining_combinations:
            combined_recipe = {}
            combined_recipe.update(recipe)
            for key, value in remaining_combination.items():
                if key in combined_recipe:
                    combined_recipe[key] += value
                else:
                    combined_recipe[key] = value
            combined_recipes.append(combined_recipe)

    return combined_recipes


"""x= [
    {'chocolate chips': 6, 'vanilla ice cream': 3},
    {'chocolate chips': 6, 'chocolate ice cream': 3},
    {'sugar': 20, 'vanilla ice cream': 3},
    {'sugar': 20, 'chocolate ice cream': 3}
]
print('YYY')
print(combined_flat_recipes([x]))
"""


def all_flat_recipes(recipes, food_item, forbidden=None):
    """
    Given a list of recipes and the name of a food item, produce a list of all possible
    flat recipes for that category, where each recipe is represented as a dictionary
    containing the atomic ingredients and their quantities.

    Returns a list of dictionaries, where each dictionary represents a flat recipe.
    """

    atom_costs = atomic_ingredient_costs(recipes)
    comp = compound_ingredient_possibilities(recipes)

    def generate_flat_recipes(food_item, quantity, forbidden=None):
        if forbidden and food_item in forbidden:
            return []

        if food_item in atom_costs:
            return [{food_item: quantity}]

        flat_recipes = []
        for recipe in comp.get(food_item, []):
            recipe_combinations = []
            for ingredient, ingredient_quantity in recipe:
                ingredient_recipes = generate_flat_recipes(
                    ingredient, ingredient_quantity * quantity, forbidden
                )
                if not ingredient_recipes:
                    break
                recipe_combinations.append(ingredient_recipes)
            else:
                for combination in combined_flat_recipes(recipe_combinations):
                    flat_recipes.append(combination)

        return flat_recipes

    return generate_flat_recipes(food_item, 1, forbidden)


"""example_recipes = [
    (
        "compound",
        "chili",
        [
            ("beans", 3),
            ("cheese", 10),
            ("chili powder", 1),
            ("cornbread", 2),
            ("protein", 1),
        ],
    ),
    ("atomic", "beans", 5),
    (
        "compound",
        "cornbread",
        [("cornmeal", 3), ("milk", 1), ("butter", 5), ("salt", 1), ("flour", 2)],
    ),
    ("atomic", "cornmeal", 7.5),
    (
        "compound",
        "burger",
        [("bread", 2), ("cheese", 1), ("lettuce", 1), ("protein", 1), ("ketchup", 1)],
    ),
    (
        "compound",
        "burger",
        [
            ("bread", 2),
            ("cheese", 2),
            ("lettuce", 1),
            ("protein", 2),
        ],
    ),
    ("atomic", "lettuce", 2),
    ("compound", "butter", [("milk", 1), ("butter churn", 1)]),
    ("atomic", "butter churn", 50),
    ("compound", "milk", [("cow", 1), ("milking stool", 1)]),
    ("compound", "cheese", [("milk", 1), ("time", 1)]),
    ("compound", "cheese", [("cutting-edge laboratory", 11)]),
    ("atomic", "salt", 1),
    ("compound", "bread", [("yeast", 1), ("salt", 1), ("flour", 2)]),
    ("compound", "protein", [("cow", 1)]),
    ("atomic", "flour", 3),
    ("compound", "ketchup", [("tomato", 30), ("vinegar", 5)]),
    ("atomic", "chili powder", 1),
    (
        "compound",
        "ketchup",
        [("tomato", 30), ("vinegar", 3), ("salt", 1), ("sugar", 2), ("cinnamon", 1)],
    ),  # the fancy ketchup
    ("atomic", "cow", 100),
    ("atomic", "milking stool", 5),
    ("atomic", "cutting-edge laboratory", 1000),
    ("atomic", "yeast", 2),
    ("atomic", "time", 10000),
    ("atomic", "vinegar", 20),
    ("atomic", "sugar", 1),
    ("atomic", "cinnamon", 7),
    ("atomic", "tomato", 13),
]
cookie_recipes = [
    ('compound', 'cookie sandwich', [('cookie', 2), ('ice cream scoop', 3)]),
    ('compound', 'cookie', [('chocolate chips', 3)]),
    ('compound', 'cookie', [('sugar', 10)]),
    ('atomic', 'chocolate chips', 200),
    ('atomic', 'sugar', 5),
    ('compound', 'ice cream scoop', [('vanilla ice cream', 1)]),
    ('compound', 'ice cream scoop', [('chocolate ice cream', 1)]),
    ('atomic', 'vanilla ice cream', 20),
    ('atomic', 'chocolate ice cream', 30),
]
print('ah')
print(all_flat_recipes(cookie_recipes, 'cookie sandwich'))
print('ah')
print(all_flat_recipes(cookie_recipes, 'cookie sandwich', ('sugar', 'chocolate ice cream')))
"""


def scaled_flat_recipe(flat_recipe, n):
    """
    Given a dictionary of ingredients mapped to quantities needed, returns a
    new dictionary with the quantities scaled by n.
    """
    # scaled_recipe = {}
    # for ingredient, quantity in flat_recipe.items():
    #     scaled_recipe[ingredient] = quantity * n
    # return scaled_recipe
    return {item: quantity * n for item, quantity in flat_recipe.items()}


def add_flat_recipes(flat_recipes):
    """
    Given a list of flat_recipe dictionaries that map food items to quantities,
    return a new overall 'grocery list' dictionary that maps each ingredient name
    to the sum of its quantities across the given flat recipes.

    For example,
        add_flat_recipes([{'milk':1, 'chocolate':1}, {'sugar':1, 'milk':2}])
    should return:
        {'milk':3, 'chocolate': 1, 'sugar': 1}
    """

    result = {}
    for flats in flat_recipes:
        for meal, value in flats.items():
            if meal in result:
                result[meal] += value
            else:
                result[meal] = value
    return result


"""example_recipes = [
    (
        "compound",
        "chili",
        [
            ("beans", 3),
            ("cheese", 10),
            ("chili powder", 1),
            ("cornbread", 2),
            ("protein", 1),
        ],
    ),
    ("atomic", "beans", 5),
    (
        "compound",
        "cornbread",
        [("cornmeal", 3), ("milk", 1), ("butter", 5), ("salt", 1), ("flour", 2)],
    ),
    ("atomic", "cornmeal", 7.5),
    (
        "compound",
        "burger",
        [("bread", 2), ("cheese", 1), ("lettuce", 1), ("protein", 1), ("ketchup", 1)],
    ),
    (
        "compound",
        "burger",
        [
            ("bread", 2),
            ("cheese", 2),
            ("lettuce", 1),
            ("protein", 2),
        ],
    ),
    ("atomic", "lettuce", 2),
    ("compound", "butter", [("milk", 1), ("butter churn", 1)]),
    ("atomic", "butter churn", 50),
    ("compound", "milk", [("cow", 1), ("milking stool", 1)]),
    ("compound", "cheese", [("milk", 1), ("time", 1)]),
    ("compound", "cheese", [("cutting-edge laboratory", 11)]),
    ("atomic", "salt", 1),
    ("compound", "bread", [("yeast", 1), ("salt", 1), ("flour", 2)]),
    ("compound", "protein", [("cow", 1)]),
    ("atomic", "flour", 3),
    ("compound", "ketchup", [("tomato", 30), ("vinegar", 5)]),
    ("atomic", "chili powder", 1),
    (
        "compound",
        "ketchup",
        [("tomato", 30), ("vinegar", 3), ("salt", 1), ("sugar", 2), ("cinnamon", 1)],
    ),  # the fancy ketchup
    ("atomic", "cow", 100),
    ("atomic", "milking stool", 5),
    ("atomic", "cutting-edge laboratory", 1000),
    ("atomic", "yeast", 2),
    ("atomic", "time", 10000),
    ("atomic", "vinegar", 20),
    ("atomic", "sugar", 1),
    ("atomic", "cinnamon", 7),
    ("atomic", "tomato", 13),
]
comp = compound_ingredient_possibilities(example_recipes)
atom = atomic_ingredient_costs(example_recipes)"""


"""cake_recipes = [{"cake": 1}, {"gluten free cake": 1}]
icing_recipes = [{"vanilla icing": 1}, {"cream cheese icing": 1}]
topping_recipes = [{"sprinkles": 20}]
print(combined_flat_recipes([cake_recipes, icing_recipes, topping_recipes]))"""


if __name__ == "__main__":
    # # load example recipes from section 3 of the write-up
    # with open("test_recipes/example_recipes.pickle", "rb") as f:
    #     example_recipes = pickle.load(f)
    # print(sum([val for key, val in atomic_ingredient_costs(example_recipes).items()]))
    # print(len([key for key, val in compound_ingredient_possibilities(example_recipes).items() if len(val)>1]))
    carrot_cake = {
        "carrots": 5,
        "flour": 8,
        "sugar": 10,
        "oil": 5,
        "eggs": 4,
        "salt": 3,
    }
    bread = {"flour": 10, "sugar": 3, "oil": 3, "yeast": 15, "salt": 5}
    soup = {
        "carrots": 5,
        "celery": 3,
        "broth": 2,
        "noodles": 1,
        "chicken": 3,
        "salt": 10,
    }
    grocery_list = [soup, carrot_cake, bread]
    # print(sorted(add_flat_recipes(grocery_list)) == sorted({"carrots": 10, "flour":18, "sugar": 13, "oil": 8, "eggs":4 , "salt":18, "yeast": 15, "celery":3, "broth":2, "noodles":1, "chicken":3, }))
    # print(scaled_flat_recipe(soup, 3))
    # you are free to add additional testing code here!
