import streamlit as st
from utils import multiple_hits

def run_simulation_logic(inputs):

    # Initialize 'last_simulation_results' in session state if it doesn't exist
    if 'last_simulation_results' not in st.session_state:
        st.session_state['last_simulation_results'] = None
        
    number_of_runs = st.number_input("Number of Runs", min_value=1, max_value=10000, value=20, step=1)

    attacker_stats = inputs['attacker_stats']
    defenders_weapon_skill = inputs['defenders_weapon_skill']
    total_number_of_attacks = inputs['total_number_of_attacks']
    to_hit_chart = inputs['to_hit_chart']
    show_dice_rolls = inputs['show_dice_rolls']

    if st.button("Simulate Combat"):
        import matplotlib.pyplot as plt
        import numpy as np

        total_hits = []
        total_roll_list = []

        # Run the simulation
        results = []
        for _ in range(number_of_runs):

            total_hits = 0

            for attacker in inputs['attacker_stats']:
                attackers_weapon_skill = attacker['attacker_weapon_skill']
                number_of_attacks = attacker['number_of_attacks']
                if number_of_attacks:
                    num_hits, _ = multiple_hits(attackers_weapon_skill, defenders_weapon_skill, number_of_attacks)
                    total_hits += num_hits

            results.append(total_hits)

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
            df = pd.DataFrame({'Number of Hits': results})

            # Plot the histogram with the current color
            fig = px.histogram(df, x='Number of Hits', nbins=20, title="Simulation Results: Number of Hits")
            fig.update_traces(marker=dict(color=current_color, line=dict(color='black', width=1)))
            fig.update_layout(xaxis_title="Number of Hits", yaxis_title="Frequency")

            # Add percentages to the top of the bars in the Plotly histogram
            counts = df['Number of Hits'].value_counts().sort_index()
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
            st.markdown("### Current Simulation Results: Number of Hits")
            st.plotly_chart(fig)

            # Display the previous simulation results below the current results
            if previous_results:
                st.markdown("### Previous Simulation Results: Number of Hits")

                # Create a DataFrame for the previous results
                prev_df = pd.DataFrame({'Number of Hits': previous_results})

                # Plot the histogram for the previous results
                prev_fig = px.histogram(prev_df, x='Number of Hits', nbins=20, title="Previous Simulation Results: Number of Hits")
                prev_fig.update_traces(marker=dict(color=previous_color, line=dict(color='black', width=1)))
                prev_fig.update_layout(xaxis_title="Number of Hits", yaxis_title="Frequency")

                # Add percentages to the top of the bars in the previous results histogram
                prev_counts = prev_df['Number of Hits'].value_counts().sort_index()
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