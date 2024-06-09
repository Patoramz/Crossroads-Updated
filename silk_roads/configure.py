# configure.py

# Role adjustments
personality_stat_changes = {
    "Villain": {"moral_compass": -20},
    "Hero": {"moral_compass": 15},
    "Mercenary": {"moral_compass": -10},
    "Explorer": {"moral_compass": 5}
}

# Class adjustments
traits_stat_changes = {
    "Warlock": {"wisdom": 2, "strength": -1},
    "Sorcerer": {"wisdom": 2, "strength": -1},
    "Wizard": {"wisdom": 2, "strength": -1},
    "Druid": {"wisdom": 2, "strength": -1},
    "Cleric": {"wisdom": 2, "strength": -1},
    "Barbarian": {"strength": 2, "health": 25, "wisdom": -1},
    "Fighter": {"strength": 2, "health": 25, "wisdom": -1},
    "Paladin": {"strength": 2, "health": 25, "wisdom": -1},
    "Monk": {"wisdom": 3, "health": -15, "strength": -1}
}

# Race adjustments
ethnicity_stat_changes = {
    "Dark Elf": {"moral_compass": -10, "wisdom": 1},
    "Dragonborn": {"moral_compass": -5, "strength": 1},
    "Dwarf": {"strength": 1},
    "Elf": {"moral_compass": 5, "wisdom": 1},
    "Fairy": {"moral_compass": 10, "wisdom": 1},
    "Goliath": {"moral_compass": -5, "strength": 1},
    "Orc": {"moral_compass": -5, "strength": 1},
    "Human": {"charisma": 1}
}
def adjust_stats(ethnicity, personality, traits):
    # Initialize all stats
    moral_compass = 0
    reputation = 0
    rizz = 0
    battery = 0
    influence = 0
    skills = 0
    esteem = 0

    # Race adjustments
    ethnicity_changes = ethnicity_stat_changes.get(ethnicity, {})
    moral_compass += ethnicity_changes.get("moral_compass", 0)
    reputation += ethnicity_changes.get("reputation", 0)
    rizz += ethnicity_changes.get("rizz", 0)
    battery += ethnicity_changes.get("battery", 0)
    influence += ethnicity_changes.get("influence", 0)
    skills += ethnicity_changes.get("skills", 0)
    esteem += ethnicity_changes.get("esteem", 0)

    # Role adjustments
    personality_changes = personality_stat_changes.get(personality, {})
    moral_compass += personality_changes.get("moral_compass", 0)

    # Class adjustments
    traits_changes = traits_stat_changes.get(traits, {})
    moral_compass += traits_changes.get("moral_compass", 0)
    reputation += traits_changes.get("reputation", 0)
    rizz += traits_changes.get("rizz", 0)
    battery += traits_changes.get("battery", 0)
    influence += traits_changes.get("influence", 0)
    skills += traits_changes.get("skills", 0)
    esteem += traits_changes.get("esteem", 0)

    # Return the adjusted stats
    return {
        "moral_compass": moral_compass,
        "reputation": reputation,
        "rizz": rizz,
        "battery": battery,
        "influence": influence,
        "skills": skills,
        "esteem": esteem
    }

