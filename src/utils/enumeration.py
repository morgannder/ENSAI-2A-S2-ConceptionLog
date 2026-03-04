from typing import Literal


Ranks_enum = Literal[
    "Bronze",
    "Silver",
    "Gold",
    "Platinum",
    "Diamond",
    "Champion",
    "Grand Champion",
    "Supersonic Legend",
]

Platform_enum = Literal[
    "epic",
    "steam",
    "ps4",
    "xbox",
    "psynet",
    "unknown",
]

GameMode_enum = Literal[
    # Non classé
    "unranked-duels",
    "unranked-doubles",
    "unranked-standard",
    "unranked-chaos",
    # Classé
    "ranked-duels",
    "ranked-doubles",
    "ranked-solo-standard",
    "ranked-standard",
    "ranked-hoops",
    "ranked-rumble",
    "ranked-dropshot",
    "ranked-snowday",
    # Modes spéciaux
    "hoops",
    "rumble",
    "dropshot",
    "snowday",
    "rocketlabs",
    "dropshot-rumble",
    "heatseeker",
    # Autres
    "private",
    "season",
    "offline",
    "tournament",
]
