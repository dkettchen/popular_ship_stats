from src.cleaning_code_refactor.stage_01_parsing_raw_data import parse_txt
from src.cleaning_code_refactor.stage_02_cleaning_names import clean_rankings
from src.cleaning_code_refactor_utils.gathered_data_to_df import gathered_data_to_df
from data.reference_and_test_files.refactor_helper_files.folder_lookup import TOTAL_DATA_FOLDER
from src.cleaning_code_refactor_utils.save_clean_rankings import make_clean_rankings_csvs
from src.cleaning_code_refactor_utils.gather_demo_data import gather_char_demo_data, gather_ship_demo_data

def order_rankings(clean_rankings:dict):
    """
    takes the cleaned name rankings dict

    makes a new version where the ships have been turned from lists to alphabetically ordered
    and " x " (for slash ships) or " & " (for gen ships) joined strings
    and only the following columns are retained in each df:
    'Rank', 'Change', 'Relationship', 'Fandom', 'Total Works', 'New Works'

    other data will be able to joined on from our reference files
    """
    new_dict = {}

    for year in clean_rankings:
        new_dict[year] = {}
        for ranking in clean_rankings[year]:
            current_df = clean_rankings[year][ranking]
            # get relevant columns only
            new_df = current_df.copy().get([
                "Rank", "Change", "Relationship", "Fandom", "Total Works", "New Works", "Type"
            ])

            # wrestling my type lists into submission smh
            # turn lists to strings
            new_df["Type"] = new_df["Type"].apply(str)
            # turn ["Gen"] to just "Gen"
            new_df["Type"] = new_df["Type"].mask(
                new_df["Type"].str.contains("Gen"), other="Gen"
            )
            # make everything else "Slash"
            new_df["Type"] = new_df["Type"].where(
                new_df["Type"] == "Gen", other="Slash"
            )

            # making ship strings
            # sort members
            new_df["Relationship"] = new_df["Relationship"].apply(lambda x: sorted(x))
            # join em based on gen/slash type
            new_df.loc[new_df["Type"] == "Gen", "Relationship"] = new_df["Relationship"].apply(lambda x: " & ".join(x))
            new_df.loc[new_df["Type"] != "Gen", "Relationship"] = new_df["Relationship"].apply(lambda x: " x ".join(x))
            new_df.pop("Type") # now we no longer need "Gen" status as it is represented in the joining symbols
                # and can be retrieved from reference file

            new_df["Fandom_Relationship"] = new_df["Fandom"] + " - " + new_df["Relationship"]

            if ranking == "data":
                new_dict[year]["annual"] = new_df
            else:
                new_dict[year][ranking] = new_df

    return new_dict

if __name__ == "__main__":
    parsed_dict = parse_txt()
    cleaned_ranking_dict = clean_rankings(parsed_dict)
    gathered_demo_data = gather_char_demo_data(cleaned_ranking_dict)
    gathered_ship_data = gather_ship_demo_data(cleaned_ranking_dict, gathered_demo_data)

    for case in ["fandoms", "characters", "ships"]:
        if case == "ships":
            gathered_data = gathered_ship_data
        else:
            gathered_data = gathered_demo_data
        df = gathered_data_to_df(gathered_data, case)
        df.to_csv(f"{TOTAL_DATA_FOLDER}/{case[:-1]}_data.csv")

    final_rankings = order_rankings(cleaned_ranking_dict)
    make_clean_rankings_csvs(final_rankings)

    # TODO did we not track year joined/appeared for ships???

