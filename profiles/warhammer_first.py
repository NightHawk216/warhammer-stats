"""Warhammer Profiles."""

import json
import math
import typing as t

weapon_dict = {
    "Greatsword": {
        "strength": 2,
    },
}


class CharacterProfile:
    """
    Represents the profile of a Warhammer character.

    Attributes
    ----------
    character_profile : dict
        A dictionary containing the character's attributes such as movement, weapon skill, ballistic skill, etc.
    """

    def __init__(self, character_profile: t.Dict[str, t.Any]) -> None:
        """
        Initialize a CharacterProfile instance.

        Parameters
        ----------
        character_profile : dict
            A dictionary containing the character's attributes.
        """
        self.character_profile = {
            "movement": character_profile["movement"],
            "weapon_skill": character_profile["weapon_skill"],
            "ballistic_skill": character_profile["ballistic_skill"],
            "strength": character_profile["strength"],
            "toughness": character_profile["toughness"],
            "initiative": character_profile["initiative"],
            "attacks": character_profile["attacks"],
            "leadership": character_profile["leadership"],
        }


class WarhammerUnitStats:
    """
    Represents the statistics of a Warhammer unit.

    Attributes
    ----------
    unit_category : dict
        A dictionary containing unit-specific attributes such as wounds, save, points cost, etc.
    troop_type : str
        The type of troop (e.g., infantry, cavalry).
    faction : str
        The faction to which the unit belongs.
    unit : str
        The name of the unit.
    base_size : dict
        A dictionary containing the width and depth of the unit's base.
    unit_width : int
        The total width of the unit.
    """

    def __init__(
        self, 
        unit_category: t.Dict[str, t.Any], 
        troop_type: str, 
        faction: str, 
        unit: str, 
        base_size: t.Dict[str, int]
    ) -> None:
        """
        Initialize a WarhammerUnitStats instance.

        Parameters
        ----------
        unit_category : dict
            A dictionary containing unit-specific attributes.
        troop_type : str
            The type of troop.
        faction : str
            The faction to which the unit belongs.
        unit : str
            The name of the unit.
        base_size : dict
            A dictionary containing the width and depth of the unit's base.
        """
        self.unit_category = {
            "wounds": unit_category["wounds"],
            "save": unit_category["save"],
            "points_cost": unit_category["points_cost"],
            "models_per_unit": unit_category["models_per_unit"],
            "models_per_row": unit_category["models_per_row"],
            "rows": unit_category["models_per_unit"] // unit_category["models_per_row"],
            "leftover_models": unit_category["models_per_unit"] % unit_category["models_per_row"],
        }
        self.troop_type = troop_type
        self.faction = faction
        self.unit = unit
        self.base_size = {
            "width": base_size["width"],
            "depth": base_size["depth"],
        }
        self.unit_width = self.get_total_width()

    def get_total_width(self) -> int:
        """
        Calculate the total width of the unit.

        Returns
        -------
        int
            The total width of the unit.
        """
        return self.base_size["width"] * self.unit_category["models_per_row"]

    def get_left_number(self) -> int:
        """
        Calculate the number of rows with leftover models.

        Returns
        -------
        int
            The number of rows with leftover models.
        """
        total_models = self.unit_category["models_per_unit"]
        fractional_rows = math.ceil(total_models / self.unit_category["models_per_row"])
        return fractional_rows

    def get_right_number(self) -> int:
        """
        Calculate the number of full rows without leftover models.

        Returns
        -------
        int
            The number of full rows without leftover models.
        """
        total_models = self.unit_category["models_per_unit"]
        fractional_rows = math.floor(
            total_models / self.unit_category["models_per_row"]
        )
        return fractional_rows

    def get_left_length(self) -> int:
        """
        Calculate the total depth of rows with leftover models.

        Returns
        -------
        int
            The total depth of rows with leftover models.
        """
        total_models = self.unit_category["models_per_unit"]
        return self.base_size["depth"] * self.get_left_number()

    def get_right_length(self) -> int:
        """
        Calculate the total depth of full rows without leftover models.

        Returns
        -------
        int
            The total depth of full rows without leftover models.
        """
        total_models = self.unit_category["models_per_unit"]
        return self.base_size["depth"] * self.get_right_number()

    def total_attacks(self) -> int:
        """
        Calculate the total number of attacks the unit can make.

        Returns
        -------
        int
            The total number of attacks.
        """
        number_that_can_attack = self.unit_category["models_per_row"]
        return number_that_can_attack * self.character_profile["attacks"]


class WarhammerUnit(WarhammerUnitStats, CharacterProfile):
    """
    Represents a Warhammer unit, combining stats and character profile.

    Attributes
    ----------
    data : dict
        The raw data used to initialize the unit.
    command : dict
        The command attributes of the unit.
    profile_extras : dict
        Additional profile attributes for specific roles (e.g., Champion).
    champion : dict
        The profile of the unit's champion.
    """

    def __init__(self, data: t.Dict[str, t.Any]) -> None:
        """
        Initialize a WarhammerUnit instance.

        Parameters
        ----------
        data : dict
            A dictionary containing all the data required to initialize the unit.
        """
        CharacterProfile.__init__(self, data["character_profile"])
        WarhammerUnitStats.__init__(
            self,
            data["unit_category"],
            data["unit_type"],
            data["faction"],
            data["unit"],
            base_size=data["base_size"],
        )
        self.data = data
        self.command = data["command"]
        self.profile_extras = data.get("profile_extras", {})
        self.champion = self.get_champion_profile()

    def attacking_strength(self) -> int:
        """
        Calculate the attacking strength of the unit.

        Returns
        -------
        int
            The attacking strength of the unit.
        """
        return self.character_profile["strength"] + self.data["weapons"]["strength"]

    def get_champion_profile(self) -> t.Dict[str, t.Any]:
        """
        Generate the profile for the unit's champion.

        Returns
        -------
        dict
            The champion's profile with additional attributes.
        """
        champion_profile = self.character_profile.copy()
        if "Champion" in self.profile_extras:
            for attr, extra in self.profile_extras["Champion"].items():
                champion_profile[attr] += extra
        return champion_profile


# Load JSON data into a Python dictionary
# with open('swordmasters.json', 'r') as f:
#     data = json.load(f)

# # Create a Swordmaster object from the dictionary
# swordmaster = WarhammerUnit(data)
# print(swordmaster.attacking_strength())
# # print(swordmaster.champion)

# # Load JSON data into a Python dictionary
# with open('white_lions.json', 'r') as f:
#     data = json.load(f)

# # Create a Swordmaster object from the dictionary
# white_lions = WarhammerUnit(data)
# print(white_lions.character_profile)
# print(white_lions.champion)
# print(white_lions.base_size)
# print(white_lions.get_total_width())
# print(white_lions.get_left_number())
# print(white_lions.get_left_length())
# print(white_lions.get_right_number())
# print(white_lions.get_right_length())

# print(white_lions.total_attacks())
