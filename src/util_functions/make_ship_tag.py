def make_ship_tag(member_list: str, fic_type):
    """
    takes a list of ship member names, and the type of the fic ("gen" or "slash")

    returns a tag of the member names in alphabetical order, 
    separated by a " & " if the fic type is "gen",
    or by an " x " if it is anything else
    """
    if len(member_list) == 1:
        return member_list[0]

    if fic_type.lower() == "gen":
        separator = " & "
    else: 
        separator = " x "

    sorted_ship = sorted(member_list)
    length = len(sorted_ship)
    ship = sorted_ship[0] + separator + sorted_ship[1]
    if length > 2:
        ship += separator + sorted_ship[2]
        if length == 4:
            ship += separator + sorted_ship[3]

    return ship