import json
import os


def ingredient_transformation():
    converted_info = {}
    converted_info["recipe_ID"] = "263122"
    converted_nutrition = []
    target_ingrs = ['jicama', 'lime_zest', 'cilantro_leaves', 'garlic', 'ground_cumin', 'kosher_salt', "_ground_black_pepper",
                    'tequila', 'tequila', "tilapia", 'mexican_crema', 'chipotle_peppers_adobo_sauce', 'olive_oil',
                    'flour_tortillas', 'lettuce', 'tomato', 'lime', 'sss']
    with open("ingr_clusters.json") as f:
        data = json.load(f)

    for target_ingr in target_ingrs:
        target = False
        for ingr_group in data.keys():
            for ingr in data[ingr_group]:
                if target_ingr == ingr:
                    ingredit_pair = []
                    print("The targer belongs to: " + ingr_group)
                    ingredit_pair.append(ingr_group)
                    ingredit_pair.append(target_ingr)
                    converted_nutrition.append(ingredit_pair)
                    target = True
                    break

            if target == True:
                print("find the target: " + target_ingr)
                break
        if target == False:
            ingredit_pair = []
            ingredit_pair.append(target_ingr)
            ingredit_pair.append(target_ingr)
            converted_nutrition.append(ingredit_pair)
            print("!!!Cannot find the target: " + target_ingr)

    converted_info["ingredients"] = converted_nutrition
    with open("output_files/ingredient_transformation.json", 'w') as f:
        json.dump(converted_info, f)
    return converted_info

def search_nutrition():
    nutrition = []
    with open('output_files/ingredient_transformation.json') as f:
        data = json.load(f)
    for ingredient in data['ingredients']:
        dataType = "Branded"
        nutrition.append(search(ingredient, dataType))
    with open("output_files/ingredient_matching_" + dataType + ".json", 'w') as f:
        json.dump(nutrition, f)
    return nutrition
        
def search(ingredient, dataType):
    command = "curl -XPOST -H "
    figure_h = " \"Content-Type:application/json\""
    figure_q = ingredient[1].replace("_", " ")
    figure_d = " \'{\"query\": \"" + figure_q + "\", \"dataType\": [\"" + dataType + "\"], \"pageSize\":1,\"pageNumber\":1,\"sortOrder\": \"desc\"}\' "
    url = "https://api.nal.usda.gov/fdc/v1/foods/search?api_key=5XhH6rNR9dLzWtUTVvFIzhupntyAfUmnYHkv4gWF"
    command = command + figure_h + " -d " + figure_d + url
    print(command)
    os.system(command + "> temp_ingredient_nutrition_USDA.json")
    with open('temp_ingredient_nutrition_USDA.json') as f:
        data = json.load(f)
    os.remove('temp_ingredient_nutrition_USDA.json')
    try:
        data = data["foods"][0]
    except:
        result = {"ingredient": data["foodSearchCriteria"]["query"]}
        result['unitName'] = "Nofound"
        print(result)
        return result
    print(data["description"])
    try:
        result = {"ingredient": data["description"],
                  "portion": '100g'}
    except:
        result = {"ingredient": figure_q,
                  "portion": '100g'}
    nu_infos = []
    for nutrient in data["foodNutrients"]:
        nu_info = {}
        header = ['calories', 'TotalFat', 'SaturatedFat', 'Cholesterol', 'Sodium', 'Potassium', 'TotalCarbohydrates',
                  'Protein', 'Sugars', 'VitaminA']

        if nutrient['nutrientName'] == "Total lipid (fat)" or nutrient['nutrientName'] == "Fatty acids, total saturated" or nutrient['nutrientName'] == "Cholesterol" or nutrient['nutrientName'] == "Sodium, Na" or nutrient['nutrientName'] == "Potassium, K" or nutrient['nutrientName']  == "Carbohydrate, by difference" or \
                nutrient['nutrientName'] == "Protein" or nutrient['nutrientName']  == "Sugars, total including NLEA" or "Vitamin A" in nutrient['nutrientName']:
            try:
                nu_info['nutrientName'] = nutrient['nutrientName']
                nu_info['value'] =  nutrient['value']
                nu_info['unitName'] = nutrient['unitName']

            except:
                nu_info['nutrientName'] = "None"
                nu_info['value'] = 0
                nu_info['unitName'] = "None"

        if nu_info != {}:
            nu_infos.append(nu_info)
    result['nutrition'] = nu_infos
    print(result)
    return result

if __name__ == '__main__':
    temp_recipe = ingredient_transformation()
    nutrition = search_nutrition()
    recipe_trans = {}
    recipe_trans['recipe_ID'] = temp_recipe['recipe_ID']
    recipe_trans["ingredients"] = {}
    index = 0
    for ingre in temp_recipe["ingredients"]:
        recipe_trans["ingredients"][ingre[1]] = nutrition[index]
        index += 1
    with open('output_files/recipe_annotation.json', 'w') as f:
        json.dump(recipe_trans, f)