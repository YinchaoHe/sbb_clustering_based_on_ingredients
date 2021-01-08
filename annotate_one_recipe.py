import argparse
import json
import os
import recipe_ingredient_matrix_clean

def ingredient_transformation(recipe):
    ing_cleaner = recipe_ingredient_matrix_clean.get_ing_cleaner()
    converted_info = {}
    converted_info["recipe_ID"] = recipe["recipe_ID"].split("_")[1]
    converted_nutrition = []
    target_ingrs = recipe["ingredients"]
    with open("ingr_clusters.json") as f:
        data = json.load(f)

    for target_ingr in target_ingrs:
        target = False
        trans_target_ingr = ing_cleaner(target_ingr)
        for ingr_group in data.keys():
            for ingr in data[ingr_group]:
                if trans_target_ingr == ingr:
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
            ingredit_pair.append(trans_target_ingr)
            ingredit_pair.append(target_ingr)
            converted_nutrition.append(ingredit_pair)
            print("!!!Cannot find the target: " + target_ingr)

    converted_info["ingredients"] = converted_nutrition

    folder = "output_files/" + recipe["recipe_ID"].split("_")[0] + "_transformmation"
    try:
        os.mkdir(folder)
    except:
        pass

    folder = folder + '/' + recipe["recipe_ID"] + '.json'
    with open(folder, 'w') as f:
        json.dump(converted_info, f)
    return converted_info, folder

def search_nutrition(folder):
    nutrition = []
    with open(folder, 'r') as f:
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
        result = {"ingredient": figure_q}
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

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", required=True)
    args = parser.parse_args()

    with open(args.file, 'r') as f:
        recipe = json.load(f)
    try:
        os.mkdir("output_files")
    except:
        pass

    temp_recipe, folder = ingredient_transformation(recipe)
    nutrition = search_nutrition(folder)
    recipe_trans = {}
    recipe_trans['recipe_ID'] = temp_recipe['recipe_ID']
    recipe_trans["ingredients"] = {}
    index = 0
    for ingre in temp_recipe["ingredients"]:
        recipe_trans["ingredients"][ingre[1]] = nutrition[index]
        index += 1


    folder = "output_files/" + recipe["recipe_ID"].split("_")[0]
    try:
        os.mkdir(folder)
    except:
        pass

    with open(folder + '/' + recipe["recipe_ID"] + '.json', 'w') as f:
        json.dump(recipe_trans, f)

    print(temp_recipe['recipe_ID'])


if __name__ == '__main__':
    main()

