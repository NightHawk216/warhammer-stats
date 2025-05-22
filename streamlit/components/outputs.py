"""Outputs component for Warhammer stats calculator."""

import streamlit as st
import streamlit.components.v1 as components
from utils import multiple_hits, multiple_wounds


def render_outputs(inputs: dict) -> None:
    """
    Renders the outputs for the Warhammer stats calculator based on the provided inputs.

    Iterates over the attacker stats and calculates the number of successful hits and wounds.
    Displays the results in a tabular format, including the required values to hit and wound,

    Parameters
    ----------
    inputs : dict
        A dictionary containing the following keys:
        - attacker_stats : list
            List of dictionaries with attacker stats.
        - show_dice_rolls : bool
            Whether to display individual dice rolls.
        - required_to_hit_list : list
            List of required values to hit for each attacker.
        - required_wound_list : list
            List of required values to wound for each attacker.
        - required_value_for_success_list : list
            List of required values for success.
        - the_type : str
            The type of calculation (e.g., "Combat", "Hits", "Wounds").
        - num_attackers : int
            The number of attackers.
        - defenders_stats : dict
            Dictionary containing defender stats.

    Returns
    -------
    None
    """
    
    attacker_stats = inputs['attacker_stats']
    show_dice_rolls = inputs['show_dice_rolls']
    required_to_hit_list = inputs['required_to_hit_list']
    required_wound_list = inputs['required_wound_list']
    required_value_for_success_list = inputs['required_value_for_success_list']
    the_type = inputs['the_type']
    num_attackers = inputs['num_attackers']
    hit_rerolls = inputs['hit_rerolls']
    wound_rerolls = inputs['wound_rerolls']

    # if the_type in ["Combat"]:
    defenders_stats = inputs['defenders_stats']
    if num_attackers:
        if st.button("Calculate Hits1"):
            total_successful_hit_rolls = []
            total_successful_wounds_rolls = []
            total_hit_roll_list = []
            total_wound_roll_list = []
            for attacker in inputs['attacker_stats']:
                attacker_weapon_skill = attacker['attacker_weapon_skill']
                attacker_strength = attacker['attacker_strength']
                num_success_hit_rolls = number_of_attacks = attacker['number_of_attacks']

                defender_weapon_skill = defenders_stats['defenders_weapon_skill']
                defender_toughness = defenders_stats['defenders_toughness']
            
                if number_of_attacks and attacker_weapon_skill:
                    num_success_hit_rolls, hit_roll_list = multiple_hits(attacker_weapon_skill, defender_weapon_skill, number_of_attacks, reroll_criteria=hit_rerolls)
                    total_successful_hit_rolls.append(num_success_hit_rolls)
                    total_hit_roll_list.append(hit_roll_list)

                if num_success_hit_rolls and attacker_strength:
                    # Calculate the number of successful wounds only if there are successful hits
                    num_success_wounds_rolls, wounds_roll_list = multiple_wounds(attacker_strength, defender_toughness, num_success_hit_rolls, reroll_criteria=wound_rerolls)
                    total_successful_wounds_rolls.append(num_success_wounds_rolls)
                    total_wound_roll_list.append(wounds_roll_list)
                else:
                    # If there are no successful hits, append 0 for wounds
                    total_successful_wounds_rolls.append(0)
                    total_wound_roll_list.append([])

            # Calculate the total number of hits
            num_hits_success = sum(total_successful_hit_rolls)
            num_wounds_success = sum(total_successful_wounds_rolls)

            for idx in range(num_attackers):
                # Display hits and wounds for the current attacker in a tabular format
                st.markdown(f"### Attacker {idx+1}")

                hits_row = ""
                wounds_row = ""

                if the_type in ["Combat", "Hits"]:
                    num_hits_success = total_successful_hit_rolls[idx]
                    required_to_hit_value = int(required_to_hit_list[idx][:-1])

                    # Process the hit_roll_list to create highlighted_first_rolls and highlighted_second_rolls
                    first_rolls = []
                    second_rolls = []

                    # Process first_rolls
                    for entry in total_hit_roll_list[idx]:
                        if entry['result'] == 'Hit':
                            first_rolls.append((entry['first_roll'], "<span style='color:green; font-weight:bold;'>{}</span>".format(entry['first_roll'])))
                        elif entry['result'] == 'Miss' and entry['second_roll'] is not None:
                            first_rolls.append((entry['first_roll'], "<span style='color:red; font-weight:bold;'>{}</span>".format(entry['first_roll'])))
                        else:
                            first_rolls.append((entry['first_roll'], "<span style='color:black;'>{}</span>".format(entry['first_roll'])))

                    # Sort first_rolls by the roll value
                    first_rolls.sort(key=lambda x: x[0])
                    highlighted_first_rolls = [highlight for _, highlight in first_rolls]

                    # Process second_rolls
                    for entry in total_hit_roll_list[idx]:
                        if entry['reroll'] and entry['second_roll'] is not None:
                            if entry['second_result'] == 'Hit':
                                second_rolls.append((entry['second_roll'], "<span style='color:green; font-weight:bold;'>{}</span>".format(entry['second_roll'])))
                            else:
                                second_rolls.append((entry['second_roll'], "<span style='color:black;'>{}</span>".format(entry['second_roll'])))

                    # Sort second_rolls by the roll value
                    second_rolls.sort(key=lambda x: x[0]) 
                    highlighted_second_rolls= [highlight for _, highlight in second_rolls]
                    if highlighted_second_rolls:
                        join_char  = " | "
                    else:
                        join_char = ""

                    hits_row = f"""
                        <td style='border: 1px solid black; padding: 8px; text-align: center;'>Hits</td>
                        <td style='border: 1px solid black; padding: 8px; text-align: center;'>{required_to_hit_value}+</td>
                        <td style='border: 1px solid black; padding: 8px; text-align: center;'>{', '.join(highlighted_first_rolls)} {join_char} {', '.join(highlighted_second_rolls)}</td>
                        <td style='border: 1px solid black; padding: 8px; text-align: center;'>{num_hits_success}</td>
                    """

                ##########################################################################

                if the_type in ["Combat", "Wounds"]:
                    num_hits_success = total_successful_wounds_rolls[idx]
                    required_to_wound_value = int(required_wound_list[idx][:-1])

                    # Process the hit_roll_list to create highlighted_first_rolls and highlighted_second_rolls
                    first_rolls = []
                    second_rolls = []

                    # Process first_rolls
                    for entry in total_wound_roll_list[idx]:
                        if entry['result'] == 'Wounded':
                            first_rolls.append((entry['first_roll'], "<span style='color:green; font-weight:bold;'>{}</span>".format(entry['first_roll'])))
                        elif entry['result'] == 'Does not wound' and entry['second_roll'] is not None:
                            first_rolls.append((entry['first_roll'], "<span style='color:red; font-weight:bold;'>{}</span>".format(entry['first_roll'])))
                        else:
                            first_rolls.append((entry['first_roll'], "<span style='color:black;'>{}</span>".format(entry['first_roll'])))

                    # Sort first_rolls by the roll value
                    first_rolls.sort(key=lambda x: x[0])
                    highlighted_first_rolls = [highlight for _, highlight in first_rolls]

                    # Process second_rolls
                    for entry in total_wound_roll_list[idx]:
                        if entry['reroll'] and entry['second_roll'] is not None:
                            if entry['second_result'] == 'Wounded':
                                second_rolls.append((entry['second_roll'], "<span style='color:green; font-weight:bold;'>{}</span>".format(entry['second_roll'])))
                            else:
                                second_rolls.append((entry['second_roll'], "<span style='color:black;'>{}</span>".format(entry['second_roll'])))

                    # Sort second_rolls by the roll value
                    second_rolls.sort(key=lambda x: x[0]) 
                    highlighted_second_rolls= [highlight for _, highlight in second_rolls]
                    if highlighted_second_rolls:
                        join_char  = " | "
                    else:
                        join_char = ""

                    wounds_row = f"""
                        <td style='border: 1px solid black; padding: 8px; text-align: center;'>Wounds</td>
                        <td style='border: 1px solid black; padding: 8px; text-align: center;'>{required_to_wound_value}+</td>
                        <td style='border: 1px solid black; padding: 8px; text-align: center;'>{', '.join(highlighted_first_rolls)} {join_char} {', '.join(highlighted_second_rolls)}</td>
                        <td style='border: 1px solid black; padding: 8px; text-align: center;'>{num_hits_success}</td>
                    """

            
                html = f"""
                <table style='width:100%; border: 1px solid black; border-collapse: collapse;'>
                    <tr style='border: 1px solid black;'>
                        <th style='border: 1px solid black; padding: 8px; text-align: center;'>Type</th>
                        <th style='border: 1px solid black; padding: 8px; text-align: center;'>Required</th>
                        <th style='border: 1px solid black; padding: 8px; text-align: center;'>Dice Rolls</th>
                        <th style='border: 1px solid black; padding: 8px; text-align: center;'>Count of Successes</th>
                    </tr>
                    <tr>
                        {hits_row}
                    </tr>
                    <tr>
                        {wounds_row}
                    </tr>
                </table>
                """

                components.html(html, scrolling=True)

            total_num_hits = sum(total_successful_hit_rolls)
            total_num_wounds = sum(total_successful_wounds_rolls)

            if the_type in ["Combat", "Hits"]:
                # Display total hits and wounds as plain text
                text = f"""
                Total Number of Hits: **{total_num_hits}**
                """
                st.write(f"{text}", unsafe_allow_html=True)

            if the_type in ["Hits"]:

                if total_num_wounds == 1:
                    st.markdown(f"<h1 style='font-size:100px; text-align:center;'>{total_num_hits} Hit</h1>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<h1 style='font-size:100px; text-align:center;'>{total_num_hits} Hits</h1>", unsafe_allow_html=True)

            if the_type in ["Combat", "Wounds"]:
                # Display total hits and wounds as plain text
                text = f"""
                Total Number of Wounds: **{total_num_wounds}**
                """
                st.write(f"{text}", unsafe_allow_html=True)

                if total_num_wounds == 1:
                    st.markdown(f"<h1 style='font-size:100px; text-align:center;'>{total_num_wounds} Wound</h1>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<h1 style='font-size:100px; text-align:center;'>{total_num_wounds} Wounds</h1>", unsafe_allow_html=True)