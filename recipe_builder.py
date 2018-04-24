from flask import Flask, jsonify, request
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'recipedb'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/recipedb'

mongo = PyMongo(app)


@app.route('/getRecipes', methods=['GET'])  # get all Recipes
def get_recipe_list():
	recipes = mongo.db.recipes
	output = []
	for recipe in recipes.find():
	    output.append({'name': recipe['name'], 'category': recipe['category'], 'image': recipe['image'], 'ingredients': recipe['ingredients'], 'rating': recipe['rating']})
	return jsonify({'result': output})


@app.route('/getRecipeByName/<name>', methods=['GET'])  # get Recipe by name
def get_recipe(name=None):
	recipes = mongo.db.recipes
	recipe = recipes.find_one({'name' : name.lower()})
	if recipe:
	    output = {'name': recipe['name'], 'category': recipe['category'], 'image': recipe['image'], 'ingredients': recipe['ingredients'], 'rating': recipe['rating']}
	else:
	    output = "Not found"
	return jsonify({'result': output})


@app.route('/getRecipesByCategory/<category>', methods=['GET'])  # get all recipes by category
def get_recipes_by_category(category=None):
	category = category.lower()
	recipes = mongo.db.recipes
	output = []
	for recipe in recipes.find({'category': {'$all': category}}):
	    output.append({'name': recipe['name'], 'category': recipe['category'], 'image': recipe['image'], 'ingredients': recipe['ingredients'], 'rating': recipe['rating']})
	return jsonify({'result': output})


@app.route('/getRecipesByRating/<rating>', methods=['GET'])  # get all recipes by rating
def get_recipes_by_rating(rating=None):
	rating = rating.lower()
	recipes = mongo.db.recipes
	output = []
	for recipe in recipes.find({'rating': {'$all': rating}}):
	    output.append({'name': recipe['name'], 'category': recipe['category'], 'image': recipe['image'], 'ingredients': recipe['ingredients'], 'rating': recipe['rating']})
	return jsonify({'result': output})
	

@app.route('/addRecipe', methods=['Post'])  # add new recipe
def add_recipe():
	recipes = mongo.db.recipes
	name = request.json['name'].lower()
	category = request.json['category'].lower()
	image = request.json['image'].lower()
	ingredients = request.json['ingredients'].lower()
	rating = request.json['rating'].lower()
	recipe_id = recipes.insert({'name': name, 'category': category, 'image': image, 'ingredients': ingredients, 'rating': rating})
	new_recipe = recipes.find_one({'_id': recipe_id})
	output = {'name': new_recipe['name'], 'category': new_recipe['category'], 'image': new_recipe['image'], 'ingredients': new_recipe['ingredients'], 'rating': new_recipe['rating']}
	return jsonify({'result': output})


if __name__ == '__main__':
	app.run()