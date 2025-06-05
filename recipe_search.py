import requests

BASE_URL = "https://www.themealdb.com/api/json/v1/1/"
DB_INGREDIENT_KEYS = ["strIngredient1", "strIngredient2", "strIngredient3", "strIngredient4", "strIngredient5", 
                      "strIngredient6", "strIngredient7", "strIngredient8", "strIngredient9", "strIngredient10", 
                      "strIngredient11", "strIngredient12", "strIngredient13", "strIngredient14", "strIngredient15", 
                      "strIngredient16", "strIngredient17", "strIngredient18", "strIngredient19", "strIngredient20"]

class Recipe:
    def __init__(self, title, category, instructions, ingredients, picture, id):
        self.title = title
        self.category = category
        self.instructions = instructions
        self.ingredients = ingredients
        self.picture = picture
        self.id = id
    
    def print_recipe(self):
        print("Title: %s\n" % (self.title))
        print("Category: %s\n" % (self.category))
        print("Instructions: %s\n" % (self.instructions))
        print("Ingredients: %s\n" % (self.ingredients))
        print("Picture: %s\n" % (self.picture))

#Used for parsing the JSON data to get each ingredient as well as their amounts
#This is a messy way to do it but so is their JSON formatting
def _get_ingredients_from_recipe(recipe):
    ingredients = []

    for key, value in recipe.items():
        if key not in DB_INGREDIENT_KEYS or value is None or value == '':
            continue

        key_num = key.split("t")[2]
        measure_key = "strMeasure" + key_num

        ingredients.append(value + " " + recipe[measure_key])

    return ingredients

"""
Get a single random recipe.

:return: instance of the Recipe class, None for errors
"""
def get_random_recipe():
    try:
        url = BASE_URL + "random.php"
        response = requests.get(url)
        if response.status_code != requests.codes.ok:
            return None

        ret_recipe = response.json()["meals"][0]

        ingredients = _get_ingredients_from_recipe(ret_recipe)
        random_recipe = Recipe(ret_recipe["strMeal"], ret_recipe["strCategory"], ret_recipe["strInstructions"], ingredients, ret_recipe["strMealThumb"], ret_recipe["idMeal"])

        return random_recipe
    except:
        return None

"""
Get every recipe for a given search query.

:param search_query: user input to search the database on, a string
:return: an instance of the Recipe class for each found recipe, a list, None for errors
"""  
def search_recipes_by_name(search_query):
    try:
        url = BASE_URL + "search.php?s=" + search_query
        response = requests.get(url)
        if response.status_code != requests.codes.ok:
            return None

        ret_recipes = response.json()["meals"]

        recipes = []

        for recipe in ret_recipes:
            ingredients = _get_ingredients_from_recipe(recipe)
            recipes.append(Recipe(recipe["strMeal"], recipe["strCategory"], recipe["strInstructions"], ingredients, recipe["strMealThumb"], recipe["idMeal"]))

        return recipes
    except:
        return None

"""
Get a certain recipe based on its id

:param id: the id of the desired recipe, a string
:return: an instance of the Recipe class, None for errors
"""
def search_recipes_by_id(id):
    try:
        url = BASE_URL + "lookup.php?i=" + id
        response = requests.get(url)
        if response.status_code != requests.codes.ok:
            return None
        
        ret_recipe = response.json()["meals"]

        ingredients = _get_ingredients_from_recipe(ret_recipe)
        return Recipe(ret_recipe["strMeal"], ret_recipe["strCategory"], ret_recipe["strInstructions"], ingredients, ret_recipe["strMealThumb"], ret_recipe["idMeal"])
    except:
        return None

"""
Returns all of the ingredients available from the API.

:return: every available ingredient, a list of strings
"""
def get_all_ingredients():
    try:
        url = BASE_URL + "list.php?i=list"
        response = requests.get(url)
        if response.status_code != requests.codes.ok:
            return None

        return [item["strIngredient"] for item in response.json()["meals"]]
    except:
        return None

"""
Returns all of the categories available from the API.

:return: every available category, a list of strings
"""
def get_all_categories():
    try:
        url = BASE_URL + "list.php?c=list"
        response = requests.get(url)
        if response.status_code != requests.codes.ok:
            return None

        return [item["strCategory"] for item in response.json()["meals"]]
    except:
        return None

"""
Returns all of the areas available from the API.

:return: every available area, a list of strings
"""
def get_all_areas():
    try:
        url = BASE_URL + "list.php?a=list"
        response = requests.get(url)
        if response.status_code != requests.codes.ok:
            return None
        
        return [item["strArea"] for item in response.json()["meals"]]
    except:
        return None

def filter_recipes(ingredient_list):
    if not ingredient_list:
        return []
        
    # Convert first list's recipe IDs to a set
    recipe_ids = {recipe["idMeal"] for recipe in ingredient_list[0]}
    
    # Intersect with all other lists' recipe IDs
    for recipes in ingredient_list[1:]:
        if recipes is None:
            continue
        recipe_ids &= {recipe["idMeal"] for recipe in recipes}
    
    # Return recipes from first list that match final ID set
    return [recipe for recipe in ingredient_list[0] if recipe["idMeal"] in recipe_ids]

def filter_by_param(supported_set, params, ingredient_list, param_type):
    if not params:
        return True
        
    for param in params:
        # if param not found skip
        if param.lower() not in supported_set:
            continue

        param_str_filtered = param.lower().replace(" ", "_")
        
        # Use different endpoints based on parameter type
        if param_type == 'ingredient':
            url = BASE_URL + "filter.php?i=" + param_str_filtered
        elif param_type == 'category':
            url = BASE_URL + "filter.php?c=" + param_str_filtered
        elif param_type == 'area':
            url = BASE_URL + "filter.php?a=" + param_str_filtered

        try:
            response = requests.get(url)
            if response.status_code != requests.codes.ok:
                continue
            meals = response.json().get("meals")
            if meals:
                ingredient_list.append(meals)
        except:
            continue


"""
Find recipes based on which ingredients they require.

:param ingredients: ingredients to search the database for, a list of strings
:return: all recipes which feature all of the ingredients, a list of Recipe objects, None for errors
"""
def filter_by_ingredient(ingredients : list[str], categories : list[str] =None, areas=None):
    supported_ingredients = get_all_ingredients()
    supported_categories = get_all_categories()
    supported_areas = get_all_areas()

    supported_ingredients_filtered = set([ingredient.lower() for ingredient in supported_ingredients])
    supported_categories_filtered = set([category.lower() for category in supported_categories])
    supported_areas_filtered = set([area.lower() for area in supported_areas])

    ingredient_list = []
    # add ingredients obtained by ingredients
    filter_by_param(supported_ingredients_filtered, ingredients, ingredient_list, 'ingredient')
    # search ingredient list and return recipes that are present in all elements of the array
    
    # add ingredients obtained by categories
    filter_by_param(supported_categories_filtered, categories, ingredient_list, 'category')
        
    # add ingredients obtained by areas
    filter_by_param(supported_areas_filtered, areas, ingredient_list, 'area')

    print("Ingredient List: ", ingredient_list)
    
    return filter_recipes(ingredient_list)

#If you run this python file print out ingredient, category, area, and a basic ingredient search for debugging
if __name__ == "__main__":
    print("Ingredients: ")
    print(get_all_ingredients())
    print("Categories: ")
    print(get_all_categories())
    print("Areas: ")
    print(get_all_areas())
    print("Ingredient Search: ")
    print(filter_by_ingredient(["beef"], ["Beef"], ["American"]))

# Ingredient List:  [[{'strMeal': 'Brown Stew Chicken', 'strMealThumb': 'https://www.themealdb.com/images/media/meals/sypxpx1515365095.jpg', 'idMeal': '52940'}, {'strMeal': 'Chicken & mushroom Hotpot', 'strMealThumb': 'https://www.themealdb.com/images/media/meals/uuuspp1511297945.jpg', 'idMeal': '52846'}, {'strMeal': 'Chicken Alfredo Primavera', 'strMealThumb': 'https://www.themealdb.com/images/media/meals/syqypv1486981727.jpg', 'idMeal': '52796'}, {'strMeal': 'Chicken Basquaise', 'strMealThumb': 'https://www.themealdb.com/images/media/meals/wruvqv1511880994.jpg', 'idMeal': '52934'}, {'strMeal': 'Chicken Congee', 'strMealThumb': 'https://www.themealdb.com/images/media/meals/1529446352.jpg', 'idMeal': '52956'}, {'strMeal': 'Chicken Handi', 'strMealThumb': 'https://www.themealdb.com/images/media/meals/wyxwsp1486979827.jpg', 'idMeal': '52795'}, {'strMeal': 'Chicken Karaage', 'strMealThumb': 'https://www.themealdb.com/images/media/meals/tyywsw1505930373.jpg', 'idMeal': '52831'}, {'strMeal': 'Kentucky Fried Chicken', 'strMealThumb': 'https://www.themealdb.com/images/media/meals/xqusqy1487348868.jpg', 'idMeal': '52813'}, {'strMeal': 'Kung Pao Chicken', 'strMealThumb': 'https://www.themealdb.com/images/media/meals/1525872624.jpg', 'idMeal': '52945'}, {'strMeal': 'Pad See Ew', 'strMealThumb': 'https://www.themealdb.com/images/media/meals/uuuspp1468263334.jpg', 'idMeal': '52774'}, {'strMeal': 'Piri-piri chicken and slaw', 'strMealThumb': 'https://www.themealdb.com/images/media/meals/hglsbl1614346998.jpg', 'idMeal': '53039'}, {'strMeal': 'Thai Green Curry', 'strMealThumb': 'https://www.themealdb.com/images/media/meals/sstssx1487349585.jpg', 'idMeal': '52814'}], [{'strMeal': 'Chilli prawn linguine', 'strMealThumb': 'https://www.themealdb.com/images/media/meals/usywpp1511189717.jpg', 'idMeal': '52839'}, {'strMeal': 'Fettuccine Alfredo', 'strMealThumb': 'https://www.themealdb.com/images/media/meals/0jv5gx1661040802.jpg', 'idMeal': '53064'}, {'strMeal': 'Fettucine alfredo', 'strMealThumb': 'https://www.themealdb.com/images/media/meals/uquqtu1511178042.jpg', 'idMeal': '52835'}, {'strMeal': 'Grilled Mac and Cheese Sandwich', 'strMealThumb': 'https://www.themealdb.com/images/media/meals/xutquv1505330523.jpg', 'idMeal': '52829'}, {'strMeal': 'Lasagna Sandwiches', 'strMealThumb': 'https://www.themealdb.com/images/media/meals/xr0n4r1576788363.jpg', 'idMeal': '52987'}, {'strMeal': 'Lasagne', 'strMealThumb': 'https://www.themealdb.com/images/media/meals/wtsvxx1511296896.jpg', 'idMeal': '52844'}, {'strMeal': 'Pilchard puttanesca', 'strMealThumb': 'https://www.themealdb.com/images/media/meals/vvtvtr1511180578.jpg', 'idMeal': '52837'}, {'strMeal': 'Spaghetti alla Carbonara', 'strMealThumb': 'https://www.themealdb.com/images/media/meals/llcbn01574260722.jpg', 'idMeal': '52982'}, {'strMeal': 'Venetian Duck Ragu', 'strMealThumb': 'https://www.themealdb.com/images/media/meals/qvrwpt1511181864.jpg', 'idMeal': '52838'}]]