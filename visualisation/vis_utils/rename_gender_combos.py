import pandas as pd

def rename_gender_combos(input_item:pd.DataFrame|pd.Series):
    """
    takes a pandas item with an index (series or df) with gender combo index labels

    returns a new item with its index labels renamed to match their equivalent labels
    """

    renaming_dict = {
        "F / M": "M / F",
        "Ambig / M": "M / Ambig",
        "Ambig / F": "F / Ambig",
        "M | Other / M": "M / M | Other"
    }

    new_item = input_item.rename(index=renaming_dict)

    return new_item