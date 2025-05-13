"""Attacking module for Warhammer The Old World combat simulator."""
import json
import random
from argparse import ArgumentParser

with open('profiles/swordmasters.json', 'r') as f:
    sm_data = json.load(f)

with open('profiles/white_lions.json', 'r') as f:
    wl_data = json.load(f)

with open('profiles/spearmen.json', 'r') as f:
    sp_data = json.load(f)

from profiles.warhammer_first import WarhammerUnit
from utils import multiple_wounds, attack_to_wound, combat



def main():
    parser = ArgumentParser()
    parser.add_argument('-a', '--attackers_skill', type=int)
    parser.add_argument('-d', '--defenders_skill', type=int)
    parser.add_argument('-n', '--number_of_attacks', type=int, default=1)
    args = parser.parse_args()

    # print(multiple_attacks(args.attackers_skill, args.defenders_skill, args.number_of_attacks))

    swordmaster = WarhammerUnit(sm_data)
    white_lions = WarhammerUnit(wl_data)
    spearmen = WarhammerUnit(data=sp_data)

    combat(swordmaster, spearmen)

if __name__ == '__main__':
    main()  
