from src.vis_code_refactor_utils.read_reference_files import read_reference_file
from src.vis_code_refactor.stage_0_read_in_and_join_data import get_data_from_files
from src.vis_code_refactor.stage_1_prep_data import prep_data

# retrieve all reference files once at top of running file
print("Reading in reference data...")
reference_data = {}
for case in ["fandoms", "characters", "ships"]:
    reference_data[case] = read_reference_file(case)
print("Reference files have been read.")

# get rankings data, including joined versions 
# (prints updates itself, you can change desired data range in stage_0 file)
joined_data = get_data_from_files(reference_data)

total_gender_count = prep_data(reference_data["characters"], "gender_count")
total_race_count = prep_data(reference_data["characters"], "race_count")
total_orient_count = prep_data(reference_data["characters"], "orientation_count")
# print(total_orient_count)
print(reference_data["ships"].columns)

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
        