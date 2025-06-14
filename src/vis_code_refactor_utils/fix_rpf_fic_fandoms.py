def fix_dual_fandoms(name:str):
    """
    name must be the name of a ship or character/person

    if the ship/person is RPF, returns True, otherwise returns False
    """
    # currently only supernatural & the untamed have both rpf & non-rpf fandoms
    if name in [
        "Wang Yi Bo x Xiao Zhan | Sean Xiao", 
        "Wang Yi Bo", "Xiao Zhan | Sean Xiao",
        "Jared Padalecki x Jensen Ackles",
        "Jared Padalecki", "Jensen Ackles",
    ]:
        return True
    return False