import math
import requests


def recipe_search(ingredient, max_ingredients):
    app_id = "18aca2a7"
    app_key = "464ebea5aa1a93828e3546b3c5d1e5b7"
    url = 'https://api.edamam.com/search?q={}&app_id={}&app_key={}&ingr={}'.format(ingredient, app_id, app_key,
                                                                                   max_ingredients)
    response = requests.get(url)
    data = response.json()
    return data["hits"]


def run():
    ingredient = input("What is the ingredient?: ")
    max_ingredients = int(input("Maximum number of ingredients?: "))
    results = recipe_search(ingredient, max_ingredients)
    open('recipes.txt', 'w').close()
    for result in results:
        recipe_set = result["recipe"]
        # for each recipe object in hits , pull off the label, uri, ingredients, number of servings and image
        recipe_name = recipe_set["label"].upper()
        recipe_link = recipe_set["uri"]
        recipe_ingredients = recipe_set["ingredientLines"]
        recipe_image = recipe_set["image"]
        recipe_yield = recipe_set["yield"]
        # for each recipe object in hits , calculate the calories per yield
        calories_yield = str(math.ceil((recipe_set["calories"]) / recipe_yield))
        # pull off total fat, protein and carbs per recipe as dictionaries
        recipe_fat = recipe_set["totalNutrients"]["FAT"]
        recipe_protein = recipe_set["totalNutrients"]["PROCNT"]
        recipe_carbohydrates = recipe_set["totalNutrients"]["CHOCDF"]

        # moving to a file

        f = open('recipes.txt', "a")
        f.write(recipe_name + "\n")
        f.write(recipe_link + "\n" * 2)
        f.write("Number of servings: " + str(int(recipe_yield)) + "\n" * 2)
        f.write("Ingredients:" + "\n" * 2)

        for item in recipe_ingredients:
            f.write(item + "\n")
        f.write("\n")
        f.write("Nutritional Information:" + "\n" * 2)
        f.write("Calories per serving: " + calories_yield + "\n")

        # Calculating nutrients per yield
        f.write(recipe_carbohydrates["label"] + " per serving: " + str(
            math.ceil((recipe_carbohydrates["quantity"]) / (result["recipe"]["yield"]))) + recipe_carbohydrates[
                    "unit"] + "\n")
        f.write(recipe_fat["label"] + " per serving: " + str(
            math.ceil((recipe_fat["quantity"]) / (result["recipe"]["yield"]))) + recipe_fat["unit"] + "\n")
        f.write(recipe_protein["label"] + " per serving: " + str(
            math.ceil((recipe_protein["quantity"]) / (result["recipe"]["yield"]))) + recipe_protein["unit"] + "\n" * 3)

        # Download image as a png file and call it by recipe name
        receive = requests.get(recipe_image)
        with open(r'{}.png'.format(recipe_name), 'wb') as f:
            f.write(receive.content)


run()
