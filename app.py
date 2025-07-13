from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__, static_url_path='/static')

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        ingredient = request.form.get('ingredient', '').strip()
        dietary = request.form.get('dietary', '').strip().lower().replace(" ", "-")
        
        print(f"Received values - Ingredient: {ingredient}, Dietary: {dietary}")
        
        results = recipe_search(ingredient, dietary)
        return render_template('result.html', results=results, ingredient=ingredient, dietary=dietary)
    
    return render_template('index.html')


def recipe_search(ingredient, dietary):
    app_id = os.environ.get("APP_ID", "8ff0a5d9")  # fallback to hardcoded for local dev
    app_key = os.environ.get("APP_KEY", "0b2108368f934dab51af55fa03b1471d")

    base_url = "https://api.edamam.com/search"
    params = {
        "q": ingredient,
        "app_id": app_id,
        "app_key": app_key
    }

    if dietary:
        params["health"] = dietary  # Must be a valid Edamam "health" label like "low-fat", "vegan", etc.

    print(f"Requesting {base_url} with params: {params}")

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        print(f"Received {len(data.get('hits', []))} results")
        return data.get('hits', [])
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return []


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # For Render compatibility
    app.run(host="0.0.0.0", port=port)
