import streamlit as st

def warhammer_to_wound_chart(attacker_strength, defender_toughness):
    difference = attacker_strength - defender_toughness
    value = ""
    if difference == -1:
        value = '5+'
    elif difference == 0:
        value = '4+'
    elif difference == 1:
        value = '3+'
    elif difference >= 2:
        value = '2+'
    elif difference <= -2 and difference >= -5:
        value = '6+'
    else:
        value = 'Impossible'
    return value

def warhammer_to_hit_chart(attackers_weapon_skill, defenders_weapon_skill):
    value = ""
    if attackers_weapon_skill >= defenders_weapon_skill * 2 + 1:
        value = '2+'
    elif attackers_weapon_skill > defenders_weapon_skill:
        value = '3+'
    elif defenders_weapon_skill >= attackers_weapon_skill * 2 + 1:
        value = '5+'
    else:
        value = '4+'
    return value

def render_combat_inputs():
    show_dice_rolls = st.checkbox("Show Dice Rolls", value=True, key="show_dice_rolls_combat")

    # Add a toggle button to show/hide the second row
    show_second_attacker = st.checkbox("Add Second Attacker (think champion, hero, or lord)", value=False, key="add_weapon_skill_combat")
    
    # run_simulation = st.checkbox("Run Simulation", value=False, key="run_simulation_combat")
    run_simulation = False

    attacker_stats = [] 

    st.markdown(f"###### Main Attacker")
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        attacker_weapon_skill = st.number_input("Attacker's Weapon Skill", min_value=1, max_value=10, value=4, step=1, key="main_combat_weapon_skill")
    with col2:
        attacker_strength = st.number_input("Attacker's Strength", min_value=1, max_value=10, value=4, step=1, key="main_combat")
    with col3:
        number_of_attacks = st.number_input("Number of Attacks", min_value=1, max_value=100, value=4, step=1, key="main_attacks")

    attacker_stats.append({"attacker_weapon_skill": attacker_weapon_skill, "attacker_strength": attacker_strength, "number_of_attacks": number_of_attacks, "attacker_num": 1})

    # Render the second row based on the toggle state
    if show_second_attacker:
        st.markdown(f"###### Second Attacker")
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            second_weapon_skill = st.number_input("Attacker's Weapon Skill", min_value=1, max_value=10, value=7, step=1, key="second_weapon_skill")
        with col2:
            second_strength = st.number_input("Attacker's Strength", min_value=1, max_value=100, value=4, step=1, key="seconds_strength")
        with col3:
            second_number_of_attacks = st.number_input("Number of Attacks", min_value=1, max_value=100, value=4, step=1, key="seconds_attacks")
            
    else:
        second_weapon_skill = 0
        second_strength = 0
        second_number_of_attacks = 0

    attacker_stats.append({"attacker_weapon_skill": second_weapon_skill, "attacker_strength": second_weapon_skill, "number_of_attacks": second_number_of_attacks, "attacker_num": 2})

    # Display total number of attacks
    total_number_of_dice_rolls = number_of_attacks + second_number_of_attacks
    st.markdown(f"### Total Number of Hits: {total_number_of_dice_rolls}")

    st.markdown(f"###### Defender")
    defenders_weapon_skill = st.number_input("Defender's Weapon Skill", min_value=1, max_value=10, value=3, step=1, key="defender_weapon_skill")
    defenders_toughness = st.number_input("Defender's Toughness", min_value=1, max_value=10, value=3, step=1, key="defender_toughness")

    defender_stats = {"defenders_weapon_skill": defenders_weapon_skill, "defenders_toughness": defenders_toughness}

    # Weapon Skill
    
    required_to_hit_list = []
    required_wound_list = []

    to_hit_success = warhammer_to_hit_chart(attacker_weapon_skill, defenders_weapon_skill)
    required_to_hit_list.append(to_hit_success)

    if second_weapon_skill > 0:
        second_to_hit_success = warhammer_to_hit_chart(second_weapon_skill, defenders_weapon_skill)
        required_to_hit_list.append(second_to_hit_success)


    st.markdown("### To-Hit Value Needed")
    st.markdown(f"**Main Attacker:**     {attacker_weapon_skill} vs {defenders_weapon_skill} : {to_hit_success}")
    if second_weapon_skill > 0:
        st.markdown(f"**Second Attacker:** {second_weapon_skill} vs {defenders_weapon_skill} : {second_to_hit_success}")

    # Toughness
    
    required_wound_list = []

    wound_success = warhammer_to_wound_chart(attacker_strength, defenders_toughness)
    required_wound_list.append(wound_success)

    if second_strength > 0:
        second_wound_success = warhammer_to_wound_chart(second_strength, defenders_toughness)
        required_wound_list.append(second_wound_success)


    st.markdown("### Wound Value Needed")
    st.markdown(f"**Main Attacker:**     {attacker_strength} vs {defenders_toughness} :{wound_success}")
    if second_strength > 0:
        st.markdown(f"**Second Attacker:** {second_strength} vs {defenders_toughness} :{second_wound_success}")

    col1, col2 = st.columns(2)

    return {
        "show_dice_rolls": show_dice_rolls,
        "run_simulation": run_simulation,
        "attacker_stats": attacker_stats,
        "defenders_stats": defender_stats,
        "total_number_of_dice_rolls": total_number_of_dice_rolls,
        "required_value_for_success_list": [],
        "required_to_hit_list": required_to_hit_list,
        "required_wound_list": required_wound_list,
    }