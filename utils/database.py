import pandas as pd
from rapidfuzz import process


class IngredientDatabase:

    def __init__(self, csv_path):
        self.df = pd.read_csv(csv_path)

        # Make all ingredient names uppercase
        self.df["ingredient"] = self.df["ingredient"].astype(str).str.upper()

        self.ingredients = self.df["ingredient"].tolist()

    def search(self, ingredient):

        ingredient = ingredient.upper().strip()

        match = process.extractOne(
            ingredient,
            self.ingredients,
            score_cutoff=70
        )

        if match is None:
            return None

        row = self.df[self.df["ingredient"] == match[0]].iloc[0]

        return row.to_dict()