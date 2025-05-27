from re import split
from src.cleaning_code_refactor_utils.categorise_char_names import categorise_names
from src.cleaning_code_refactor_utils.make_full_name import make_full_name
from data.reference_and_test_files.refactor_helper_files.old_character_names_lookup import OLD_CHARACTERS_LOOKUP
from src.cleaning_code_refactor_utils.complete_char_names import unify_chars, complete_chars

def remove_brackets(old_name:str):
    """
    if there are brackets in the given name,
    it removes everything from the whitespace before the brackets 
    and returns the remaining name

    ex "Arthur Pendragon (Merlin)" -> "Arthur Pendragon"
    """

    if "(" in old_name:
        new_name = split(" \(", old_name)[0]
    else: 
        new_name = old_name

    return new_name
def separate_into_parts(old_name:str):
    """
    separates the given name into the contained name parts
    """

    if " | " in old_name:
        split_name = split(r" \| ", old_name)
    else: 
        split_name = [old_name]

    new_name = []

    specific_cases = {
        "Rap Monster": ["Rap Monster/RM"], 
        "RM": ["Rap Monster/RM"],
        'Rumpelstiltskin': ["Rumpelstiltskin"],
        'Rumplestiltskin': ["Rumpelstiltskin"],
        "Geralt z Rivii": ["Geralt","z Rivii"],
        "Helena 'H. G.' Wells": ["Helena","'H. G.'","Wells"],
        "You": ["Reader"],
    }
    multi_word_names = [
        'Chat Noir',
        #'Darth Vader',
        #'Captain Hook',
        'Evil Queen',
        'The Golden Guard',
        'The Archivist',
        'Six-eared Macaque',
        #'Madam Satan',
        'My Unit', # I think this is not a name, but tbh look up, other name was 'Byleth'
        'Red Riding Hood',
        'Cherry Blossom',
        'Soldier: 76',
        'Monkey King',
        'The Darkling',
        'All Might',
        'Present Mic',
        #'Kylo Ren',
        "Ninth Doctor",
        "Persona 5 Protagonist",
        #"Princess Bubblegum",
        "Pink Diamond",
        "Rose Quartz",
        #"Mr. Gold",
        "Tenth Doctor",
        "The Doctor",
        "Thirteenth Doctor",
        "Twelfth Doctor",
        "Eleventh Doctor",
        "Upgraded Connor",
        "Venom Symbiote",
        "Lapis Lazuli", 
        "Iron Bull",
        "Wilbur Soot"
    ]

    for part in split_name:
        new_part = None

        # "<blank> of <blank>" et al
        for conn in [
            " of ",
            " di ",
            " al ",
            " Van ",
            " von ",
            " the ",
        ]:
            if conn in part:
                temp_split = split(conn, part)
                new_part = [temp_split[0], conn[1:] + temp_split[1]]
                break

        if not new_part:
            if part in specific_cases: # special cases dict
                new_part = specific_cases[part]
            elif ("Female " in part or "Male " in part) \
            or part not in multi_word_names: # just split at white spaces
                new_part = split(r"\s", part)
            else: # do not split
                new_part = [part]

        # add separated parts to new name
        new_name += new_part

    return new_name

def clean_names(old_name:str, fandom:str):
    """
    takes old name & clean fandom

    returns a dict with at least a full_name key

    if it's a new character that isn't in the lookup yet, 
    it also prints the full name (to add to the lookup) 
    and returns the parsed name parts in the dict
    """
    # check if character is already in our known characters lookup
    if f"{fandom} - {old_name}" in OLD_CHARACTERS_LOOKUP:
        new_name = {"full_name": OLD_CHARACTERS_LOOKUP[f"{fandom} - {old_name}"]}

    # otherwise clean & print
    else:
        new_name = remove_brackets(old_name)
        new_name = separate_into_parts(new_name)
        new_name = categorise_names(new_name, fandom)
        new_name = unify_chars(new_name, fandom)
        new_name = complete_chars(new_name, fandom)
        
        print("This character is not in the lookup yet:", {f"{fandom} - {old_name}" : new_name["full_name"]})

    return new_name
