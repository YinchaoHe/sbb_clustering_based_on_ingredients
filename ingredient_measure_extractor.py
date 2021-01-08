import json
import os

def main():
    command = "find . -name *Recipes*.json > recipes_path.txt"
    os.system(command)
    with open("recipes_path.txt") as f:
        paths = f.readlines()

    try:
        os.mkdir('input')
    except:
        print('this folder exists')

    for path in paths:
        print(path)
        path = path.replace('\n', '')
        folder = 'input/' + path.split("./")[1].split("_text")[0]
        subfolder = folder + "/" + path.split("Recipes_")[2].split("_")[0]
        try:
            os.mkdir(folder)
        except:
            print('this folder exists')
        try:
            os.mkdir(subfolder)
        except:
            print('this folder exists')

        with open(path) as f:
            recipes = json.load(f)
        for recipe in recipes:
            recipe_ID = recipe["recipe_ID"]
            recipe_ingredients = recipe["ingredients"]
            file = open(subfolder + '/' + recipe_ID+'.txt', 'w', encoding='utf-8')

            for recipe_ingredient in recipe_ingredients:
                file.write(recipe_ingredient + '\n')
            file.close()



if __name__ == '__main__':
    main()
