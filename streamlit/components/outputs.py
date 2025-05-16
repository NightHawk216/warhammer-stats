import streamlit as st


def render_outputs(inputs, the_type):
    from utils import multiple_hits, multiple_wounds

    attacker_stats = inputs['attacker_stats']
    show_dice_rolls = inputs['show_dice_rolls']
    required_to_hit_list = inputs['required_to_hit_list']
    required_wound_list = inputs['required_wound_list']
    required_value_for_success_list = inputs['required_value_for_success_list']
    the_type = the_type

    if the_type in ["Hits", "Wounds"]:
        defenders_stats = inputs['defenders_stats']
        if st.button("Calculate Hits"):
            total_successful_rolls = []
            total_roll_list = []
            for attacker in inputs['attacker_stats']:
                if the_type == "Hits":
                    attackers_weapon_skill = attacker['attacker_weapon_skill']
                    number_of_attacks = attacker['number_of_attacks']
                    if number_of_attacks:
                        num_success_rolls, roll_list = multiple_hits(attackers_weapon_skill, defenders_stats, number_of_attacks)
                        total_successful_rolls.append(num_success_rolls)
                        total_roll_list.append(roll_list)
                if the_type == "Wounds":
                    attacker_strength = attacker['attacker_strength']
                    number_of_attacks = attacker['number_of_attacks']
                    if number_of_attacks:
                        num_success_rolls, roll_list = multiple_wounds(attacker_strength, defenders_stats, number_of_attacks)
                        total_successful_rolls.append(num_success_rolls)
                        total_roll_list.append(roll_list)
            # Calculate the total number of hits
            total_num_success = sum(total_successful_rolls)

            for idx, (num_success, roll_list) in enumerate(zip(total_successful_rolls, total_roll_list)):
                print(f"Attacker {idx + 1}: {num_success} {the_type}, rolls: {roll_list}")

                st.markdown(f"### Attacker {idx+1}")

                # Highlight dice rolls for hits
                required_value_for_success = int(required_value_for_success_list[idx][:-1])
                highlighted_hit_rolls = [
                    f"<span style='color:green; font-weight:bold;'>{roll}</span>" if roll >= required_value_for_success else str(roll)
                    for roll in roll_list
                ]

                highlighted_hit_rolls.sort(reverse=False)  # Sort dice rolls

                # Create a table for hits and wounds
                st.markdown(
                    f"""
                    <table style='width:100%; border: 1px solid black; border-collapse: collapse;'>
                        <tr style='border: 1px solid black;'>
                            <th style='border: 1px solid black; padding: 8px;'>Type</th>
                            <th style='border: 1px solid black; padding: 8px;'>Required</th>
                            <th style='border: 1px solid black; padding: 8px;'>Dice Rolls</th>
                            <th style='border: 1px solid black; padding: 8px;'># of Successes</th>
                        </tr>
                        <tr style='border: 1px solid black;'>
                            <td style='border: 1px solid black; padding: 8px;'>Hits</td>
                            <td style='border: 1px solid black; padding: 8px;'>{required_value_for_success}+</td>
                            <td style='border: 1px solid black; padding: 8px;'>{', '.join(highlighted_hit_rolls)}</td>
                            <td style='border: 1px solid black; padding: 8px;'>{num_success}</td>
                        </tr>
                    </table>
                    """,
                    unsafe_allow_html=True
                )


            if total_num_success == 1:
                st.markdown(f"<h1 style='font-size:100px; text-align:center;'>{total_num_success} {the_type[:-1]}</h1>", unsafe_allow_html=True)
            else:
                st.markdown(f"<h1 style='font-size:100px; text-align:center;'>{total_num_success} {the_type}</h1>", unsafe_allow_html=True)

                # st.markdown(f"### Attacker {idx+1} Number of {the_type}: {num_success}")
                # if show_dice_rolls:
                #     roll_list.sort(reverse=False)
                #     # Highlight dice rolls that are equal to or higher than the "required to hit" value
                #     required_to_hit_value = int(required_value_for_success_list[idx][:-1])  # Extract the numeric value from the to-hit chart
                #     highlighted_rolls = [
                #         f"<span style='color:green; font-weight:bold;'>{roll}</span>" if roll >= required_to_hit_value else str(roll)
                #         for roll in roll_list
                #     ]
                #     # Split the title and values into separate lines
                #     st.markdown("### Dice Rolls:")
                #     # Make the font of the dice rolls bigger
                #     st.markdown(f"<p style='font-size:40px;'>{', '.join(highlighted_rolls)}</p>", unsafe_allow_html=True)

    if the_type in ["Combat"]:
        defenders_stats = inputs['defenders_stats']
        if st.button("Calculate Hits"):
            total_successful_hit_rolls = []
            total_successful_wounds_rolls = []
            total_hit_roll_list = []
            total_wound_roll_list = []
            for attacker in inputs['attacker_stats']:
                attacker_weapon_skill = attacker['attacker_weapon_skill']
                attacker_strength = attacker['attacker_strength']
                number_of_attacks = attacker['number_of_attacks']

                defender_weapon_skill = defenders_stats['defenders_weapon_skill']
                defender_toughness = defenders_stats['defenders_toughness']
            
                if number_of_attacks:
                    num_success_hit_rolls, hit_roll_list = multiple_hits(attacker_weapon_skill, defender_weapon_skill, number_of_attacks)
                    total_successful_hit_rolls.append(num_success_hit_rolls)
                    total_hit_roll_list.append(hit_roll_list)

                    if num_success_hit_rolls:
                        # Calculate the number of successful wounds only if there are successful hits
                        num_success_wounds_rolls, wounds_roll_list = multiple_wounds(attacker_strength, defender_toughness, num_success_hit_rolls)
                        total_successful_wounds_rolls.append(num_success_wounds_rolls)
                        total_wound_roll_list.append(wounds_roll_list)
                    else:
                        # If there are no successful hits, append 0 for wounds
                        total_successful_wounds_rolls.append(0)
                        total_wound_roll_list.append([])

                    
            # Calculate the total number of hits
            num_hits_success = sum(total_successful_hit_rolls)
            num_wounds_success = sum(total_successful_wounds_rolls)

            for idx in range(len(total_successful_hit_rolls)):
                # Display hits and wounds for the current attacker in a tabular format
                num_hits_success = total_successful_hit_rolls[idx]
                total_hit_roll_list_for_attacker = sorted(total_hit_roll_list[idx])  # Sort dice rolls
                num_wounds_success = total_successful_wounds_rolls[idx]
                total_wound_roll_list_for_attacker = sorted(total_wound_roll_list[idx])  # Sort dice rolls

                st.markdown(f"### Attacker {idx+1}")

                # Highlight dice rolls for hits
                required_to_hit_value = int(required_to_hit_list[idx][:-1])
                highlighted_hit_rolls = [
                    f"<span style='color:green; font-weight:bold;'>{roll}</span>" if roll >= required_to_hit_value else str(roll)
                    for roll in total_hit_roll_list_for_attacker
                ]

                # Highlight dice rolls for wounds
                required_to_wound_value = int(required_wound_list[idx][:-1])
                highlighted_wound_rolls = [
                    f"<span style='color:green; font-weight:bold;'>{roll}</span>" if roll >= required_to_wound_value else str(roll)
                    for roll in total_wound_roll_list_for_attacker
                ]

                # Create a table for hits and wounds
                st.markdown(
                    f"""
                    <table style='width:100%; border: 1px solid black; border-collapse: collapse;'>
                        <tr style='border: 1px solid black;'>
                            <th style='border: 1px solid black; padding: 8px;'>Type</th>
                            <th style='border: 1px solid black; padding: 8px;'>Required</th>
                            <th style='border: 1px solid black; padding: 8px;'>Dice Rolls</th>
                            <th style='border: 1px solid black; padding: 8px;'># of Successes</th>
                        </tr>
                        <tr style='border: 1px solid black;'>
                            <td style='border: 1px solid black; padding: 8px;'>Hits</td>
                            <td style='border: 1px solid black; padding: 8px;'>{required_to_hit_value}+</td>
                            <td style='border: 1px solid black; padding: 8px;'>{', '.join(highlighted_hit_rolls)}</td>
                            <td style='border: 1px solid black; padding: 8px;'>{num_hits_success}</td>
                        </tr>
                        <tr style='border: 1px solid black;'>
                            <td style='border: 1px solid black; padding: 8px;'>Wounds</td>
                            <td style='border: 1px solid black; padding: 8px;'>{required_to_wound_value}+</td>
                            <td style='border: 1px solid black; padding: 8px;'>{', '.join(highlighted_wound_rolls)}</td>
                            <td style='border: 1px solid black; padding: 8px;'>{num_wounds_success}</td>
                        </tr>
                    </table>
                    """,
                    unsafe_allow_html=True
                )
            st.markdown(f"### Total")

            total_num_wounds = sum(total_successful_wounds_rolls)

            # Display total hits and wounds as plain text
            text = f"""
            Total Number of Hits: **{sum(total_successful_hit_rolls)}**
            <br>
            Total Number of Wounds: **{total_num_wounds}**
            """
            st.write(f"{text}", unsafe_allow_html=True)


            if total_num_wounds == 1:
                st.markdown(f"<h1 style='font-size:100px; text-align:center;'>{total_num_wounds} Wound</h1>", unsafe_allow_html=True)
            else:
                st.markdown(f"<h1 style='font-size:100px; text-align:center;'>{total_num_wounds} Wounds</h1>", unsafe_allow_html=True)