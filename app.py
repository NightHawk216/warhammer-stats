import streamlit as st
from utils import warhammer_to_hit_chart, multiple_hits

# Streamlit app title
st.title("Warhammer To-Hit Chart")

# Add a toggle at the top of the page for showing dice rolls
show_dice_rolls = st.checkbox("Show Dice Rolls", value=True)

# Add a toggle at the top of the page for running a simulation
run_simulation = st.checkbox("Run Simulation", value=True)

# Add a toggle at the top of the page for running a simulation
# show_labels = st.checkbox("Show Labels", value=True)
show_labels = True

# Initialize 'last_simulation_results' in session state if it doesn't exist
if 'last_simulation_results' not in st.session_state:
    st.session_state['last_simulation_results'] = None

# Use Streamlit columns to place the first two number inputs on the same line
col1, col2 = st.columns(2)

with col1:
    attackers_weapon_skill = st.number_input("Attacker's Weapon Skill", min_value=1, max_value=10, value=7, step=1)

with col2:
    defenders_weapon_skill = st.number_input("Defender's Weapon Skill", min_value=1, max_value=10, value=3, step=1)

st.markdown("### To-Hit Value Needed")
# Display the to-hit chart
to_hit_chart = warhammer_to_hit_chart(attackers_weapon_skill, defenders_weapon_skill)
st.markdown(f"**Required to hit:** {to_hit_chart}")

col1, col2 = st.columns(2)

with col1:
# Use Streamlit columns to make the buttons less wide

    # User input for number of attacks
    number_of_attacks = st.number_input("Number of Attacks", min_value=1, max_value=20, value=10, step=1)

if run_simulation:
    # Show number of runs input if simulation is enabled
    number_of_runs = st.number_input("Number of Runs", min_value=1, max_value=10000, value=200, step=1)

    if st.button("Simulate Combat"):
        import matplotlib.pyplot as plt
        import numpy as np

        # Run the simulation
        results = []
        for _ in range(number_of_runs):
            num_hits, _ = multiple_hits(attackers_weapon_skill, defenders_weapon_skill, number_of_attacks)
            results.append(num_hits)

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

        else:

            # Plot the bell curve graph
            fig, ax = plt.subplots()
            counts, bins, patches = ax.hist(results, bins=20, color='blue', alpha=0.7, edgecolor='black')
            total = sum(counts)
            for count, patch in zip(counts, patches):
                percentage = (count / total) * 100
                if percentage > 10:
                    ax.text(patch.get_x() + patch.get_width() / 2, count, f'{percentage:.1f}%',
                            ha='center', va='bottom', fontsize=10, color='black')
            ax.set_title("Simulation Results: Number of Hits")
            ax.set_xlabel("Number of Hits")
            ax.set_ylabel("Frequency")

            st.pyplot(fig)
else:
    # Combine the two buttons into one
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