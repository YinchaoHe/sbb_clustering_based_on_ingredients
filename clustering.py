import pickle

import pandas as pd


def main():
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 1000)
    data = pd.read_pickle("recipe_ingredients_scaled_units_wide_df.pkl")
    print(data)
if __name__ == '__main__':
    main()