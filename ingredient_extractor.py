import argparse
import json
import os

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", required=True)
    args = parser.parse_args()

    file = args.file.split("/")[-1].split(".json")[0]

    with open(args.file, 'r') as f:
        js = json.load(f)

    js_ = []
    for x in js:
        try:
            if "cups" in x['name']:
                js_.append(x['name'].split("cups ")[1])
            elif "cup" in x['name']:
                js_.append(x['name'].split("cup ")[1])
            elif "tablespoons" in x['name']:
                js_.append(x['name'].split("tablespoons ")[1])
            elif "tablespoon" in x['name']:
                js_.append(x['name'].split("tablespoon ")[1])
            else:
                js_.append(x['name'])
        except:
            pass
    recipe = {"recipe_ID": file}
    recipe["ingredients"] = js_

    try:
        os.mkdir("targets")
    except:
        print('this folder exists')
    try:
        os.mkdir("targets/" + file.split("_")[0])
    except:
        print('this folder exists')

    with open("targets/" + file.split("_")[0] + "/" + file + '.json', 'w') as f:
       json.dump(recipe, f)

if __name__ == '__main__':
    main()