non_white_categories = [
    "white_involved_ship", 
    "e_asian_involved_ship", 
    "non_white_ship", 
    "non_white_or_ea_ship"
]

interracial_categories = [
    "interracial_ships", 
    "ambiguous_ships", 
    "non-interracial_ships"
]

suffixes = {
    "femslash" : " (AO3 femslash ranking 2014-2023)",
    "total": " (AO3 2013-2023)",
    "overall": " (AO3 overall ranking 2013-2023)",
    "annual": " (AO3 annual ranking 2016-2023)"
}

racial_group_umbrellas = { # racial group umbrella groups
    "north, west, middle and eastern europe": [
        'White', 
        'White (Multi)',
        'Romani', 
        'Eu Ind (Multi)', 
    ],
    "black (incl afro-latin)": [
        'Black', 
        'Black (Multi)',
        'Af Lat', 
    ],
    "south europe and (rest of) latin": [
        'Latin',
        'Latin (Multi)', 
        'SE Eu', 
        'SE Eu (Multi)', 
    ],
    "middle-east and north-africa": [
        'MENA', 
        'MENA (Multi)', 
    ],
    "east asia": [
        'E Asian', 
        'E Asian (Multi)', 
    ],
    "(rest of) asia": [
        'S Asian', 
        'S Asian (Multi)',
        'SE Asian', 
        'SE Asian (Multi)', 
        'As Ind',
        'As Ind / S Asian (Multi)', 
        'Asian (Multi)', 
        'Central As', 
    ],
    "american & polynesian indigenous": [
        'Am Ind', 
        'Am Ind / E Asian (Multi)', 
        'Māori Ind',
        'Māori Ind (Multi)', 
    ],
    "other": {
        'Ambig': "ambiguous or differing casting", 
        'N.H.': "non-human", 
        'Unknown': "unknown",
    },
}

gender_combo_umbrellas = { # gender combo umbrella groups
    "mlm": ["M / M", "M / M | Other","M | Other / M / M",],
    "wlw": ["F / F","F | Other / F | Other", "F / F | Other",],
    "non-same-sex": ["M / F","F / Other","M / Other","F / M / M"],
    "ambiguous": ["M / Ambig","M | Other / Ambig", "F / Ambig","M | F | Other / M | F | Other"]
}

continents = {
    "Europe":["UK", "Ireland", "France", "Norway", "Sweden", "Poland", "Ireland / UK"],
    "North America":["USA", "Canada", "Canada / USA", "Mexico"],
    "Asia":["China", "Japan", "South Korea", "Thailand", "China / Japan"],
    "Oceania":["Australia", "New Zealand"],
    "North America / Europe":["UK / USA", "France / UK / USA", "France / USA", "Ireland / Mexico / UK / USA"],
    "Asia / Europe":["France / Japan"],
    "North America / Asia":["Japan / USA"],
}