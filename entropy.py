import json
import math
import os


from pymongo import MongoClient

def main():
    folder = "ingr_entropy"
    try:
        os.mkdir(folder)
    except:
        print("The folder exists")

    client = MongoClient('mongodb://example:example@sbbi-panda.unl.edu:27017/')
    db = client.food
    recipes = db.recipe

    error_number = 0
    ingredients = []
    ingre_frequence = {}
    error_recipe_IDs = []
    amount_recipes = recipes.count_documents({})
    count = []

    for recipe in recipes.find():
        try:
            processed_ingrs = recipe['processed_ingredients']
            for processed_ingr in processed_ingrs:
                if processed_ingr not in ingredients:
                    ingredients.append(processed_ingr)
                    ingre_frequence[processed_ingr] = 1
                else:
                    ingre_frequence[processed_ingr] = ingre_frequence[processed_ingr] + 1
        except:
            error_recipe_IDs.append(recipe['recipe_ID'])
            error_number += 1
            pass
    for ingr in ingredients:
        ingre_frequence[ingr] = ingre_frequence[ingr] * 1.0  / amount_recipes
        count.append(ingre_frequence[ingr])

    print("Before Rank")
    print(ingre_frequence)
    print(ingredients)
    print(count)

    ingredients, count = bubble_sort(ingredients, count)

    print('After Rank: ')
    print(ingredients)
    print(count)

    ranked_ingre_freq = {}
    for ingredient in ingredients:
        ranked_ingre_freq[ingredient] = ingre_frequence[ingredient]

    print('---------------------------')
    print(ranked_ingre_freq)

    with open(folder + '/unranked_ingr_frequence.json', 'w') as f:
        json.dump(ingre_frequence, f)
    f.close()

    with open(folder + '/ranked_ingr_frequence.json', 'w') as f:
        json.dump(ranked_ingre_freq, f)
    f.close()

    ingre_entropy = ranked_ingre_freq.copy()
    for ingr in ingredients:
        ingre_entropy[ingr] = -math.log10(ingre_entropy[ingr])
    with open(folder + '/ranked_ingr_entropy.json', 'w') as f:
        json.dump(ingre_entropy, f)
    f.close()

    with open(folder + '/error_recipes.json', 'w') as f:
        errors = {"Number of errors: " : error_number}
        errors['error_recipe_IDs'] =  error_recipe_IDs

        json.dump(errors, f)
    f.close()

    print("error recipes' amount: " + str(error_number))


def bubble_sort(ingredients, count):
    number = len(ingredients)
    i = 0
    while i < number:
        j = i + 1
        while j < number:
            if count[i] < count[j]:
                temp_count = count[i]
                count[i] = count[j]
                count[j] = temp_count

                temp_ingre = ingredients[i]
                ingredients[i] = ingredients[j]
                ingredients[j] = temp_ingre
            j += 1
        i += 1

    return ingredients, count

if __name__ == '__main__':
    main()
