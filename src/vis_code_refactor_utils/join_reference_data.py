import pandas as pd
from src.vis_code_refactor_utils.fix_rpf_fic_fandoms import fix_dual_fandoms

# func take 2 dfs & joins em
def join_ranking_and_ref(ranking_df:pd.DataFrame, reference_dict:dict, case:str):
    """
    takes a given year/rankings' data, a dict with all our reference file data, and a case

    - case="ships" returns a df with joined on data for each ship in the ranking
    - case="characters" returns a df with joined on data for each character in each ship of the ranking
    (incl doubling up characters who were in multiple ships bc they had different ranks per ship)

    both cases join on fandoms data as well

    rpf status is joined via fandoms data, 
    and any fandoms that have both rpf and fic ships are replaced on a
    per-ship/-char basis with the correct rpf status
    """
    # we're adding fandom data to both
    renaming_dict = { # making sure we mark these as fandom data bc may be diff for ships/chars
        'rpf': 'fandom_rpf', 
        'year_joined': 'fandom_year_joined',
        'latest_year': 'fandom_latest_year', 
        'total_years': 'fandom_total_years',
        "country_of_origin": "fandom_country_of_origin",
        "continent": "fandom_continent",
        "language": "fandom_language",
    }
    new_df = ranking_df.join(reference_dict["fandoms"], on="Fandom").rename(columns=renaming_dict)

    if case == "ships":
        get_columns = [
            'gender_combo', 'race_combo', 'orientation_combo', 'gen_ship', 
            'canon', 'canon_alignment', 'incest', 'member_no'
        ]
        name = "Relationship"
    elif case == "characters":
        get_columns = [
            'member_1', 'member_2', 'member_3', 'member_4'
        ]
        name = "Name"
    new_df = new_df.join(reference_dict["ships"].get(get_columns), on="Fandom_Relationship")

    # join on data for each char
    if case == "characters":
        members_list = []
        for i in range(1,5):
            member = f"member_{i}"
            df = new_df.copy()
            
            # get rid of other member columns & rename this one
            for column in df.columns:
                if "member" in column and column != member:
                    df.pop(column)
            df = df.rename(columns={member: "Name"})

            # add column to match to 
            df["Fandom_Name"] = df["Fandom"] + " - " + df["Name"]
            # join
            get_columns = [
                'year_joined', 'latest_year', 'total_years', 
                'gender', 'race', 'orientation', 
                "country_of_origin", "continent", "language",
            ]
            df = df.join(reference_dict["characters"].get(get_columns), on="Fandom_Name")

            char_renaming_dict = { # mark as char specific
                'year_joined': 'char_year_joined',
                'latest_year': 'char_latest_year', 
                'total_years': 'char_total_years',
                "country_of_origin": "char_country_of_origin",
                "continent": "char_continent",
                "language": "char_language",
            }
            df = df.rename(columns=char_renaming_dict)

            # removing any non-existent members (ie if ship only had 2 members & we're on member_3 & _4)
            df = df.where(df["Name"].notna()).dropna(how="all")

            # add to list of dfs
            members_list.append(df)

        # make into one big df
        new_df = pd.concat(members_list)
    
    # fix "both" rpf values
    # making sure we know of all the current fandoms that have both rpf & fic ships/ppl
    both_fandoms = ["Supernatural", "Grandmaster of Demonic Cultivation / The Untamed | 魔道祖师 / 陈情令"]
    other_both_fandoms = new_df[(~new_df["Fandom"].isin(both_fandoms)) & (new_df['fandom_rpf'] == "both")]
    if len(other_both_fandoms) != 0:
        print(other_both_fandoms["Fandom"].unique())

    # replacing on a per-ship/char basis with correct RPF status
    new_df["rpf"] = new_df["fandom_rpf"].mask(
        new_df['fandom_rpf'] == "both", 
        other=new_df[name].apply(fix_dual_fandoms)
    )
    # removing fandom rpf column
    new_df.pop("fandom_rpf")

    return new_df
