from fastapi import FastAPI
import httpx
from fastapi.responses import HTMLResponse

app = FastAPI(title="Do you even Cook?")


async def get_recipe():
    url = "https://www.themealdb.com/api/json/v1/1/random.php"
    async with httpx.AsyncClient(timeout=10) as client:
        res = await client.get(url)
        data = res.json()
        meal = data["meals"][0]

    ingredients = []
    for i in range(1, 21):
        ingredient = meal.get(f"strIngredient{i}")
        measure = meal.get(f"strMeasure{i}")
        if ingredient and ingredient.strip():
            ingredients.append(f"{measure.strip()} {ingredient.strip()}")

    return {
        "name": meal["strMeal"],
        "category": meal["strCategory"],
        "area": meal["strArea"],
        "instructions": meal["strInstructions"],
        "image": meal["strMealThumb"],
        "ingredients": ingredients,
        "source": meal["strSource"]
    }


@app.get("/recipe")
async def recipe_json():
    return await get_recipe()


@app.get("/recipe/html", response_class=HTMLResponse)
async def recipe_html():
    recipe = await get_recipe()
    ingredient_list = "".join(
        [f"<li>{item}</li>" for item in recipe["ingredients"]])
    html = f"""
    <html>
    <head>
        <title>{recipe['name']} - Recipe</title>
        <style>
            body {{ font-family: Arial; margin: 30px; background-color: #fff7f0; color: #333; }}
            img {{ max-width: 400px; border-radius: 12px; }}
            h1 {{ color: #d35400; }}
            ul {{ list-style-type: circle; }}
        </style>
    </head>
    <body>
        <h1>{recipe['name']}</h1>
        <img src="{recipe['image']}" alt="Recipe Image">
        <p><strong>Category:</strong> {recipe['category']} | <strong>Area:</strong> {recipe['area']}</p>
        <h2>Ingredients</h2>
        <ul>{ingredient_list}</ul>
        <h2>Instructions</h2>
        <p>{recipe['instructions']}</p>
        <p><a href="{recipe['source']}" target="_blank">Source Link</a></p>
    </body>
    </html>
    """
    return html
