import streamlit as st
from utils import multiple_hits, multiple_wounds

def run_simulation_logic(inputs, the_type):

    # Initialize 'last_simulation_results' in session state if it doesn't exist
    if 'last_simulation_results' not in st.session_state:
        st.session_state['last_simulation_results'] = None
        
    number_of_runs = st.number_input("Number of Runs", min_value=1, max_value=10000, value=20, step=1)

    attacker_stats = inputs['attacker_stats']
    defenders_stats = inputs['defenders_stats']
    total_number_of_dice_rolls = inputs['total_number_of_dice_rolls']
    required_value_for_success_list = inputs['required_value_for_success_list']
    show_dice_rolls = inputs['show_dice_rolls']
    the_type = the_type

    if st.button("Simulate Combat"):
        import matplotlib.pyplot as plt
        import numpy as np

        total_successful_rolls = []
        total_roll_list = []

        # Run the simulation
        results = []
        for _ in range(number_of_runs):

            total_successes = 0

            for attacker in inputs['attacker_stats']:
                if the_type == "Hits":
                    attackers_weapon_skill = attacker['attacker_weapon_skill']
                    number_of_attacks = attacker['number_of_attacks']
                    if number_of_attacks:
                        num_success_rolls, roll_list = multiple_hits(attackers_weapon_skill, defenders_stats, number_of_attacks)
                        total_successful_rolls.append(num_success_rolls)
                        total_roll_list.append(roll_list)
                        total_successes += num_success_rolls
                if the_type == "Wounds":
                    attacker_strength = attacker['attacker_strength']
                    number_of_attacks = attacker['number_of_attacks']
                    if number_of_attacks:
                        num_success_rolls, roll_list = multiple_wounds(attacker_strength, defenders_stats, number_of_attacks)
                        total_successful_rolls.append(num_success_rolls)
                        total_roll_list.append(roll_list)
                        total_successes += num_success_rolls

            results.append(total_successes)

        show_labels = True
        if show_labels:
            import plotly.express as px
            import pandas as pd
            import random

            # Define available colors
            available_colors = ["blue", "green", "red", "purple", "orange", "gray"]

            # Ensure the new graph color is not the same as the last graph color
            if 'last_graph_color' not in st.session_state:
                st.session_state['last_graph_color'] = None

            current_color = random.choice([color for color in available_colors if color != st.session_state['last_graph_color']])

            # Update the last graph color in session state
            st.session_state['last_graph_color'] = current_color

            # Create a DataFrame for Plotly
            df = pd.DataFrame({f'Number of {the_type}': results})

            # Plot the histogram with the current color
            fig = px.histogram(df, x=f'Number of {the_type}', nbins=20, title=f"Simulation Results: Number of {the_type}")
            fig.update_traces(marker=dict(color=current_color, line=dict(color='black', width=1)))
            fig.update_layout(xaxis_title=f'Number of {the_type}', yaxis_title="Frequency")

            # Add percentages to the top of the bars in the Plotly histogram
            counts = df[f'Number of {the_type}'].value_counts().sort_index()
            total = counts.sum()
            percentages = [(count / total) * 100 for count in counts]

            for x, percentage in zip(counts.index, percentages):
                fig.add_annotation(
                    x=x, 
                    y=counts[x], 
                    text=f'{percentage:.1f}%',
                    showarrow=False,
                    font=dict(size=10, color='black'),
                    yshift=10
                )

            # Store the current results and color in session state only after displaying the previous results
            previous_results = st.session_state['last_simulation_results']['results'] if st.session_state['last_simulation_results'] else []
            previous_color = st.session_state['last_simulation_results']['color'] if st.session_state['last_simulation_results'] else "gray"

            # Display the current simulation results first
            # st.markdown(f"### Current Simulation Results: Number of {the_type}")
            st.plotly_chart(fig)

            # Display the previous simulation results below the current results
            if previous_results:
                # st.markdown(f"### Previous Simulation Results: Number of {the_type}")

                # Create a DataFrame for the previous results
                prev_df = pd.DataFrame({f'Number of {the_type}': previous_results})

                # Plot the histogram for the previous results
                prev_fig = px.histogram(prev_df, x=f'Number of {the_type}', nbins=20, title=f"Previous Simulation Results: Number of {the_type}")
                prev_fig.update_traces(marker=dict(color=previous_color, line=dict(color='black', width=1)))
                prev_fig.update_layout(xaxis_title=f"Number of {the_type}", yaxis_title="Frequency")

                # Add percentages to the top of the bars in the previous results histogram
                prev_counts = prev_df[f'Number of {the_type}'].value_counts().sort_index()
                prev_total = prev_counts.sum()
                prev_percentages = [(count / prev_total) * 100 for count in prev_counts]

                for x, percentage in zip(prev_counts.index, prev_percentages):
                    prev_fig.add_annotation(
                        x=x, 
                        y=prev_counts[x], 
                        text=f'{percentage:.1f}%',
                        showarrow=False,
                        font=dict(size=10, color='black'),
                        yshift=10
                    )

                st.plotly_chart(prev_fig)

            # Save the current results and color to session state after displaying the previous results
            st.session_state['last_simulation_results'] = {'results': results, 'color': current_color}