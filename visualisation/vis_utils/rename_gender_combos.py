import pandas as pd

def rename_gender_combos(input_item:pd.DataFrame|pd.Series, column=None):
    """
    takes a pandas item with an index (series or df) or a "gender_combo" column of gender combo labels

    defaults to renaming the index

    if a truthy value is given for column=, it will instead rename the "gender_combo" column

    returns a new item with its relevant gender combo labels renamed to match the other labels
    """

    renaming_dict = {
        "F / M": "M / F",
        "Ambig / M": "M / Ambig",
        "Ambig / F": "F / Ambig",
        "M | Other / M": "M / M | Other"
    }

    if column:
        new_item = input_item.copy()
        new_list = []
        for combo in new_item["gender_combo"]:
            if combo in renaming_dict.keys():
                new_list.append(renaming_dict[combo])
            else: new_list.append(combo)
        new_item["gender_combo"] = new_list

    else: new_item = input_item.rename(index=renaming_dict)

    return new_item