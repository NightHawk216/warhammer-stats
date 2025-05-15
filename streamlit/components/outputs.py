import streamlit as st



def render_outputs(inputs, the_type):
    from utils import multiple_hits, multiple_wounds

    attacker_stats = inputs['attacker_stats']
    defenders_stats = inputs['defenders_stats']
    required_value_for_success = inputs['required_value_for_success']
    show_dice_rolls = inputs['show_dice_rolls']
    the_type = the_type

    print(f"the_type: {the_type}")
    if the_type:
        if st.button("Calculate Hits"):
            total_successful_rolls = []
            total_roll_list = []
            for attacker in inputs['attacker_stats']:
                if the_type == "Hits":
                    attackers_weapon_skill = attacker['attacker_weapon_skill']
                    number_of_attacks = attacker['number_of_attacks']
                    print(f"here", number_of_attacks)
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
            num_success = sum(total_successful_rolls)

            for idx, (num_success, roll_list) in enumerate(zip(total_successful_rolls, total_roll_list)):
                print(f"Attacker {idx + 1}: {num_success} {the_type}, rolls: {roll_list}")

                st.markdown(f"### Attacker {idx+1} Number of {the_type}: {num_success}")
                if show_dice_rolls:
                    roll_list.sort(reverse=False)
                    # Highlight dice rolls that are equal to or higher than the "required to hit" value
                    required_to_hit_value = int(required_value_for_success[:-1])  # Extract the numeric value from the to-hit chart
                    highlighted_rolls = [
                        f"<span style='color:green; font-weight:bold;'>{roll}</span>" if roll >= required_to_hit_value else str(roll)
                        for roll in roll_list
                    ]
                    # Split the title and values into separate lines
                    st.markdown("### Dice Rolls:")
                    # Make the font of the dice rolls bigger
                    st.markdown(f"<p style='font-size:40px;'>{', '.join(highlighted_rolls)}</p>", unsafe_allow_html=True)