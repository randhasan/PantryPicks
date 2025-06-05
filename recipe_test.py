from recipe_search import *

#prompt user for query and get list from api
def get_recipes():
    query = input("Search for a recipe: ")
    recipes = search_recipes(query)
    
    #shorten array to 5 or less
    if len(recipes) > 5:
        recipes = recipes[:5]
    
    return recipes

#given the list of recipes, pick one and print details
#loop until 0 entered
def results_loop(recipes):
    length = len(recipes)

    while(True):
            print("\nHere are the first %d results:" % (length))
            for i in range(length):
                print("[%d] %s" % (i+1, recipes[i].title))
            print("[0] Back to Search")
                
            choice = int(input("Enter a number to see that recipe: "))
            if(choice == 0): break
            elif(choice > length or choice < 1): print("Invalid Number")
            else:
                selection = recipes[choice-1]
                selection.print_recipe()

def main():
    print("Welcome to Pantry Picks!")
    while(True):
        
        #search api
        recipes = get_recipes()
        #print results
        results_loop(recipes)
        
    
main()