import streamlit as st

from components.utils import warhammer_to_hit_chart

def render_inputs():
    show_dice_rolls = st.checkbox("Show Dice Rolls", value=True)
    run_simulation = st.checkbox("Run Simulation", value=False)
    # Use Streamlit columns to place the first two number inputs on the same line
    col1, col2 = st.columns(2)

    with col1:
        attackers_weapon_skill = st.number_input("Attacker's Weapon Skill", min_value=1, max_value=10, value=7, step=1)

    with col2:
        defenders_weapon_skill = st.number_input("Defender's Weapon Skill", min_value=1, max_value=10, value=3, step=1)
    # attackers_weapon_skill = st.number_input("Attacker's Weapon Skill", min_value=1, max_value=10, value=7, step=1)
    # defenders_weapon_skill = st.number_input("Defender's Weapon Skill", min_value=1, max_value=10, value=3, step=1)
    
    st.markdown("### To-Hit Value Needed")
    # Display the to-hit chart
    to_hit_chart = warhammer_to_hit_chart(attackers_weapon_skill, defenders_weapon_skill)
    st.markdown(f"**Required to hit:** {to_hit_chart}")

    col1, col2 = st.columns(2)

    # Use Streamlit columns to make the buttons less wide
    with col1:

        # User input for number of attacks
        number_of_attacks = st.number_input("Number of Attacks", min_value=1, max_value=20, value=6, step=1)
        

    return {
        "show_dice_rolls": show_dice_rolls,
        "run_simulation": run_simulation,
        "attackers_weapon_skill": attackers_weapon_skill,
        "defenders_weapon_skill": defenders_weapon_skill,
        "number_of_attacks": number_of_attacks,
        "to_hit_chart": to_hit_chart,
    }