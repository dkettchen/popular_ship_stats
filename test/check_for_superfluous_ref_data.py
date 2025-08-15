from src.vis_code_refactor_utils.read_reference_files import read_reference_file
from src.vis_code_refactor.stage_0_read_in_and_join_data import get_data_from_files

#### VERIFYING THAT WE DON'T HAVE SUPERFLUOUS FANDOMS/SHIPS IN OUR REFERENCE DATA

# retrieve all reference files once at top of running file
print("Reading in reference data...")
reference_data = {}
for case in ["fandoms", "characters", "ships"]:
    reference_data[case] = read_reference_file(case)
print("Reference files have been read.")

# get rankings data, including joined versions 
# (prints updates itself, you can change desired data range in stage_0 file)
joined_ranking_data = get_data_from_files(reference_data)

# collect all items
print("Collecting all items from rankings.")

all_fandoms = []
all_ships = []

for year in joined_ranking_data:
    year_ranking = joined_ranking_data[year]
    for ranking in year_ranking:
        current = year_ranking[ranking]["clean"]

        fandoms = list(current["Fandom"].unique())
        ships = list(current["Relationship"].unique())

        all_fandoms.extend([fandom for fandom in fandoms if fandom not in all_fandoms])
        all_ships.extend([ship for ship in ships if ship not in all_ships])

print("Collected all fandoms and ships from rankings.")

ref_fandoms = list(reference_data["fandoms"].index)
ref_ships = list(reference_data["ships"]["ship_name"])

for fandom in ref_fandoms:
    if fandom not in all_fandoms:
        print("Superfluous fandom:", fandom)

for ship in ref_ships:
    if ship not in all_ships:
        print("Superfluous ship:", ship)