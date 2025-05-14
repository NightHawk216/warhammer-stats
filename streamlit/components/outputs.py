import streamlit as st



def render_outputs(inputs):
    from utils import multiple_hits

    attacker_stats = inputs['attacker_stats']
    defenders_weapon_skill = inputs['defenders_weapon_skill']
    to_hit_chart = inputs['to_hit_chart']
    show_dice_rolls = inputs['show_dice_rolls']

    if st.button("Calculate Hits"):
        total_hits = []
        total_roll_list = []
        for attacker in inputs['attacker_stats']:
            attackers_weapon_skill = attacker['attacker_weapon_skill']
            number_of_attacks = attacker['number_of_attacks']
            if number_of_attacks:
                num_hits, roll_list = multiple_hits(attackers_weapon_skill, defenders_weapon_skill, number_of_attacks)
                total_hits.append(num_hits)
                total_roll_list.append(roll_list)
        # Calculate the total number of hits
        num_hits = sum(total_hits)

        for idx, (num_hits, roll_list) in enumerate(zip(total_hits, total_roll_list)):
            print(f"Attacker {idx + 1}: {num_hits} hits, rolls: {roll_list}")

            st.markdown(f"### Attacker {idx+1} Number of hits: {num_hits}")
            if show_dice_rolls:
                roll_list.sort(reverse=False)
                # Highlight dice rolls that are equal to or higher than the "required to hit" value
                required_to_hit_value = int(to_hit_chart[:-1])  # Extract the numeric value from the to-hit chart
                highlighted_rolls = [
                    f"<span style='color:green; font-weight:bold;'>{roll}</span>" if roll >= required_to_hit_value else str(roll)
                    for roll in roll_list
                ]
                # Split the title and values into separate lines
                st.markdown("### Dice Rolls:")
                # Make the font of the dice rolls bigger
                st.markdown(f"<p style='font-size:40px;'>{', '.join(highlighted_rolls)}</p>", unsafe_allow_html=True)