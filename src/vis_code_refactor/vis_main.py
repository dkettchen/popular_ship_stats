from src.vis_code_refactor_utils.read_reference_files import read_reference_file
from src.vis_code_refactor.stage_0_read_in_and_join_data import get_data_from_files
from src.vis_code_refactor.stage_1_prep_data import prep_data
import pandas as pd

# retrieve all reference files once at top of running file
print("Reading in reference data...")
reference_data = {}
for case in ["fandoms", "characters", "ships"]:
    reference_data[case] = read_reference_file(case)
print("Reference files have been read.")

# get rankings data, including joined versions 
# (prints updates itself, you can change desired data range in stage_0 file)
joined_ranking_data = get_data_from_files(reference_data)

# add characters per rankings
for ranking in ["overall", "annual", "femslash"]:
    # get all ships from ship ref for ranking
    current = joined_ranking_data[ranking]
    ranking_ships = reference_data["ships"].where(
        reference_data["ships"]["ship_name"].isin(list(current["ship_name"]))
    ).dropna(how="all")

    # compile members
    members = []
    for member in ["member_1", "member_2", "member_3", "member_4"]:
        member_list = list(ranking_ships[member].dropna())
        if len(member_list) > 0:
            members.extend(member_list)
    members = sorted(list(set(members)))

    # get all chars from char ref
    ranking_chars = reference_data["characters"].where(
        reference_data["characters"]["name"].isin(members)
    ).dropna(how="all")

    joined_ranking_data[f"{ranking}_characters"] = ranking_chars

# TODO items for presentation
(
# new total numbers (total chars, total fandoms represented) ✅
# biggest fandoms (total) accounting for >1% of total ships ✅ - can stay pie chart
    # extract new numbers to list of how many ships for biggest few fandoms ✅
# make a version of it for each ranking! ✅ - also pie chart
    # check for weighted by ranks??
# check HP ships! cause I know we got some new ones in 2024 ✅
    # maybe make a chart for the which ships are which category (ie marauders, fanta beasts, etc) ✅ (have prepped category info)
# check for top ships! (longest running/longest streak for annual) ✅
    # how tf did we do that the first time?
    # check if same 6 pairings are still in there every year of overall? ✅ (yes)
# do we want to rerun the weighted by rank most popular ships? 🟨 (optional for now)
    # (I think we had these per ranking)
    # and then also by gender combo version 🟨
# also rerun hottest chars (in 3+ ships, per fandom) ✅
    # -> doesn't need a table chart, just a ranking 
        # -> visualise/save however you prefer if it's a bother, 
        # as we'll put their pics in the presentation/video
    # marvel ones are the same as before, so I can simply keep the same chart for the presentation! re bucky
# check rpf numbers, we don't need charts, just figures ✅
    # total numbers ✅ 
    # by gender in co-ed rankings ✅
# gender: ✅
    # (we prepped the numbers in one big df & a dict for minority genders) ✅ 
    # stacked bars per ranking? (stacked bar out of 100% per year)
    # figures!
    # rerun total minority chars although I don't think we got new ones? maybe player chars?? idr ✅
    # figures & maybe a stacked bars chart for gender combos
# race: ❗
    # (general numbers & minorities dict have been prepped same as gender) ✅ 
    # simplify any groups that were below a certain percent bc they won't show up properly anyway ✅
        # ranking specific tho ✅
    # stacked bars per ranking out of 100% per year
    # get figures too
    # 4 categories ✅ can remain bar chart for total
        # get new lowest number ✅ (17 total)
    # make stacked bars for years? (I just think stacked bars will look nice! & bc we have % option anyway)
        # figure out how to handle the top 50 femslash year? make it so the bar is half of other ones still!
        # I also think stacked bars for categories will nicely show different groups pushing each other by 
        # expanding etc
    # rerun the avg rank by categories one ❗
    # get a list of all the non-white/non-EA pairings for each ranking ✅
    # check for black & afro-latin superheroes for my sam wilson point ✅
        # Sam is the only one to make co-ed rankings, all the others are femslash exclusives ✅
    # check for british south asian ppl ✅ (same two as before)
# geo data ✅
    # rerun totals for language & countries (make sure it's relevant one for where diff between char & fandom) ✅ 
    # we need a graph for femslash for meme to work ✅ 
    # -> make charts for each ranking? maybe stacked bars again?
    # get figures
    # check for oceania fandoms, although I don't think we got any new ones ✅
    # check for non-UK euro fandoms, although also doubt ✅
    # % of white & ea rep in east & west fandoms ✅
    # check for gender combos in east asian fandoms for not enough straight pairings point ✅
    # check for rpf in korean fandoms for not enough non-rpf point ✅
        # (alien stage is new non-rpf!, only one other than omniscient reader, both are only mlm)
# sexuality & canon ✅
    # make some charts but tbd what we want to include & how
    # canon by gender combo ✅
    # canon alignment by gender combo ✅
    # canon-established sexuality by gender? 🟨 (optional for now)
)
# TODO (after everything) print updates about data & chart making process below

print("Retrieving relevant data...")

## series to collect all solo-number figures
figures = pd.Series()

print("Getting total numbers...")
# start with total numbers across entire data set
figures["total_characters"] = len(reference_data["characters"]) # 914
figures["total_ships"] = len(reference_data["ships"]) # 615
figures["total_fandoms"] = len(reference_data["fandoms"]) # 204

# numbers of ships in each ranking (annual has the most diff ships despite being shortest period tracked)
figures["total_ships_in_overall"] = len(joined_ranking_data["overall"]) # 206
figures["total_ships_in_femslash"] = len(joined_ranking_data["femslash"]) # 210
figures["total_ships_in_annual"] = len(joined_ranking_data["annual"]) # 368

print("Getting biggest fandoms...")
## biggest fandoms (>1% of ships)
fandom_ship_count = pd.DataFrame({
    "most_ships_count":prep_data(reference_data["ships"], "fandom_count"),
    "most_ships_percent":prep_data(reference_data["ships"], "fandom_percent"),
})
fandom_ship_count = fandom_ship_count.where(
    fandom_ship_count["most_ships_percent"] >= 1
).dropna(how="all").sort_values("most_ships_count", ascending=False)

# top 5 biggest fandoms + ship numbers
    # Marvel                    34
    # Youtube                   27  # TODO rename this fandom? ie "online creators" or "youtube & streaming" idk
    # Harry Potter Universe     22
    # DC                        21
    # Genshin Impact            18

# of individual rankings
overall_fandom_ship_count = pd.DataFrame({
    "most_ships_count":prep_data(joined_ranking_data["overall"], "fandom_count"),
    "most_ships_percent":prep_data(joined_ranking_data["overall"], "fandom_percent"),
})
overall_fandom_ship_count = overall_fandom_ship_count.where(
    overall_fandom_ship_count["most_ships_percent"] >= 1
).dropna(how="all").sort_values("most_ships_count", ascending=False)

femslash_fandom_ship_count = pd.DataFrame({
    "most_ships_count":prep_data(joined_ranking_data["femslash"], "fandom_count"),
    "most_ships_percent":prep_data(joined_ranking_data["femslash"], "fandom_percent"),
})
femslash_fandom_ship_count = femslash_fandom_ship_count.where(
    femslash_fandom_ship_count["most_ships_percent"] >= 1
).dropna(how="all").sort_values("most_ships_count", ascending=False)

annual_fandom_ship_count = pd.DataFrame({
    "most_ships_count":prep_data(joined_ranking_data["annual"], "fandom_count"),
    "most_ships_percent":prep_data(joined_ranking_data["annual"], "fandom_percent"),
})
annual_fandom_ship_count = annual_fandom_ship_count.where(
    annual_fandom_ship_count["most_ships_percent"] >= 1
).dropna(how="all").sort_values("most_ships_count", ascending=False)

print("Categorising HP ships...")
## assign categories to HP ships (ie which generation/series the characters are from) -> series
    # -> to make a chart about which make up the most ships to demonstrate it's not fantastic beasts!
hp_ships_srs = reference_data["ships"].where(reference_data["ships"]["fandom"] == "Harry Potter Universe").dropna(how="all")["ship_name"]
hp_ship_categories = { # currently all ships until 2024 categorised
    "Harry Potter gen": [
        "Draco Malfoy x Harry Potter",
        "Draco Malfoy x Hermione Granger",
        "Fleur Isabelle Weasley, née Delacour x Hermione Granger",
        "Ginny Weasley x Harry Potter",
        "Ginny Weasley x Hermione Granger",
        "Ginny Weasley x Luna Lovegood",
        "Hermione Granger x Pansy Parkinson",
        "Hermione Granger x Ron Weasley",
    ],
    "Marauders gen": [
        "Barty Crouch Jr. x Evan Rosier",
        "Dorcas Meadowes x Marlene McKinnon",
        "James Potter x Lily Potter, née Evans",
        "James Potter x Regulus Black",
        "Lily Potter, née Evans x Mary Macdonald",
        "Lily Potter, née Evans x Pandora Lovegood",
        "Regulus Black & Sirius Black",
        "Remus Lupin x Severus Snape",
        "Remus Lupin x Sirius Black",
    ],
    "Cross-gen": [
        "Bellatrix Lestrange, née Black x Hermione Granger",
        "Harry Potter x Severus Snape",
        "Harry Potter x Tom Riddle | Voldemort",
        "Hermione Granger x Severus Snape",
    ],
    "Fantastic Beasts": [
        "Credence Barebone x Percival Graves",
    ],
}
def assign_hp_category(x):
    for key in hp_ship_categories:
        if x in hp_ship_categories[key]:
            return key
hp_ships = pd.DataFrame()
hp_ships["ship"] = hp_ships_srs
hp_ships["category"] = hp_ships_srs.apply(lambda x: assign_hp_category(x))
hp_ships = hp_ships.set_index("ship")

print("Calculating most-shipped characters...")
## hottest characters per fandom
members = []
for member in ["member_1", "member_2", "member_3", "member_4"]:
    member_column = reference_data["ships"].where(
        reference_data["ships"]["gen_ship"] == False # we don't want gen ships for this
    ).get(["fandom", member]).rename(columns={member:"name"}).dropna(how="any") # get fandom & name
    members.append(member_column)
chars_by_ships = pd.concat(members) # get all members
chars_by_ships["count"] = "1" # add a column so it has something to count
hottest_chars = chars_by_ships.groupby(["name", "fandom"]).count()
hottest_chars = hottest_chars.where(hottest_chars["count"] >= 3).dropna(how="all") # must be in 3+ ships
# sort by fandom & rank therein, save new order via index
hottest_chars = hottest_chars.reset_index().sort_values(["fandom", "count"], ascending=False).reset_index()
hottest_chars.pop("index")
# TODO rank numbers per fandom incl who tied? how?
# marvel ones for presentation re bucky x sam -> same as before, so I can keep the graphic as is
hottest_marvel_chars = hottest_chars.where(hottest_chars["fandom"] == "Marvel").dropna(how="all")

print("Finding longest-running ships...")
## longest running ships
longest_running = {}
for ranking in ["overall", "annual", "femslash"]:
    current_ranking = {}

    if ranking == "femslash":
        top_ranks = 5
    else:
        top_ranks = 10

    for year in joined_ranking_data:
        if type(year) != int or ranking not in joined_ranking_data[year]: 
            # ignore the ranking-total ship lists
            # & skip rankings not tracked that year
            continue
        curr = joined_ranking_data[year][ranking]["clean"]
        top = curr.where(curr["Rank"] <= top_ranks).dropna(how="all")
        for ship in list(top["Fandom_Relationship"]):
            if ship not in current_ranking:
                current_ranking[ship] = 0
            current_ranking[ship] += 1

    longest_running[ranking] = pd.Series(current_ranking).sort_values(ascending=False)
    longest_running[ranking] = longest_running[ranking].where(longest_running[ranking] > 1).dropna()


# (...) (most popular weighted by rank per ranking & gender combo-separated version there-of)

print("Getting RPF numbers...")
## RPF
rpf_ships = {
    "total":prep_data(reference_data["ships"], "rpf_subset"),
    "overall":prep_data(joined_ranking_data["overall"], "rpf_subset"),
    "femslash":prep_data(joined_ranking_data["femslash"], "rpf_subset"),
    "annual":prep_data(joined_ranking_data["annual"], "rpf_subset"),
}
rpf_ships_by_gender = pd.DataFrame({
    "overall_count":prep_data(rpf_ships["overall"], "gender_combo_count"),
    "overall_percent":prep_data(rpf_ships["overall"], "gender_combo_percent"),
    "annual_count":prep_data(rpf_ships["annual"], "gender_combo_count"),
    "annual_percent":prep_data(rpf_ships["annual"], "gender_combo_percent"),
})
figures["total_RPF_ships"] = len(rpf_ships["total"]) # 80
figures["total_RPF_ships_in_overall"] = len(rpf_ships["overall"]) # 35
figures["total_RPF_ships_in_femslash"] = len(rpf_ships["femslash"]) # 9
figures["total_RPF_ships_in_annual"] = len(rpf_ships["annual"]) # 61

print("Getting gender and race data...")
## gender & race

# total
char_genders = {
    "total": pd.DataFrame({
        "total_count":prep_data(reference_data["characters"], "gender_count"),
        "total_percent":prep_data(reference_data["characters"], "gender_percent"),
    }),
}
char_races = {
    "total": pd.DataFrame({
        "total_count":prep_data(reference_data["characters"], "race_count"),
        "total_percent":prep_data(reference_data["characters"], "race_percent"),
    })
}

# ranking specific totals
for ranking in ["overall", "annual", "femslash"]:
    char_genders[ranking]= pd.DataFrame({
        f"total_count":prep_data(joined_ranking_data[f"{ranking}_characters"], "gender_count"),
        f"total_percent":prep_data(joined_ranking_data[f"{ranking}_characters"], "gender_percent"),
    })
    char_races[ranking]= pd.DataFrame({
        f"total_count":prep_data(joined_ranking_data[f"{ranking}_characters"], "race_count"),
        f"total_percent":prep_data(joined_ranking_data[f"{ranking}_characters"], "race_percent"),
    })

# by year (add more columns to same dfs)
# iterate over all years
for year in joined_ranking_data:
    if type(year) != int: # ignore the ranking-total ship lists
        continue
    # iterate over all rankings
    for ranking in ["overall", "annual", "femslash"]:
        if ranking not in joined_ranking_data[year]: 
            # skip rankings not tracked that year
            continue

        # we want the characters subset 
            # -> easier to get percentile of bc more similar numbers
            # -> more accurate to rep that made the ranking that year, even if some are repeats of indiv. chars
        current = joined_ranking_data[year][ranking]["characters"] # clean/*characters*/unique_characters/ships

        # we want the percentile number for each year & each ranking to use for our diagrams later
        char_genders[ranking][f"{year}_percent"] = prep_data(current, "gender_percent")
        char_races[ranking][f"{year}_percent"] = prep_data(current, "race_percent")

# combine smallest racial groups into one value based on (ranking) total numbers
for key in char_races:
    big_race_groups = char_races[key].where(
        char_races[key]["total_percent"] >= 0.5
    ).dropna(how="all").sort_values("total_percent", ascending=False)

    small_race_groups = char_races[key].where(
        char_races[key]["total_percent"] < 0.5
    ).dropna(how="all").sum()

    small_race_groups = pd.DataFrame(
        small_race_groups, 
        columns=["< 0.5%"], 
        index=small_race_groups.index
    ).transpose()

    char_races[key] = pd.concat([big_race_groups, small_race_groups])

# TODO make a group_by_ for minority races to separate into categories
    # latin (minus af lat), black, other asian, indig, other european (was there anything else??)

# minority labels (as dicts)
minority_gender_dict = {}
minority_race_dict = {}
for label in ["gender", "race"]:
    # get subset (save this somewhere if you wanna re-use it later for querying other things)
    subset = prep_data(reference_data["characters"], f"minority_{label}s_subset")
    # get just the name & fandom data
    minority_folks = subset.get(["name", "fandom", label])

    # make into dict 
        # per each label: list of names (to look up pics to show!) & total number
    temp_dict = {}
    for tag in minority_folks[label].unique():
        # make a sub-dict for this tag
        temp_dict[tag] = {}

        # find only this tag's chars
        category = minority_folks.where(minority_folks[label] == tag).dropna(how="all")

        # mark names w their fandoms
        category["blank_from_blank"] = category["name"] + " (" + category["fandom"] + ")"

        # add names list & total per each category
        temp_dict[tag]["names_list"] = list(category["blank_from_blank"])
        temp_dict[tag]["number"] = len(category)
    
    if label == "gender":
        minority_gender_dict = temp_dict
    elif label == "race":
        minority_race_dict = temp_dict

print("Grouping ships by whether or not they contain white and/or east asian people...")
# 4 categories
four_categories = { # full subsets
    ranking: prep_data(
        joined_ranking_data[ranking], "group_by_race_combo_category"
    ) for ranking in ["overall", "femslash", "annual"]
}
four_categories["total"] = prep_data(reference_data["ships"], "group_by_race_combo_category")

# ship counts per each ranking & total 
    # (no percentages as we're excluding ships without (known) real racial groups -> not full set of ships)
four_categ_counts = pd.DataFrame({
    ranking: four_categories[ranking].get(
        ["white-involved", "EA-involved", "non-white", "non-white/non-EA"]
    ).count() for ranking in four_categories
})

# TODO average rank per year per category

print("Getting country and language data...")
## geo data
geo_count = pd.DataFrame({
    "total_country_count":prep_data(reference_data["ships"], "country_of_origin_count"),
    "total_country_percent":prep_data(reference_data["ships"], "country_of_origin_percent"),
    # TODO add femslash/ranking-specific data
    # TODO should rankings be total or by year?
})
lang_count = pd.DataFrame({
    "total_language_count":prep_data(reference_data["ships"], "language_count"),
    "total_language_percent":prep_data(reference_data["ships"], "language_percent"),
})
# add ranking totals & yearly data
for ranking in ["overall", "annual", "femslash"]:
    geo_count[f"total_{ranking}_country_percent"] = prep_data(joined_ranking_data[ranking], "country_of_origin_percent")
    lang_count[f"total_{ranking}_language_percent"] = prep_data(joined_ranking_data[ranking], "language_percent")

    for year in joined_ranking_data:
        if type(year) != int or ranking not in joined_ranking_data[year]: 
            # ignore the ranking-total ship lists
            # & skip rankings not tracked that year
            continue
        geo_count[f"{year}_{ranking}_country_percent"] = prep_data(joined_ranking_data[year][ranking]["ships"], "country_of_origin_percent")
        lang_count[f"{year}_{ranking}_language_percent"] = prep_data(joined_ranking_data[year][ranking]["ships"], "language_percent")

print("Calculating eastern and western rep...")
## east vs west!
eastern_characters = prep_data(reference_data["characters"], "eastern_countries_subset")
western_characters = prep_data(reference_data["characters"], "western_countries_subset")

# how many white & east asian folks in east vs west (only biggest 3 countries each)
race_groups_by_hemisphere = pd.DataFrame({
    "eastern_percent": prep_data(eastern_characters, "race_percent"),
    "western_percent": prep_data(western_characters, "race_percent"),
}).loc[["White", "E Asian"]]
race_groups_by_hemisphere = race_groups_by_hemisphere.transpose()
# adding remaining percent back in
race_groups_by_hemisphere["Others"] = 100 - (race_groups_by_hemisphere["White"] + race_groups_by_hemisphere["E Asian"])

# gender combos for east vs west
    # japan makes up for most wlw & het ships in the east top 3
    # china & korea have only one (1) het ship and it's one of the 2024 genshin ones!
    # vs total ca 3/4 mlm & china/korea only >80% mlm!
    # meanwhile west actually has *more* wlw ships than mlm ones total! 
        # bc there is just so much north american femslash
    # both at ca 40% of all western ships with hets only ca 15%
eastern_ships = prep_data(reference_data["ships"], "eastern_countries_subset")
western_ships = prep_data(reference_data["ships"], "western_countries_subset")
china_and_korea_only_ships = eastern_ships.where(
        eastern_ships["country_of_origin"] != "Japan"
    ).dropna(how="all")
gender_combos_by_hemisphere = pd.DataFrame({
    "eastern_percent": prep_data(eastern_ships, "gender_combo_percent"),
    "china_and_korea_only_percent": prep_data(china_and_korea_only_ships, "gender_combo_percent"),
    "western_percent": prep_data(western_ships, "gender_combo_percent"),
    "eastern_count": prep_data(eastern_ships, "gender_combo_count"),
    "china_and_korea_only_count": prep_data(china_and_korea_only_ships, "gender_combo_count"),
    "western_count": prep_data(western_ships, "gender_combo_count"),
})
gender_combos_by_hemisphere = gender_combos_by_hemisphere.transpose().fillna(0)
# TODO if we get other combos that fit in these categories in future years, 
# we need to add those/implement a means to find all combos we have automatically in any case here
gender_combos_by_hemisphere["mlm"] = gender_combos_by_hemisphere["M / M"] \
                                    + gender_combos_by_hemisphere["M / M | Other"] \
                                    + gender_combos_by_hemisphere["M | Other / M"] \
                                    + gender_combos_by_hemisphere["M | F | Other / M | F | Other"]
gender_combos_by_hemisphere["wlw"] = gender_combos_by_hemisphere["F / F"] \
                                    + gender_combos_by_hemisphere["F / F | Other"] \
                                    + gender_combos_by_hemisphere["F | Other / F | Other"]
gender_combos_by_hemisphere["het"] = gender_combos_by_hemisphere["F / M"] \
                                    + gender_combos_by_hemisphere["M / F"]
gender_combos_by_hemisphere = gender_combos_by_hemisphere.get(["mlm", "wlw", "het"])

print("Getting canon data by gender combo...")
## canon & sexuality data
gender_combo_subsets = {
    "mlm":prep_data(reference_data["ships"], "mlm_subset"),
    "wlw":prep_data(reference_data["ships"], "wlw_subset"),
    "het":prep_data(reference_data["ships"], "het_subset"),
    # "other":prep_data(reference_data["ships"], "other_gender_combo_subset"), # this is mostly ambig ships huh
}
canon_by_gender_combo = pd.DataFrame({
    "mlm_count":prep_data(gender_combo_subsets["mlm"], "canon_count"),
    "mlm_percent":prep_data(gender_combo_subsets["mlm"], "canon_percent"),
    "wlw_count":prep_data(gender_combo_subsets["wlw"], "canon_count"),
    "wlw_percent":prep_data(gender_combo_subsets["wlw"], "canon_percent"),
    "het_count":prep_data(gender_combo_subsets["het"], "canon_count"),
    "het_percent":prep_data(gender_combo_subsets["het"], "canon_percent"),
})
canon_alignment_by_gender_combo = pd.DataFrame({
    "mlm_count":prep_data(gender_combo_subsets["mlm"], "canon_alignment_count"),
    "mlm_percent":prep_data(gender_combo_subsets["mlm"], "canon_alignment_percent"),
    "wlw_count":prep_data(gender_combo_subsets["wlw"], "canon_alignment_count"),
    "wlw_percent":prep_data(gender_combo_subsets["wlw"], "canon_alignment_percent"),
    "het_count":prep_data(gender_combo_subsets["het"], "canon_alignment_count"),
    "het_percent":prep_data(gender_combo_subsets["het"], "canon_alignment_percent"),
})

# TODO this currently doesn't actually do it correctly, fix, but we don't necessarily need it for presentation
# orientation_by_gender = prep_data(reference_data["characters"], "orientation_by_gender")
# print(orientation_by_gender)

#############################

# what do we want to check for?
### total data

## fandoms


# top 15 fandoms weighed for rank

# fandoms x ship type
    # num of fandoms with no/over half/only this ship type
    # avg num of ship type in fandoms
    # top 3 fandoms with most ships of this ship type

# top fandoms for racial diversity

# hottest chars per fandom (in 3+ ships)

# top 6 countries' fandoms 
    # (use single item country of origins, then char country of origins to account for idols)

## various

# rpf vs fictional ships



# TODO:

    # total gender combo of ships
    # minority gender combos
    # total race combo categories (white-inv, EA-inv, non-white, non-white/-EA)
        # also total num of last category!
    # total interracial vs non-interracial vs ambig ships
    # maybe total interracial vs etc ships for only our two biggest groups? (white & EA)
        # -> to demonstrate that most EA ships are non-interracial

    # total canon vs non canon
        # & by gender combo
    # orientation label by male/female chars
    # orientation aligned vs conflicted vs ambig w canon
        # & by gender combo
    # incest can just be numbers

    # total country distribution of fandoms
        # maybe also weighed for number of ships?
        # also by chars bc rpf folks are from diff countries?
    # total language distribution of fandoms

    # other stats by top 6 countries
        # gender distr (chars)
        # ship gender combo (ships)
        # race distr (chars)
        # fandoms from that country 
            # (fandom country of origin, where single country (ie idols), 
            # char country of origin for other rpf) -> count by chars
        # interracial ships
        # multiracial chars
        # canon by country
        # orientation by country
        # canon conflict by country
        # -> make a chart for each thingy that has data for all the 6 countries as stacked bar charts?
    # east vs west's white & EA rep % (grouped bar chart)


# TODO
# - start on chart code
    # - I wanna be able to run charts for a given time range
    # - I want any multiplot charts to adapt to the range given
    # - and/or turn multiplot charts to linear ones instead of pies (ie linegraph or stacked bar) 
    # to make more efficient to display
    # - we should have functions to prep the data by case (to reuse for both yearly ranking & total data)
    # - and then a func to compile all years into one df to use
    # - and then funcs for the actual charts

    # - I wanna add charts abt years appeared stuff
        # - number of ships vs years appeared of a fandom -> make a scatter plot 
            # & see if there's two groups: where longest running fandoms either have only 
            # very few ships that have carried their ass, or where they have the most ships -> big fandoms
        # - possibly check ships too in a similar manner? 
            # ie which ships out of big fandoms have carried them for so long
            # vs which were just kinda added by sheer size
        # - were those ships mlm/wlw/het -> cause I think femslash has more different fandoms that have lasted,
            # while mlm has a few fandoms that have not budged with the rest being more fluctuating
        # - also how many fandoms per how many years they lasted
            # also possible how many per "lasted all years since appearance"? 
            # or like how long they last on average? (ie ship joined x year, how long on average did it last after?)
            # - how long do ships usually last per type/ranking/ -> how much fluctuation is there
                # bc say the overall/femslash rankings seem decently stable
                # and femslash in general has certain ships that just stay in there for ages, 
                # even if they're not high up


#TODO (I returned after a while so I'm reorienting myself aah)
# data
# - we made it so all rankings are only up to rank 100 ✅
# - we already removed the resulting superfluous reference data ✅

# - I want to be able to access data
    # - total all years -> can use ref data bc it's up to date! ✅
    # - total all years, by ranking -> prepped in joined data as "overall"/"annual"/"femslash" ✅
    # - by each year (all rankings) -> prepped in joined data as year/"total" ✅
    # - by each year AND ranking -> various versions are prepped in joined data as year/ranking/ ✅

# - move old code to its own folder(s)??

# - char data: [
    # (index = fandom_name), 
    # name, 
    # fandom,
    # year_joined, 
    # latest_year, 
    # total_years,
        # Q: do we want to have a list of all the years somewhere? does it matter?
    # gender, 
    # race, 
        # Q: do we want to separate the ambigs into conflicted casting, can't determine, and variable? 
        # and then also abt whether they are def not/never white? idk!!
    # orientation,
    # country_of_origin, 
    # continent, 
    # language
        # N: country, continent, language can be diff between char & fandom they're in
        # Q: ❗ how did we categorise certain chars/fandoms again? Idr
        # Q: ❗ do we need to update methodology about it?
# ]

# - fandom data: [
    # fandom,
        # Q: do we want to add the korean version of kpops?
    # rpf,
    # year_joined,
    # latest_year,
        # Q: could we check for which fandoms were added in/didn't appear after a given year?
    # total_years,
    # country_of_origin,
    # continent,
    # language
# ]

# - ship data: [
    # index (fandom_ship_name),
    # ship_name,
        # N: gen ships are listed separately from their slash ships, 
        # but only when they're in the ranking, not by default
    # fandom,
    # gender_combo,
    # race_combo, 
        # N: if same race -> no / between, just one label
    # orientation_combo,
    # gen_ship,
        # N: the below three are labelled "gen ship" for any gen ships
    # canon,
    # canon_alignment,
    # incest,
    # member_no,
    # member_1,member_2,member_3,member_4
# ]


