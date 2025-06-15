from data.reference_and_test_files.refactor_helper_files.location_lookup import (
    COUNTRY_LANGUAGES, CONTINENTS, ENGLISH_SPEAKERS, COUNTRIES
)

def find_continent_and_language(country_of_origin, fandom):
    """
    assigns continent and language based on inputs

    accounts for fandoms whose language doesn't match their country of origin

    returns a list of [continent, language]
    """

    # find continent
    continent = None
    for c in CONTINENTS:
        if country_of_origin in CONTINENTS[c]:
            continent = c
    if not continent:
        print("This country is not in the continent lookup yet:", country_of_origin)

    # find language
    lang = None
    # get base languages based on country of origin
    for c in COUNTRY_LANGUAGES:
        if c == country_of_origin:
            lang = COUNTRY_LANGUAGES[c]
    
    # non-korean kpops still make content in korean, not their nationality's language
    if fandom in COUNTRIES["South Korea"]:
        lang = COUNTRY_LANGUAGES["South Korea"]

    # finding the various english speaking fandoms & ppl
    elif country_of_origin in ENGLISH_SPEAKERS \
    or "UK" in country_of_origin \
    or "USA" in country_of_origin \
    or fandom in [
        # fandoms without UK/USA in the country but that still are international -> english speaking
        "Youtube", # our latin members still make english content
        "Life Is Strange", 
        "All For The Game", 
        "Figure Skating",
        "Formula 1"
    ]:
        lang = "English"

    # checking for non-english speaking countries of origin that may be english speaking fandoms
    elif country_of_origin not in ["South Korea", "China", "Japan"] and fandom not in [
        # known non-english speaking fandoms
        "SKAM",
        "The Witcher | Wiedźmin",
        "KinnPorsche | คินน์พอร์ช เดอะ ซีรีส์",
        "Young Royals",
        "Miraculous: Tales of Ladybug & Cat Noir | Miraculous: Les Aventures de Ladybug et Chat Noir",
    ]:
        print(fandom,lang)
    
    if fandom == "Mirror": # cantopop
        lang += " (Cantonese)"
    if fandom == "Formula 1" and lang == "Dutch": # verstappen is belgian & dutch
        lang = "Dutch / French"

    # did we miss anyone?
    if not lang:
        print("No language was assigned:",country_of_origin)
    
    return [continent, lang]

