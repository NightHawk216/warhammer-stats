import streamlit as st

CHANGELOG_LINES_TO_SKIP = 6  # header lines
DISPLAY_LATEST = 0  # number or latest versions to display


def show_changelog():
    # suppose that ChangeLog.md is located at the same folder as Streamlit app
    with open('../CHANGELOG.md', 'r', encoding='utf-8') as f:
        lines = f.readlines()[CHANGELOG_LINES_TO_SKIP:]

    # lines which contain version numbers only
    version_numbers = [line for line in lines if line.startswith('## [')]
    
    # number of line, which separates displayed entries from hidden ones
    version_idx = lines.index(version_numbers[DISPLAY_LATEST])
    
    # display entries
    st.header('Release Notes')
    st.markdown(''.join(lines[:version_idx]))
    
    # hide others with expander
    st.markdown(''.join(lines[version_idx:]))


show_changelog()