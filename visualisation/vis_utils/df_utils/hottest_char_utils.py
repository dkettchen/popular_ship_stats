from visualisation.vis_utils.df_utils.retrieve_numbers import get_unique_values_list
import pandas as pd

def unify_doctors_and_PCs(input_df:pd.DataFrame):
    """
    takes a dataframe with (at least) the columns: "gender" and "full_name"

    changes characters with multiple gender options from their specified version to Ambig 
    (to match their general version), and their names to remove any gender specification 
    (ie "Warden (Female) | Player Character" -> "Warden | Player Character") or Doctor Who numbering 
    (ie "The Tenth Doctor" -> "The Doctor")

    Non-Doctor-Who doctors should not be affected (currently accounting for Doctor Strange, will 
    need to add other cases if other Doctors get added to the dataset)

    Currently only player characters from Dragon Age and Mass Effect are accounted for (as none of the 
    others both 1) had multiple gender options & 2) had one specified over the other in the rankings)

    returns a new dataframe with the updated genders & names
    """

    new_df = input_df.copy()

        # setting genders
    new_df["gender"] = new_df["gender"].mask(
        cond=(
            (new_df["full_name"].str.contains("Female", na=False)
            ) | (new_df["full_name"].str.contains("Male", na=False)
            ) | (new_df["full_name"].str.contains(" Doctor", na=False)
            ) & (~new_df["full_name"].str.contains("Strange", na=False)) # not doctor strange
        ),
        other="Ambig"
    )
    
    # making renaming dict
    renaming_dict = {}
    for doctor in [
        "The Eleventh Doctor",
        "The Ninth Doctor",
        "The Tenth Doctor",
        "The Thirteenth Doctor",
        "The Twelfth Doctor",
    ]:
        renaming_dict[doctor] = "The Doctor"
    for pc in [
        "Hawke (Female) | Player Character",
        "Inquisitor (Female) | Player Character",
        "Warden (Female) | Player Character",
        "Shepard (Female) | Player Character",
        "Shepard (Male) | Player Character",
    ]:
        if "Hawke" in pc:
            renaming_dict[pc] = "Hawke | Player Character"
        elif "Inquisitor" in pc:
            renaming_dict[pc] = "Inquisitor | Player Character"
        elif "Warden" in pc:
            renaming_dict[pc] = "Warden | Player Character"
        elif "Shepard" in pc:
            renaming_dict[pc] = "Shepard | Player Character"
    
    # renaming
    new_df["full_name"] = new_df["full_name"].replace(to_replace=renaming_dict)

    return new_df

def find_tied_fandoms(input_df:pd.DataFrame):
    """
    takes a dataframe containing (at least) the columns: "fandom" & "no_of_ships_they_in"

    finds any fandoms where all characters are tied for how many ships they're in

    returns a list listing the fandoms in question, if any
    """
    new_df = input_df.copy()

    # figuring out which fandoms' characters are all tied for ship numbers
    unique_fandoms = get_unique_values_list(new_df, "fandom")

    tied_fandoms = []
    for fandom in unique_fandoms:
        fandom_group = new_df.where(
            cond=new_df["fandom"] == fandom
        ).sort_values(by="no_of_ships_they_in").dropna()

        if fandom_group["no_of_ships_they_in"].max() == fandom_group["no_of_ships_they_in"].min() and \
        fandom_group.shape[0] > 1 and fandom_group["no_of_ships_they_in"].max() > 1:
            tied_fandoms.append(fandom)

    return tied_fandoms # -> only ['Carmilla', 'Amphibia']