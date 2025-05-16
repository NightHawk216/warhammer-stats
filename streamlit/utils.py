"""Utility functions."""

import random
from typing import List, Tuple

def warhammer_to_hit_chart(attackers_weapon_skill: int, defenders_weapon_skill: int) -> str:
    """
    Determines the required roll to hit based on the attacker's and defender's weapon skills.

    Parameters
    ----------
    attackers_weapon_skill : int
        The weapon skill of the attacker.
    defenders_weapon_skill : int
        The weapon skill of the defender.

    Returns
    -------
    str
        The required roll to hit (e.g., '2+', '3+').
    """
    value = ""
    if attackers_weapon_skill >= defenders_weapon_skill * 2 + 1:
        value = '2+'
    elif attackers_weapon_skill > defenders_weapon_skill:
        value = '3+'
    elif defenders_weapon_skill >= attackers_weapon_skill * 2 + 1:
        value = '5+'
    else:
        value = '4+'
    return value

def calc_hit(attackers_weapon_skill: int, defenders_weapon_skill: int, required_roll: int = -1, log: bool = False) -> Tuple[str, int]:
    """
    Simulates a single attack roll to determine if it hits.

    Parameters
    ----------
    attackers_weapon_skill : int
        The weapon skill of the attacker.
    defenders_weapon_skill : int
        The weapon skill of the defender.
    required_roll : int, optional
        The required roll to hit (default is -1, which calculates it automatically).
    log : bool, optional
        Whether to log the details of the roll (default is False).

    Returns
    -------
    tuple
        A tuple containing the outcome ('Hit' or 'Miss') and the roll value.
    """
    # Calculate the required roll to hit
    if required_roll == -1:
        required_roll = warhammer_to_hit_chart(attackers_weapon_skill, defenders_weapon_skill)
    required_roll_value = int(required_roll[:-1])  # Remove the '+' and convert to int

    # Roll a D6
    roll = random.randint(1, 6)

    # Print out the details
    if log:
        print(f"Attacker's weapon skill: {attackers_weapon_skill}")
        print(f"Defender's weapon skill: {defenders_weapon_skill}")
        print(f"Required to hit: {required_roll}")
        print(f"Rolled: {roll}")

    # Check if the roll is successful
    outcome = ""
    if roll >= required_roll_value:
        outcome = "Hit"
    else:
        outcome = "Miss"
    return outcome, roll

def multiple_hits(attackers_weapon_skill: int, defenders_weapon_skill: int, num_attacks: int, show_results: bool = True, log: bool = False) -> Tuple[int, List[int]]:
    """
    Simulates multiple attack rolls to determine the number of successful hits.

    Parameters
    ----------
    attackers_weapon_skill : int
        The weapon skill of the attacker.
    defenders_weapon_skill : int
        The weapon skill of the defender.
    num_attacks : int
        The number of attacks to simulate.
    show_results : bool, optional
        Whether to display the results (default is True).
    log : bool, optional
        Whether to log the details of the rolls (default is False).

    Returns
    -------
    tuple
        A tuple containing the number of successful hits and a list of roll values.
    """
    successful_hits = 0
    required_roll = warhammer_to_hit_chart(attackers_weapon_skill, defenders_weapon_skill)

    # Print out the details
    if log:
        print(f"Attacker's weapon skill: {attackers_weapon_skill}")
        print(f"Defender's weapon skill: {defenders_weapon_skill}")
        print(f"Required to hit: {required_roll}")

    roll_list = []

    for _ in range(num_attacks):
        result, dice_value = calc_hit(attackers_weapon_skill, defenders_weapon_skill, required_roll)
        roll_list.append(dice_value)
        if result == "Hit":
            successful_hits += 1

    hit_percentage = (successful_hits / num_attacks) * 100
    
    # Print out the details
    if log:
        print(f"Number of successful hits: {successful_hits}\n")
    # print(f"Hit percentage: {hit_percentage}%")

    return successful_hits, roll_list 

def multiple_wounds(attacker_strength: int, defender_toughness: int, num_attacks: int) -> Tuple[int, List[int]]:
    """
    Simulates multiple wound rolls to determine the number of successful wounds.

    Parameters
    ----------
    attacker_strength : int
        The strength of the attacker.
    defender_toughness : int
        The toughness of the defender.
    num_attacks : int
        The number of attacks to simulate.

    Returns
    -------
    tuple
        A tuple containing the number of successful wounds and a list of roll values.
    """
    successful_hits = 0
    required_roll = warhammer_to_wound_chart(attacker_strength, defender_toughness)
    print(f"Attacker's strength: {attacker_strength}")
    print(f"Defender's toughness: {defender_toughness}")
    print(f"Required to wound: {required_roll}")

    roll_list = []

    for _ in range(num_attacks):
        result, dice_value = calc_wound(attacker_strength, defender_toughness, required_roll)
        roll_list.append(dice_value)
        if result == "Wounded":
            successful_hits += 1

    hit_percentage = (successful_hits / num_attacks) * 100

    print(f"Number of successful wounds: {successful_hits}\n")
    # print(f"Wound percentage: {hit_percentage}%")

    return successful_hits, roll_list

def calc_wound(attacker_strength: int, defender_toughness: int, required_roll: int = -1, log: bool = False) -> Tuple[str, int]:
    """
    Simulates a single wound roll to determine if it wounds.

    Parameters
    ----------
    attacker_strength : int
        The strength of the attacker.
    defender_toughness : int
        The toughness of the defender.
    required_roll : int, optional
        The required roll to wound (default is -1, which calculates it automatically).
    log : bool, optional
        Whether to log the details of the roll (default is False).

    Returns
    -------
    tuple
        A tuple containing the outcome ('Wounded' or 'Does not wound') and the roll value.
    """
    # Calculate the required roll to wound
    if required_roll == -1:
        required_roll = warhammer_to_wound_chart(attacker_strength, defender_toughness)
    required_roll_value = int(required_roll[:-1])  # Remove the '+' and convert to int

    # Roll a D6
    roll = random.randint(1, 6)

    # Print out the details
    if log:
        print(f"Attacker's strength: {attacker_strength}")
        print(f"Defender's toughness: {defender_toughness}")
        print(f"Required to wound: {required_roll}")
        print(f"Rolled: {roll}")

    # Check if the roll is successful
    values = ""
    if roll >= required_roll_value:
        value = "Wounded"
    else:
        value = "Does not wound"
    return value, roll

def warhammer_to_wound_chart(attacker_strength: int, defender_toughness: int) -> str:
    """
    Determines the required roll to wound based on the attacker's strength and defender's toughness.

    Parameters
    ----------
    attacker_strength : int
        The strength of the attacker.
    defender_toughness : int
        The toughness of the defender.

    Returns
    -------
    str
        The required roll to wound (e.g., '2+', '3+').
    """
    difference = attacker_strength - defender_toughness
    value = ""
    if difference == -1:
        value = '5+'
    elif difference == 0:
        value = '4+'
    elif difference == 1:
        value = '3+'
    elif difference >= 2:
        value = '2+'
    elif difference <= -2 and difference >= -5:
        value = '6+'
    else:
        value = 'Impossible'
    return value

def warhammer_to_wound_chart(attacker_strength: int, defender_toughness: int) -> str:
    """
    Determines the required roll to wound based on the attacker's strength and defender's toughness.

    Parameters
    ----------
    attacker_strength : int
        The strength of the attacker.
    defender_toughness : int
        The toughness of the defender.

    Returns
    -------
    str
        The required roll to wound (e.g., '2+', '3+').
    """
    difference = attacker_strength - defender_toughness
    value = ""
    if difference == -1:
        value = '5+'
    elif difference == 0:
        value = '4+'
    elif difference == 1:
        value = '3+'
    elif difference >= 2:
        value = '2+'
    elif difference <= -2 and difference >= -5:
        value = '6+'
    else:
        value = 'Impossible'
    return value

def warhammer_to_hit_chart(attackers_weapon_skill: int, defenders_weapon_skill: int) -> str:
    """
    Determines the required roll to hit based on the attacker's and defender's weapon skills.

    Parameters
    ----------
    attackers_weapon_skill : int
        The weapon skill of the attacker.
    defenders_weapon_skill : int
        The weapon skill of the defender.

    Returns
    -------
    str
        The required roll to hit (e.g., '2+', '3+').
    """
    value = ""
    if attackers_weapon_skill >= defenders_weapon_skill * 2 + 1:
        value = '2+'
    elif attackers_weapon_skill > defenders_weapon_skill:
        value = '3+'
    elif defenders_weapon_skill >= attackers_weapon_skill * 2 + 1:
        value = '5+'
    else:
        value = '4+'
    return value

# from profiles.warhammer_first import WarhammerUnit



# def warhammer_to_wound_chart(attacker_strength, defender_toughness):
#     difference = attacker_strength - defender_toughness
#     if difference == -1:
#         return '5+'
#     elif difference == 0:
#         return '4+'
#     elif difference == 1:
#         return '3+'
#     elif difference >= 2:
#         return '2+'
#     elif difference <= -2 and difference >= -5:
#         return '6+'
#     else:
#         return 'Impossible'

# def calc_wound(attacker_strength, defender_toughness, required_roll=-1, log=False):
#     # Calculate the required roll to wound
#     if required_roll == -1:
#         required_roll = warhammer_to_wound_chart(attacker_strength, defender_toughness)
#     required_roll_value = int(required_roll[:-1])  # Remove the '+' and convert to int

#     # Roll a D6
#     roll = random.randint(1, 6)

#     # Print out the details
#     if log:
#         print(f"Attacker's strength: {attacker_strength}")
#         print(f"Defender's toughness: {defender_toughness}")
#         print(f"Required to wound: {required_roll}")
#         print(f"Rolled: {roll}")

#     # Check if the roll is successful
#     if roll >= required_roll_value:
#         return "Wounded"
#     else:
#         return "Does not wound"

# def multiple_wounds(attacker_strength, defender_toughness, num_attacks):
#     successful_hits = 0
#     required_roll = warhammer_to_wound_chart(attacker_strength, defender_toughness)
#     print(f"Attacker's strength: {attacker_strength}")
#     print(f"Defender's toughness: {defender_toughness}")
#     print(f"Required to wound: {required_roll}")

#     for _ in range(num_attacks):
#         result = calc_wound(attacker_strength, defender_toughness, required_roll)
#         if result == "Wounded":
#             successful_hits += 1

#     hit_percentage = (successful_hits / num_attacks) * 100

#     print(f"Number of successful wounds: {successful_hits}\n")
#     # print(f"Wound percentage: {hit_percentage}%")

#     return successful_hits

# def sort_units_by_initiative(unit1: WarhammerUnit, unit2: WarhammerUnit) -> dict:
#     """
#     Sorts two Warhammer units by their initiative values in descending order.

#     Parameters
#     ----------
#     unit1 : WarhammerUnit
#         The first unit to compare.
#     unit2 : WarhammerUnit
#         The second unit to compare.

#     Returns
#     -------
#     dict
#         A dictionary where the keys are the WarhammerUnit instances and the values are their initiatives. 
#         The dictionary is sorted in descending order by initiative.

#     """
#     units_with_initiatives = {unit1: unit1.character_profile['initiative'], unit2: unit2.character_profile['initiative']}
#     sorted_units_with_initiatives = dict(sorted(units_with_initiatives.items(), key=lambda item: item[1], reverse=True))
#     return sorted_units_with_initiatives


# def combat(attacker_unit: WarhammerUnit, defender_unit: WarhammerUnit):
#     """
#     Simulates a combat round between two Warhammer units.

#     Parameters
#     ----------
#     attacker_unit : WarhammerUnit
#         The unit that is attacking.
#     defender_unit : WarhammerUnit
#         The unit that is defending.

#     Returns
#     -------
#     tuple
#         A tuple containing the number of successful hits and the hit percentage.

#     """
#     sorted_units = sort_units_by_initiative(attacker_unit, defender_unit)

#     number_of_attacks = attacker_unit.total_attacks()

#     # Attacker attacks first
#     print("---------Attacks---------")
#     print(f"Starting Attacks: {number_of_attacks}")
#     # To Hit
#     hits = attack_to_hit(attacker_unit, defender_unit)
#     # To Wound 
#     wounds = attack_to_wound(attacker_unit, defender_unit, hits)
#     # Armor Save
#     print(f"you did {wounds} wounds\n")

#     # Calculate Returning Attacks
#     number_of_returning_attacks = defender_unit.total_attacks() - wounds
#     print("---------Attacks Back---------")
#     print(f"Returning Attacks: {number_of_returning_attacks}")

#     # Secondary attacks
#     # To Hit
#     hits = attack_to_hit(defender_unit, attacker_unit, number_of_returning_attacks)
#     # To Wound 
#     wounds = attack_to_wound(defender_unit, attacker_unit, hits)
#     # Armor Save
#     print(f"they did {wounds} wounds back")

# def attack_to_hit(attacker_unit, defender_unit, num_attacks=-1):
#     if num_attacks == 0:
#         return 0
#     if num_attacks == -1:
#         num_attacks = attacker_unit.total_attacks()
#     attackers_weapon_skill = attacker_unit.character_profile['weapon_skill']
#     defenders_weapon_skill = defender_unit.character_profile['weapon_skill']
#     return multiple_hits(attackers_weapon_skill, defenders_weapon_skill, num_attacks)[0]

# def attack_to_wound(attacker_unit, defender_unit, num_attacks=-1):
#     if num_attacks == 0:
#         return 0
#     if num_attacks == -1:
#         num_attacks = attacker_unit.total_attacks()
#     attacker_strength = attacker_unit.attacking_strength()
#     defender_toughness = defender_unit.character_profile['toughness']
#     return multiple_wounds(attacker_strength, defender_toughness, num_attacks)