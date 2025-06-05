import string
import recipe_search

class User:
    def __init__(self, name):
        self.name = name
        self.saved_recipes = []
        self.ingredients = []
        self.allergens = []
        self.preferences = []
#-------RECIPES------------------
    #add new recipe
    def add_recipe(self, title, category, instructions, ingredients, picture, id):
        #turn into recipe object and add to saved recipes
        recipe = recipe_search.Recipe(title, category, instructions, ingredients, picture, id)
        self.saved_recipes.append(recipe)
    def save_recipe(self, recipe):
    #adds a recipe to saved recipes
        self.saved_recipes.append(recipe)
    #return all saved recipes for user
    def get_recipes(self):
        return self.saved_recipes
#--------------------------------

#---------INGREDIENTS------------
    #adds ingredient to the user's list
    def add_ingredient(self, ingredient):
        self.ingredients.append(ingredient.lower())
    
    #removes ingredient from user list
    #ideally the 'ingredient' input is chosen out of a list of ingredients that already exist
    def rem_ingredient(self, ingredient):
        self.ingredients.remove(ingredient)
        
    def get_ingredients(self):
        return self.ingredients
#--------------------------------

#----------ALLERGENS-------------

    #adds allergen to the user's list
    def add_allergen(self, allergen):
        self.allergens.append(allergen.lower())
    
    #removes allergen from user list
    #ideally the 'allergen' input is chosen out of a list of ingredients that already exist
    def rem_allergen(self, allergen):
        self.allergens.remove(allergen)
        
    def get_allergens(self):
        return self.allergens
#--------------------------------

#---------PREFERENCES------------

    #adds preference to the user's list
    def add_preference(self, preference):
        self.preferences.append(preference.lower())
    
    #removes preference from user list
    #ideally the 'preference' input is chosen out of a list of ingredients that already exist
    def rem_preference(self, preference):
        self.preferences.remove(preference)
        
    def get_preferences(self):
        return self.preferences
#--------------------------------

        