import streamlit as st

from utils import warhammer_to_hit_chart

def render_hit_inputs():
    show_dice_rolls = st.checkbox("Show Dice Rolls", value=True, key="show_dice_rolls_hits")

    # Add a toggle button to show/hide the second row
    show_second_attacker = st.checkbox("Add Second Attacker (think champion, hero, or lord)", value=False, key="add_weapon_skill_hits")
    
    run_simulation = st.checkbox("Run Simulation", value=False, key="run_simulation_hits")

    attacker_stats = [] 

    st.markdown(f"###### Main Attacker")
    col1, col2 = st.columns([1, 1])
    with col1:
        attackers_weapon_skill = st.number_input("Attacker's Weapon Skill", min_value=1, max_value=10, value=4, step=1, key="main_weapon_skill_hits")
    with col2:
        number_of_attacks = st.number_input("Number of Attacks", min_value=1, max_value=100, value=4, step=1, key="main_attacks_hits")

    attacker_stats.append({"attacker_weapon_skill": attackers_weapon_skill, "number_of_attacks": number_of_attacks, "attacker_num": 1})

    # Render the second row based on the toggle state
    if show_second_attacker:
        st.markdown(f"###### Second Attacker")
        col1, col2 = st.columns([1, 1])
        with col1:
            second_weapon_skill = st.number_input("Attacker's Weapon Skill", min_value=1, max_value=10, value=5, step=1, key="second_weapon_skill")
        with col2:
            second_number_of_attacks = st.number_input("Number of Attacks", min_value=1, max_value=100, value=3, step=1, key="second_attacks")
            
    else:
        second_weapon_skill = 0
        second_number_of_attacks = 0

    attacker_stats.append({"attacker_weapon_skill": second_weapon_skill, "number_of_attacks": second_number_of_attacks, "attacker_num": 2})

    # Display total number of attacks
    total_number_of_dice_rolls = number_of_attacks + second_number_of_attacks
    st.markdown(f"### Total Number of Attacks: {total_number_of_dice_rolls}")

    st.markdown(f"###### Defender")
    defenders_weapon_skill = st.number_input("Defender's Weapon Skill", min_value=1, max_value=10, value=3, step=1)
    
    st.markdown("### To-Hit Value Needed")
    required_value_for_success = warhammer_to_hit_chart(attackers_weapon_skill, defenders_weapon_skill)
    st.markdown(f"**Main Attacker:** {required_value_for_success}")

    required_value_for_success_list = []
    required_value_for_success_list.append(required_value_for_success)

    if second_weapon_skill > 0:
        second_required_value_for_success = warhammer_to_hit_chart(second_weapon_skill, defenders_weapon_skill)
        st.markdown(f"**Second Attacker:** {second_required_value_for_success}")
        required_value_for_success_list.append(second_required_value_for_success)
    

    col1, col2 = st.columns(2)

    return {
        "show_dice_rolls": show_dice_rolls,
        "run_simulation": run_simulation,
        "attacker_stats": attacker_stats,
        "defenders_stats": defenders_weapon_skill,
        "total_number_of_dice_rolls": total_number_of_dice_rolls,
        "required_value_for_success_list": required_value_for_success_list,
        "required_to_hit_list": [],
        "required_wound_list": [],
    }