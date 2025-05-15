# poetry run streamlit run app.py

import streamlit as st
from components.inputs_hits import render_hit_inputs
from components.inputs_wounds import render_wounds_inputs
from components.outputs import render_outputs
from components.simulation import run_simulation_logic

import extra_streamlit_components as stx

st.title("Warhammer Simulation Tool")
st.markdown("#### Select one of the following options")
chosen_id = stx.tab_bar(data=[
    stx.TabBarItemData(id="tab1", title="Hits", description="Calculate the number of hits"),
    stx.TabBarItemData(id="tab2", title="Wounds", description="Calculate the number of wounds"),
])

placeholder = st.container()

if chosen_id == "tab1":
    st.header("Hits")

    # Render inputs
    inputs = render_hit_inputs()
    the_type = "Hits"

elif chosen_id == "tab2":
    st.header("Wounds")

    # Render inputs
    inputs = render_wounds_inputs()
    the_type = "Wounds"

else:
    inputs = {'run_simulation': False, 'show_dice_rolls': False, 'attacker_stats': [], 'defenders_stats': [], 'required_value_for_success': 0}
    the_type = None


# Run simulation logic
if inputs['run_simulation']:
    results = run_simulation_logic(inputs, the_type)
    # plot_results(results)
else:
    render_outputs(inputs, the_type)