from flask import Flask, jsonify, request
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'recipedb'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/recipedb'

mongo = PyMongo(app)


@app.route('/recipes', methods=['GET'])  # get all Recipes
def get_recipe_list():
	recipes = mongo.db.recipes
	output = []
	for recipe in recipes.find():
		output.append({'name': recipe['name'], 'ingredients': recipe['ingredients'], 'quantity': recipe['quantity']})

	return jsonify({'result': output})


@app.route('/recipe/<name>', methods=['GET'])  # get Recipe by name
def get_recipe(name=None):
	recipes = mongo.db.recipes
	recipe = recipes.find_one({'name' : name.lower()})
	if recipe:
		output = {'name': recipe['name'], 'ingredients': recipe['ingredients'], 'quantity': recipe['quantity']}
	else:
		output = "Not found"
	return jsonify({'result': output})


@app.route('/recipe/ingredients/<name>', methods=['GET'])  # get all recipes with all ingredients
def get_recipe_from_ingredients(name=None):
	name = name.lower().split(',')
	recipes = mongo.db.recipes
	output = []
	for recipe in recipes.find({'ingredients': {'$all': name}}):
		output.append({'name': recipe['name'], 'ingredients': recipe['ingredients'], 'quantity': recipe['quantity']})

	return jsonify({'result': output})


@app.route('/recipes/ingredients/<name>', methods=['GET'])  # get list of Recipes containing at least 1 ingredient
def get_recipes_from_ingredients(name=None):
	names = name.lower().split(',')
	recipes = mongo.db.recipes
	output = []
	for name in names:
		for recipe in recipes.find({'ingredients': name}):
			if output.__contains__({'name': recipe['name'], 'ingredients': recipe['ingredients'], 'quantity': recipe['quantity']}):
				continue
			else :
				output.append({'name': recipe['name'], 'ingredients': recipe['ingredients'], 'quantity': recipe['quantity']})

	return jsonify({'result': output})


@app.route('/recipes/ingredients/<name>/<qty>', methods=['GET'])  # get list of Recipes containing at least 1 ingredient
def get_recipes_from_ingredients_and_quantity(name=None, qty=None):
	names = name.lower().split(',')
	qtys = qty.lower().split(',')
	recipes = mongo.db.recipes
	output = []
	for i in range(0,len(names)):
		for recipe in recipes.find({'ingredients': names[i], 'quantity': qtys[i]}):
			if output.__contains__({'name': recipe['name'], 'ingredients': recipe['ingredients'], 'quantity': recipe['quantity']}):
				continue
			else :
				output.append({'name': recipe['name'], 'ingredients': recipe['ingredients'], 'quantity': recipe['quantity']})

	return jsonify({'result': output})


@app.route('/recipe', methods=['Post'])  # add new recipe
def add_recipe():
	recipes = mongo.db.recipes
	name = request.json['name'].lower()
	ingredients = request.json['ingredients'].lower()
	quantity = request.json['quantity'].lower()
	recipe_id = recipes.insert({'name': name, 'ingredients': ingredients, 'quantity': quantity})
	new_recipe = recipes.find_one({'_id': recipe_id})
	output = {'name': new_recipe['name'], 'ingredients': new_recipe['ingredients'], 'quantity': new_recipe['quantity']}
	return jsonify({'result': output})


if __name__ == '__main__':
	app.run()