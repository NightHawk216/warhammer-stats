import streamlit as st
from components.inputs import render_inputs
from components.outputs import render_outputs
from components.simulation import run_simulation_logic

# Streamlit app title
st.title("Warhammer To-Hit Chart")

# Render inputs
inputs = render_inputs()

# Run simulation logic
if inputs['run_simulation']:
    results = run_simulation_logic(inputs)
    # plot_results(results)
else:
    render_outputs(inputs)