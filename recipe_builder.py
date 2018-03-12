from flask import Flask, jsonify, request
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'recipedb'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/recipedb'

mongo = PyMongo(app)


@app.route('/recipe', methods=['GET'])  # get Recipes
def get_recipe_list():
	recipes = mongo.db.recipes
	output = []
	for recipe in recipes.find():
		output.append({'name': recipe['name'], 'ingredients': recipe['ingredients'], 'quantity': recipe['quantity']})

	return jsonify({'result': output})


@app.route('/recipe/<name>', methods=['GET'])  # get Recipe
def get_recipe(name=None):
	recipes = mongo.db.recipes
	recipe = recipes.find_one({'name' : name})
	if recipe:
		output = {'name': recipe['name'], 'ingredients': recipe['ingredients'], 'quantity': recipe['quantity']}
	else:
		output = "Not found"
	return jsonify({'result': output})


@app.route('/recipe/ingredients/<name>', methods=['GET'])  # get Recipe from ingredient
def get_recipe_from_ingredients(name=None):
	name = name.split(',')
	recipes = mongo.db.recipes
	output = []
	for recipe in recipes.find({'ingredients': {'$all': name}}):
		output.append({'name': recipe['name'], 'ingredients': recipe['ingredients'], 'quantity': recipe['quantity']})

	return jsonify({'result': output})


@app.route('/recipe', methods=['Post'])  # add recipe
def add_recipe():
	recipes = mongo.db.recipes
	name = request.json['name']
	ingredients = request.json['ingredients']
	quantity = request.json['quantity']
	recipe_id = recipes.insert({'name': name, 'ingredients': ingredients, 'quantity': quantity})
	new_recipe = recipes.find_one({'_id': recipe_id})
	output = {'name': new_recipe['name'], 'ingredients': new_recipe['ingredients'], 'quantity': new_recipe['quantity']}
	return jsonify({'result': output})


if __name__ == '__main__':
	app.run()