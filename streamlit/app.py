import streamlit as st

pages = {
    "warhammer-tow-roll-simulator": [
        st.Page("main.py", title="Main"),
        # st.Page("page_2.py", title="ChangeLog"),
    ],
    # "Resources": [
    #     st.Page("learn.py", title="Learn about us"),
    #     st.Page("trial.py", title="Try it out"),
    # ],
}

pg = st.navigation(pages)
pg.run()