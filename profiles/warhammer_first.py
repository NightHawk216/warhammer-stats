import json
import math

weapon_dict = {
    'Greatsword': {
        'strength': 2,
    },
}

class CharacterProfile:
    def __init__(self, character_profile):
        self.character_profile = {
            'movement': character_profile['movement'],
            'weapon_skill': character_profile['weapon_skill'],
            'ballistic_skill': character_profile['ballistic_skill'],
            'strength': character_profile['strength'],
            'toughness': character_profile['toughness'],
            'initiative': character_profile['initiative'],
            'attacks': character_profile['attacks'],
            'leadership': character_profile['leadership'],
        }

class WarhammerUnitStats:
    def __init__(self, unit_category, troop_type, faction, unit, base_size):
        self.unit_category = {
            'wounds': unit_category['wounds'],
            'save': unit_category['save'],
            'points_cost': unit_category['points_cost'],
            'models_per_unit': unit_category['models_per_unit'],
            'models_per_row': unit_category['models_per_row'],
            'rows': unit_category['models_per_unit'] // unit_category['models_per_row'],
            'leftover_models': unit_category['models_per_unit'] % unit_category['models_per_row'],
        }
        self.troop_type = troop_type
        self.faction = faction
        self.unit = unit
        self.base_size = {
            'width': base_size['width'],
            'depth': base_size['depth'],
        }
        self.unit_width = self.get_total_width()

    def get_total_width(self):
        return self.base_size['width'] * self.unit_category['models_per_row']

    def get_left_number(self):
        total_models = self.unit_category['models_per_unit']
        fractional_rows = math.ceil(total_models / self.unit_category['models_per_row'])
        return fractional_rows

    def get_right_number(self):
        total_models = self.unit_category['models_per_unit']
        fractional_rows = math.floor(total_models / self.unit_category['models_per_row'])
        return fractional_rows

    def get_left_length(self):
        total_models = self.unit_category['models_per_unit']
        fractional_rows = total_models % self.unit_category['models_per_row']
        return self.base_size['depth'] * self.get_left_number()

    def get_right_length(self):
        total_models = self.unit_category['models_per_unit']
        fractional_rows = total_models % self.unit_category['models_per_row']
        return self.base_size['depth'] * self.get_right_number()

    def total_attacks(self):
        number_that_can_attack = self.unit_category['models_per_row']

        return number_that_can_attack * self.character_profile['attacks']


class WarhammerUnit(WarhammerUnitStats, CharacterProfile):
    def __init__(self, data):
        CharacterProfile.__init__(self, data['character_profile'])
        WarhammerUnitStats.__init__(self, data['unit_category'], data['unit_type'], data['faction'], data['unit'], base_size=data['base_size'])
        self.data = data
        self.command = data['command']
        self.profile_extras = data.get('profile_extras', {})
        self.champion = self.get_champion_profile()

    def attacking_strength(self):
        return self.character_profile['strength'] + self.data['weapons']['strength']

    def get_champion_profile(self):
        champion_profile = self.character_profile.copy()
        if 'Champion' in self.profile_extras:
            for attr, extra in self.profile_extras['Champion'].items():
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



