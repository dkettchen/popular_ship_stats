# TODO 
# a func that takes a df of a total data set or a yearly ranking data set,
# and a case
# that then prepares the data requested by the case from the given data set
# ex. "race percent" might give a series of all our race labels along with the % of characters 
# in the given data set that had that label

from src.vis_code_refactor_utils.read_reference_files import read_reference_file
from src.vis_code_refactor_utils.read_ranking_files import read_rankings

# retrieve all reference files once at top of running file
print("Reading in reference data...")
reference_data = {}
for case in ["fandoms", "characters", "ships"]:
    reference_data[case] = read_reference_file(case)
print("Reference files have been read.")

start_year = 2013
end_year = 2024
which_ranking = "all"
website = "AO3"
print(f"Reading in {which_ranking} {website} ranking data from {start_year} to {end_year}...")
# retrieve ranking data
all_rankings = read_rankings(end_year, start_year, which_ranking, website)
print("Ranking files have been read.")
