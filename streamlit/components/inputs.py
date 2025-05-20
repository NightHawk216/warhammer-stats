import streamlit as st

from utils import warhammer_to_hit_chart, warhammer_to_wound_chart

def get_combat_stats(show_second_attacker: bool) -> list:
    """
    Collects combat stats for one or two attackers based on user input.

    Parameters
    ----------
    show_second_attacker : bool
        Whether to include a second attacker in the stats.

    Returns
    -------
    list
        A list of dictionaries containing stats for each attacker.
    """
    # Add a toggle button to show/hide the second row

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

    attacker_stats.append({"attacker_weapon_skill": second_weapon_skill, "attacker_strength": second_strength, "number_of_attacks": second_number_of_attacks, "attacker_num": 2})

    return attacker_stats

def get_hits_stats(show_second_attacker: bool) -> list:
    """
    Collects hit stats for one or two attackers based on user input.

    Parameters
    ----------
    show_second_attacker : bool
        Whether to include a second attacker in the stats.

    Returns
    -------
    list
        A list of dictionaries containing hit stats for each attacker.
    """
    # Add a toggle button to show/hide the second row

    attacker_stats = [] 

    st.markdown(f"###### Main Attacker")
    col1, col2 = st.columns([1, 1])
    with col1:
        attacker_weapon_skill = st.number_input("Attacker's Weapon Skill", min_value=1, max_value=10, value=4, step=1, key="main_hits_weapon_skill")
    with col2:
        number_of_attacks = st.number_input("Number of Attacks", min_value=1, max_value=100, value=4, step=1, key="main_hits_attacks")

    attacker_stats.append({"attacker_weapon_skill": attacker_weapon_skill, "attacker_strength": 0, "number_of_attacks": number_of_attacks, "attacker_num": 1})

    # Render the second row based on the toggle state
    if show_second_attacker:
        st.markdown(f"###### Second Attacker")
        col1, col2 = st.columns([1, 1])
        with col1:
            second_weapon_skill = st.number_input("Attacker's Weapon Skill", min_value=1, max_value=10, value=7, step=1, key="second_hits_weapon_skill")
        with col2:
            second_number_of_attacks = st.number_input("Number of Attacks", min_value=1, max_value=100, value=4, step=1, key="seconds_hits_attacks")
            
    else:
        second_weapon_skill = 0
        second_strength = 0
        second_number_of_attacks = 0

    attacker_stats.append({"attacker_weapon_skill": second_weapon_skill, "attacker_strength": 0, "number_of_attacks": second_number_of_attacks, "attacker_num": 2})

    return attacker_stats



def get_wounds_stats(show_second_attacker: bool) -> list:
    """
    Collects wound stats for one or two attackers based on user input.

    Parameters
    ----------
    show_second_attacker : bool
        Whether to include a second attacker in the stats.

    Returns
    -------
    list
        A list of dictionaries containing wound stats for each attacker.
    """
    # Add a toggle button to show/hide the second row

    attacker_stats = [] 

    st.markdown(f"###### Main Attacker")
    col1, col2 = st.columns([1, 1])
    with col1:
        attacker_strength = st.number_input("Attacker's Strength", min_value=1, max_value=10, value=4, step=1, key="main_combat")
    with col2:
        number_of_attacks = st.number_input("Number of Attacks", min_value=1, max_value=100, value=4, step=1, key="main_attacks")

    attacker_stats.append({"attacker_weapon_skill": 0, "attacker_strength": attacker_strength, "number_of_attacks": number_of_attacks, "attacker_num": 1})

    # Render the second row based on the toggle state
    if show_second_attacker:
        st.markdown(f"###### Second Attacker")
        col1, col2 = st.columns([1, 1])
        with col1:
            second_strength = st.number_input("Attacker's Strength", min_value=1, max_value=100, value=4, step=1, key="seconds_strength")
        with col2:
            second_number_of_attacks = st.number_input("Number of Attacks", min_value=1, max_value=100, value=4, step=1, key="seconds_attacks")
            
    else:
        second_strength = 0
        second_number_of_attacks = 0

    attacker_stats.append({"attacker_weapon_skill": 0, "attacker_strength": second_strength, "number_of_attacks": second_number_of_attacks, "attacker_num": 2})

    return attacker_stats


def render_inputs(the_type: str) -> dict:
    """
    Renders input fields for the Warhammer stats calculator and collects user input.

    Collects both attacker and defender stats, including weapon skill, strength, and number of attacks for one or two attackers.

    Parameters
    ----------
    the_type : str
        The type of calculation (e.g., "Combat", "Hits", "Wounds").

    Returns
    -------
    dict
        A dictionary containing user inputs and calculated stats.
    """
    show_dice_rolls = st.checkbox("Show Dice Rolls", value=True, key="show_dice_rolls_combat")

    show_second_attacker = st.checkbox("Add Second Attacker (think champion, hero, or lord)", value=False, key="add_weapon_skill_combat")

    num_attackers = 2 if show_second_attacker else 1

    # run_simulation = st.checkbox("Run Simulation", value=False, key="run_simulation_combat")
    run_simulation = False

    if the_type == "Combat":
        attacker_stats = get_combat_stats(show_second_attacker)
    if the_type == "Hits":
        attacker_stats = get_hits_stats(show_second_attacker)
    if the_type == "Wounds":
        attacker_stats = get_wounds_stats(show_second_attacker)

    # Display total number of attacks
    total_number_of_dice_rolls  = sum([attacker['number_of_attacks'] for attacker in attacker_stats])
    # total_number_of_dice_rolls = attacker_stats[0]['number_of_attacks'] + attacker_stats[1]['number_of_attacks']
    st.markdown(f"### Total Number of Hits: {total_number_of_dice_rolls}")

    st.markdown(f"###### Defender")
    defenders_weapon_skill = st.number_input("Defender's Weapon Skill", min_value=1, max_value=10, value=3, step=1, key="defender_weapon_skill")
    defenders_toughness = st.number_input("Defender's Toughness", min_value=1, max_value=10, value=3, step=1, key="defender_toughness")

    defender_stats = {"defenders_weapon_skill": defenders_weapon_skill, "defenders_toughness": defenders_toughness}

    # Weapon Skill
    
    required_to_hit_list = []
    required_wound_list = []

    attacker_weapon_skill = attacker_stats[0]['attacker_weapon_skill']
    second_weapon_skill = attacker_stats[1]['attacker_weapon_skill']

    attacker_strength = attacker_stats[0]['attacker_strength']
    second_strength = attacker_stats[1]['attacker_strength']

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
    st.markdown(f"**Main Attacker:**     {attacker_strength} vs {defenders_toughness} : {wound_success}")
    if second_strength > 0:
        st.markdown(f"**Second Attacker:** {second_strength} vs {defenders_toughness} : {second_wound_success}")

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
        "the_type": the_type,
        "num_attackers": num_attackers,
    }