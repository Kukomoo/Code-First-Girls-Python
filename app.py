

from flask import Flask, render_template, request
import requests

app = Flask(__name__, static_url_path='/static') #everything you need to run this file 

@app.route("/", methods=['GET', 'POST']) #python Decorator adds more functionality (the place to go)

def index():
    if request.method == 'POST':
        ingredient = request.form['ingredient']
        dietary = request.form['dietary']
        # testing to make sure the values are grabbed
        print(f"Received values - Ingredient: {ingredient}, Dietary: {dietary}")
        results = recipe_search(ingredient, dietary)
        return render_template('result.html', results=results, ingredient=ingredient, dietary=dietary)
    return render_template('index.html')


def recipe_search(ingredient, dietary):
    
    app_id = "8ff0a5d9"
    app_key = "0b2108368f934dab51af55fa03b1471d"

    
    result = requests.get('https://api.edamam.com/search?q={}%2C{}&app_id={}&app_key={}'.format(ingredient, dietary, app_id, app_key))

    # Check if the request was successful (status code 200)
    if result.status_code == 200:
        # Parse the JSON data from the API response
        data = result.json()
        # Return the 'hits' part of the API response, assumed to contain recipe information
        return data.get('hits', [])
    else:
        # If the request was not successful, print an error message and return an empty list
        print(f"Error: Unable to fetch recipes. Status Code: {result.status_code}")
        return []

import os

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
