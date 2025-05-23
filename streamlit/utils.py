"""Utility functions."""

import random
from typing import Dict, Any, List, Tuple


def warhammer_to_hit_chart(
    attackers_weapon_skill: int, defenders_weapon_skill: int
) -> str:
    """
    Determine the required roll to hit based on the attacker's and defender's weapon skills.

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
        value = "2+"
    elif attackers_weapon_skill > defenders_weapon_skill:
        value = "3+"
    elif defenders_weapon_skill >= attackers_weapon_skill * 2 + 1:
        value = "5+"
    else:
        value = "4+"
    return value


def calc_hit(
    attackers_weapon_skill: int,
    defenders_weapon_skill: int,
    required_roll: int = -1,
    log: bool = False,
) -> Tuple[str, int]:
    """
    Simulate a single attack roll to determine if it hits.

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
        required_roll = warhammer_to_hit_chart(
            attackers_weapon_skill, defenders_weapon_skill
        )
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


def multiple_hits(
    attackers_weapon_skill: int,
    defenders_weapon_skill: int,
    num_attacks: int,
    show_results: bool = True,
    reroll_criteria: dict = {},
    log: bool = False,
) -> Tuple[int, List[int]]:
    """
    Simulate multiple attack rolls to determine the number of successful hits.

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
    reroll_criteria : dict, optional
        A dictionary containing criteria for rerolls (default is empty).
    log : bool, optional
        Whether to log the details of the rolls (default is False).

    Returns
    -------
    tuple
        A tuple containing
         - the number of successful hits
         - a sorted list of all roll values
         - a sorted list of successful roll values
         - a sorted list of failed roll values
    """
    successful_hits = 0
    required_roll = warhammer_to_hit_chart(
        attackers_weapon_skill, defenders_weapon_skill
    )

    # Print out the details
    if log:
        print(f"Attacker's weapon skill: {attackers_weapon_skill}")
        print(f"Defender's weapon skill: {defenders_weapon_skill}")
        print(f"Required to hit: {required_roll}")

    roll_list = []
    success_list = []
    fail_list = []

    for _ in range(num_attacks):
        result, dice_value = calc_hit(
            attackers_weapon_skill, defenders_weapon_skill, required_roll
        )
        die_roll = {
            "first_roll": dice_value,
            "result": result,
            "reroll": reroll_criteria,
            "second_roll": None,
            "second_result": None,
            "reroll_type": None,
        }
        # provide logic here to determine if reroll is needed
        if reroll_criteria["reroll_1s"] and result == "Miss" and dice_value == 1:
            result_2, dice_value_2 = calc_hit(
                attackers_weapon_skill, defenders_weapon_skill, required_roll
            )
            die_roll.update(
                {
                    "second_roll": dice_value_2,
                    "second_result": result_2,
                    "reroll_type": "reroll_1s",
                }
            )
        # provide logic here to determine if reroll is needed
        elif reroll_criteria["reroll_fail_hits"] and result == "Miss":
            result_2, dice_value_2 = calc_hit(
                attackers_weapon_skill, defenders_weapon_skill, required_roll
            )
            die_roll.update(
                {
                    "second_roll": dice_value_2,
                    "second_result": result_2,
                    "reroll_type": "reroll_fail_hits",
                }
            )
        elif reroll_criteria["reroll_suc_hits"] and result == "Hit":
            result_2, dice_value_2 = calc_hit(
                attackers_weapon_skill, defenders_weapon_skill, required_roll
            )
            die_roll.update(
                {
                    "second_roll": dice_value_2,
                    "second_result": result_2,
                    "reroll_type": "reroll_suc_hits",
                }
            )
        roll_list.append(die_roll)
        if die_roll["result"] == "Hit" and not reroll_criteria["reroll_suc_hits"]:
            successful_hits += 1
            success_list.append(die_roll["first_roll"])
        elif die_roll["second_result"] == "Hit":
            successful_hits += 1
            success_list.append(die_roll["second_roll"])

    return successful_hits, roll_list


def multiple_wounds(
    attacker_strength: int,
    defender_toughness: int,
    num_attacks: int,
    reroll_criteria: dict = {},
) -> Tuple[int, List[int]]:
    """
    Simulate multiple wound rolls to determine the number of successful wounds.

    Parameters
    ----------
    attacker_strength : int
        The strength of the attacker.
    defender_toughness : int
        The toughness of the defender.
    num_attacks : int
        The number of attacks to simulate.
    reroll_criteria : dict, optional
        A dictionary containing criteria for rerolls (default is empty).

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
    success_list = []
    fail_list = []

    for _ in range(num_attacks):
        print("reroll_criteria", reroll_criteria)
        result, dice_value = calc_wound(
            attacker_strength, defender_toughness, required_roll
        )
        print(result)
        die_roll = {
            "first_roll": dice_value,
            "result": result,
            "reroll": reroll_criteria,
            "second_roll": None,
            "second_result": None,
            "reroll_type": None,
        }
        # provide logic here to determine if reroll is needed
        if (
            reroll_criteria["reroll_1s"]
            and result == "Does not wound"
            and dice_value == 1
        ):
            result_2, dice_value_2 = calc_hit(
                attacker_strength, defender_toughness, required_roll
            )
            die_roll.update(
                {
                    "second_roll": dice_value_2,
                    "second_result": result_2,
                    "reroll_type": "reroll_1s",
                }
            )
        # provide logic here to determine if reroll is needed
        elif reroll_criteria["reroll_fail_wounds"] and result == "Does not wound":
            result_2, dice_value_2 = calc_hit(
                attacker_strength, defender_toughness, required_roll
            )
            die_roll.update(
                {
                    "second_roll": dice_value_2,
                    "second_result": result_2,
                    "reroll_type": "reroll_fail_wounds",
                }
            )
        elif reroll_criteria["reroll_suc_wounds"] and result == "Wounded":
            result_2, dice_value_2 = calc_hit(
                attacker_strength, defender_toughness, required_roll
            )
            die_roll.update(
                {
                    "second_roll": dice_value_2,
                    "second_result": result_2,
                    "reroll_type": "reroll_suc_wounds",
                }
            )
        roll_list.append(die_roll)
        if result == "Wounded":
            successful_hits += 1
            success_list.append(dice_value)
        else:
            fail_list.append(dice_value)

    return successful_hits, roll_list


def calc_wound(
    attacker_strength: int,
    defender_toughness: int,
    required_roll: int = -1,
    log: bool = False,
) -> Tuple[str, int]:
    """
    Simulate a single wound roll to determine if it wounds.

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
    Determine the required roll to wound based on the attacker's strength and defender's toughness.

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
        value = "5+"
    elif difference == 0:
        value = "4+"
    elif difference == 1:
        value = "3+"
    elif difference >= 2:
        value = "2+"
    elif difference <= -2 and difference >= -5:
        value = "6+"
    else:
        value = "Impossible"
    return value


def warhammer_to_hit_chart(
    attackers_weapon_skill: int, defenders_weapon_skill: int
) -> str:
    """
    Determine the required roll to hit based on the attacker's and defender's weapon skills.

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
        value = "2+"
    elif attackers_weapon_skill > defenders_weapon_skill:
        value = "3+"
    elif defenders_weapon_skill >= attackers_weapon_skill * 2 + 1:
        value = "5+"
    else:
        value = "4+"
    return value


class WarhammerUnit:
    """
    Represents a Warhammer unit with attributes and methods for combat simulation.

    Attributes
    ----------
    character_profile : dict
        The profile of the character, including attributes like weapon skill, strength, etc.
    unit_category : dict
        The category of the unit, including attributes like wounds, save, and points cost.
    base_size : dict
        The dimensions of the unit's base.
    """

    def __init__(
        self,
        character_profile: Dict[str, Any],
        unit_category: Dict[str, Any],
        base_size: Dict[str, int],
    ) -> None:
        """
        Initialize a WarhammerUnit instance with character profile, unit category, and base size.

        Parameters
        ----------
        character_profile : dict
            The profile of the character.
        unit_category : dict
            The category of the unit.
        base_size : dict
            The dimensions of the unit's base.
        """
        self.character_profile = character_profile
        self.unit_category = unit_category
        self.base_size = base_size

    def total_attacks(self) -> int:
        """
        Calculate the total number of attacks the unit can make.

        Returns
        -------
        int
            The total number of attacks.
        """
        return self.unit_category["models_per_row"] * self.character_profile["attacks"]


def sort_units_by_initiative(unit1: WarhammerUnit, unit2: WarhammerUnit) -> Dict[WarhammerUnit, int]:
    """
    Sort two Warhammer units by their initiative values in descending order.

    Parameters
    ----------
    unit1 : WarhammerUnit
        The first unit to compare.
    unit2 : WarhammerUnit
        The second unit to compare.

    Returns
    -------
    dict
        A dictionary mapping WarhammerUnit instances to their initiative values, sorted in descending order.
    """
    units_with_initiatives = {
        unit1: unit1.character_profile['initiative'],
        unit2: unit2.character_profile['initiative']
    }
    return dict(sorted(units_with_initiatives.items(), key=lambda item: item[1], reverse=True))


def combat(attacker_unit: WarhammerUnit, defender_unit: WarhammerUnit) -> Tuple[int, float]:
    """
    Simulate a combat round between two Warhammer units.

    Parameters
    ----------
    attacker_unit : WarhammerUnit
        The unit that is attacking.
    defender_unit : WarhammerUnit
        The unit that is defending.

    Returns
    -------
    tuple
        A tuple containing the number of successful hits and the hit percentage.
    """
    sorted_units = sort_units_by_initiative(attacker_unit, defender_unit)

    number_of_attacks = attacker_unit.total_attacks()

    # Attacker attacks first
    print("---------Attacks---------")
    print(f"Starting Attacks: {number_of_attacks}")
    # To Hit
    hits = attack_to_hit(attacker_unit, defender_unit)
    # To Wound
    wounds = attack_to_wound(attacker_unit, defender_unit, hits)
    # Armor Save
    print(f"you did {wounds} wounds\n")

    # Calculate Returning Attacks
    number_of_returning_attacks = defender_unit.total_attacks() - wounds
    print("---------Attacks Back---------")
    print(f"Returning Attacks: {number_of_returning_attacks}")

    # Secondary attacks
    # To Hit
    hits = attack_to_hit(defender_unit, attacker_unit, number_of_returning_attacks)
    # To Wound
    wounds = attack_to_wound(defender_unit, attacker_unit, hits)
    # Armor Save
    print(f"they did {wounds} wounds back")


def attack_to_hit(attacker_unit: WarhammerUnit, defender_unit: WarhammerUnit, num_attacks: int = -1) -> int:
    """
    Calculate the number of successful hits in an attack.

    Parameters
    ----------
    attacker_unit : WarhammerUnit
        The unit that is attacking.
    defender_unit : WarhammerUnit
        The unit that is defending.
    num_attacks : int, optional
        The number of attacks to simulate (default is -1, which uses the total attacks of the attacker).

    Returns
    -------
    int
        The number of successful hits.
    """
    if num_attacks == 0:
        return 0
    if num_attacks == -1:
        num_attacks = attacker_unit.total_attacks()
    attackers_weapon_skill = attacker_unit.character_profile['weapon_skill']
    defenders_weapon_skill = defender_unit.character_profile['weapon_skill']
    return multiple_hits(attackers_weapon_skill, defenders_weapon_skill, num_attacks)[0]


def attack_to_wound(attacker_unit: WarhammerUnit, defender_unit: WarhammerUnit, num_attacks: int = -1) -> int:
    """
    Calculate the number of successful wounds in an attack.

    Parameters
    ----------
    attacker_unit : WarhammerUnit
        The unit that is attacking.
    defender_unit : WarhammerUnit
        The unit that is defending.
    num_attacks : int, optional
        The number of attacks to simulate (default is -1, which uses the total attacks of the attacker).

    Returns
    -------
    int
        The number of successful wounds.
    """
    if num_attacks == 0:
        return 0
    if num_attacks == -1:
        num_attacks = attacker_unit.total_attacks()
    attacker_strength = attacker_unit.attacking_strength()
    defender_toughness = defender_unit.character_profile['toughness']
    return multiple_wounds(attacker_strength, defender_toughness, num_attacks)
