genders = [
    "male", 
    "female", 
    "nonbinary", 
    "other"
] 
#I'm questionning the nb labelling of ao3's dataset tho cause of loki's continued 
# mlm labelling despite canon genderfluidity since literally 2013

racial_groups = [
    "white", 
    "asian", 
    "latino", 
    "MENA", 
    "black", 
    "afro-latino",
    "indigenous", 
    "ambiguous", 
    "non-human"
] 
#from terms used in ao3 stats
    #short forms from table
    # Af Lat = Afro-Latino
    # Ambig = Ambiguous Race
    # Indig = Indigenous Peoples
    # MENA = Middle Eastern or North African
    # N.H. = Non-Human Skin Tones
#they have the characters' racial tags separately in the ao3 list, 
# rather than a combo, so I will replicate that in my structure too
# -> accessing both characters' actual attributes to check later, 
# rather than making a combo attribute for their ship, 
# like we are doing w gender

pairings = ["M/M", "F/M", "F/F", "general", "other"]
#from terms used in ao3 stats
# I would like to add a differentiation between 
    # "other" bc of x reader -> m/reader, f/reader, nb/reader, other/reader
    # and "other" bc of nb/other gender pairing -> nb/nb, m/nb, f/nb
#also imo we should have some means of determining apparent gender, 
# like in cases w "genderless" angels played by male actors f.e., 
# cause that's still mlm, not nblnb as far as I'm concerned
    # -> include actor gender where live action maybe?
# also pls note precedent set in femslash ranking including 
# f.e. steven universe gems who are also genderless in canon
    # op has a double standard if they're listing the good omens lads as other 
    # rather than mlm but the gems and trixie/katya as femslash smh

property_types = [
    "movie", 
    "TV series", 
    "online series", 
    "video game", 
    "real life"
]