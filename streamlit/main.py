"""Main page of warhammer simulation tool.

Cmd:
 - poetry run streamlit run app.py
"""



import streamlit as st
from components.inputs import render_inputs
from components.outputs import render_outputs
from components.simulation import run_simulation_logic

import extra_streamlit_components as stx

st.title("Warhammer Simulation Tool")
chosen_id = stx.tab_bar(
    data=[
        stx.TabBarItemData(
            id="tab1", title="Hits and Wounds", description="Simulate combat"
        ),
        stx.TabBarItemData(id="tab2", title="Hits", description="Calculate hits"),
        stx.TabBarItemData(id="tab3", title="Wounds", description="Calculate wounds"),
    ]
)

placeholder = st.container()

if chosen_id == "tab1":
    st.header("Combat")

    # Render inputs
    inputs = render_inputs("Combat")

elif chosen_id == "tab2":
    st.header("Hits")

    # Render inputs
    inputs = render_inputs("Hits")

elif chosen_id == "tab3":
    st.header("Wounds")

    # Render inputs
    inputs = render_inputs("Wounds")

else:
    inputs = {
        "run_simulation": False,
        "show_dice_rolls": False,
        "attacker_stats": [],
        "defenders_stats": [],
        "required_value_for_success": 0,
        "required_value_for_success_list": [],
        "required_to_hit_list": [],
        "required_wound_list": [],
        "the_type": None,
        "num_attackers": 0,
        "rerolls": {},
        "hit_rerolls": {},
        "wound_rerolls": {},
    }
    the_type = None


# Run simulation logic
if inputs["run_simulation"]:
    results = run_simulation_logic(inputs, the_type)
    # plot_results(results)
else:
    render_outputs(inputs)
