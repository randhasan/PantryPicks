from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from recipe_search import *
from user import User
app = Flask(__name__)

recipes = []

app.secret_key = "key" 
users = {}

test_user_dylan = User("Dylan")

test_user_dylan.add_recipe(
    title="Classic Spaghetti Carbonara",
    category="Pasta",
    instructions="1. Cook spaghetti according to package instructions.\n"
                "2. In a bowl, whisk eggs and grated Pecorino Romano cheese.\n"
                "3. Cook pancetta or guanciale until crispy.\n"
                "4. Drain pasta, reserving some pasta water.\n"
                "5. Quickly mix hot pasta with egg mixture, adding pancetta and pasta water as needed.\n"
                "6. Season with black pepper and serve immediately.",
    ingredients=["400g spaghetti", 
                "200g pancetta or guanciale", 
                "4 large eggs",
                "100g Pecorino Romano cheese",
                "Freshly ground black pepper",
                "Salt"],
    picture="https://www.themealdb.com/images/media/meals/llcbn01574260722.jpg",
    id="53013"  
)


# Add test user to users dictionary
users["Dylan"] = test_user_dylan


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        username = request.form.get("username")
        session["username"] = username  
        if username not in users:
            users[username] = User(username)
            print(f"Created new user: {username}")
        else:
            print(f"Returning user: {username}")
        return redirect(url_for("recipes")) 
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/recipes")
def recipes():
    username = session.get("username")
    if not username or username not in users:
        return redirect(url_for("home"))  # go back if not logged in

    user = users[username]
    saved_recipes = user.get_recipes()

    return render_template("recipes.html", saved_recipes=saved_recipes)

@app.route("/add_recipe")
def add_recipe():
    return render_template("add_recipe.html")

@app.route("/search_recipe")
def search_recipe():
    return render_template("search_recipe.html")

@app.route("/view_recipe/<query>")
def view_recipe(query):
    try:
        found_recipes = search_recipes_by_name(query)
        if not found_recipes:
            return "Recipe not found", 404
            
        found_recipe = found_recipes[0]
        is_saved = False
        
        username = session.get("username")
        if username and username in users:
            user = users[username]
            is_saved = any(r.id == found_recipe.id for r in user.get_recipes())
        
        return render_template("view_recipe.html", 
                            recipe=found_recipe,
                            is_saved=is_saved,
                            recipe_source="api")
    except Exception as e:
        print(f"Error in view_recipe: {str(e)}")
        return "An error occurred while loading the recipe", 500

@app.route("/api/ingredients")
def get_ingredients():
    ingredients = get_all_ingredients()
    return jsonify(ingredients if ingredients else [])

@app.route("/api/categories")
def get_categories():
    categories = get_all_categories()
    return jsonify(categories if categories else [])

@app.route("/api/areas")
def get_areas():
    areas = get_all_areas()
    return jsonify(areas if areas else [])

@app.route("/api/search", methods=["POST"]) 
def search():
    data = request.get_json()
    
    ingredients = data.get("ingredients", [])
    categories = data.get("categories", [])
    areas = data.get("areas", [])
    #print debug info
    print("Ingredients: ", ingredients)
    print("Categories: ", categories)
    print("Areas: ", areas)
    if not ingredients:
        return jsonify({"error": "No ingredients provided"})
    
    results = filter_by_ingredient(ingredients, categories, areas)
    return jsonify(results if results else [])

@app.route("/view_saved_recipe/<recipe_id>")
def view_saved_recipe(recipe_id):
    try:
        username = session.get("username")
        if not username or username not in users:
            return redirect(url_for("home"))

        user = users[username]
        found_recipe = next((r for r in user.get_recipes() if r.id == recipe_id), None)
        
        if not found_recipe:
            return "Recipe not found", 404
            
        return render_template("view_recipe.html", 
                            recipe=found_recipe,
                            is_saved=True,
                            recipe_source="saved")
    except Exception as e:
        print(f"Error in view_saved_recipe: {str(e)}")
        return "An error occurred while loading the recipe", 500

@app.route("/save_recipe", methods=["POST"])
def save_recipe():
    username = session.get("username")
    if not username or username not in users:
        return jsonify({"success": False, "message": "Not logged in"}), 401
    
    data = request.get_json()
    user = users[username]
    
    # Check if recipe already exists
    if any(recipe.id == data['id'] for recipe in user.get_recipes()):
        return jsonify({"success": False, "message": "Recipe already saved"})
    
    # Add the recipe
    user.add_recipe(
        title=data['title'],
        category=data['category'],
        instructions=data['instructions'],
        ingredients=data['ingredients'],
        picture=data['picture'],
        id=data['id']
    )
    
    return jsonify({"success": True})

@app.route("/unsave_recipe", methods=["POST"])
def unsave_recipe():
    username = session.get("username")
    if not username or username not in users:
        return jsonify({"success": False, "message": "Not logged in"}), 401
    
    data = request.get_json()
    user = users[username]
    
    # Find and remove the recipe
    user.saved_recipes = [r for r in user.saved_recipes if r.id != data['id']]
    
    return jsonify({"success": True})

if __name__ == "__main__":
    app.run(debug=True)