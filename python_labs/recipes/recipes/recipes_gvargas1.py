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
            _, name, cost = rec
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
    Given a recipes list, the name of a particular food item, and an 
    optional iterable of food items to ignore,return the minimum cost 
    required to make that food item (by purchasing all necessary atomic 
    items) along with the list of atomic ingredients and their costs.
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
    #LL of dict, each inner represents ingredients and dict's are possibilities
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
        #iter on food item's list of list of tuples(ingre,quant), inner list is recipe
        for recipe in comp.get(food_item, []):
            recipe_combinations = []
            for ingredient, ingredient_quantity in recipe:
                ingredient_recipes = generate_flat_recipes(
                    ingredient, ingredient_quantity * quantity, forbidden
                )
                if not ingredient_recipes:
                    break
                recipe_combinations.append(ingredient_recipes)
            #finished with a recipe(inner list) in list of list of tuples
            #so take this list of list of dictionaries and make all combos
            else:
                for combination in combined_flat_recipes(recipe_combinations):
                    flat_recipes.append(combination)
        #return 
        return flat_recipes

    return generate_flat_recipes(food_item, 1, forbidden)


def scaled_flat_recipe(flat_recipe, n):
    """
    Given a dictionary of ingredients mapped to quantities needed, returns a
    new dictionary with the quantities scaled by n.
    """
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

if __name__ == "__main__":
    # # load example recipes from section 3 of the write-up
    # with open("test_recipes/example_recipes.pickle", "rb") as f:
    #     example_recipes = pickle.load(f)
    # print(sum([val for key, val in atomic_ingredient_costs(example_recipes).items()]))
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
    # print(scaled_flat_recipe(soup, 3))
    # you are free to add additional testing code here!
