import streamlit as st



def render_outputs(inputs):
    from utils import multiple_hits

    attackers_weapon_skill = inputs['attackers_weapon_skill']
    defenders_weapon_skill = inputs['defenders_weapon_skill']
    number_of_attacks = inputs['number_of_attacks']
    to_hit_chart = inputs['to_hit_chart']
    show_dice_rolls = inputs['show_dice_rolls']

    if st.button("Calculate Hits"):
        num_hits, roll_list = multiple_hits(attackers_weapon_skill, defenders_weapon_skill, number_of_attacks)
        st.markdown(f"### Number of hits: {num_hits}")
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