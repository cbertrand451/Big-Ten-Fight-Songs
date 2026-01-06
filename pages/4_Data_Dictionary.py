import streamlit as st
import pandas as pd
from utils.components import styled_section_df, pill_button_styler, background_band_fill_side

st.set_page_config(page_title="Data Dictionary", 
                   layout="wide")

# title + caption
st.markdown("<h1 style='text-align:center;'>Data Dictionary</h1>", unsafe_allow_html=True)

st.markdown("<h4 style='text-align:center;'>A thorough explanation of the variables used in this dashboard</h3>", unsafe_allow_html=True)

'---'
# define data categories and their values in the datafram
core_metadata = [
    {"Variable": "school", "Description": "University or college name", "Type": "string", "Source": "Original Data"},
    {"Variable": "conference", "Description": "Conference affiliation (e.g., Big Ten)", "Type": "string", "Source": "Original Data"},
    {"Variable": "song_name", "Description": "Fight song title", "Type": "string", "Source": "Original Data"},
    {"Variable": "writers", "Description": "Composer / lyricist names", "Type": "string", "Source": "Original Data"},
    {"Variable": "year", "Description": "Year the fight song was written", "Type": "integer", "Source": "Original Data"},
    {"Variable": "student_writer", "Description": "1 if writer was a student; 0 otherwise", "Type": "binary", "Source": "Original Data"},
    {"Variable": "official_song", "Description": "1 if officially designated as the school song; 0 otherwise", "Type": "binary", "Source": "Original Data"},
    {"Variable": "contest", "Description": "1 if selected via contest; 0 otherwise", "Type": "binary", "Source": "Original Data"},
]

audio_metrics = [
    {"Variable": "bpm", "Description": "Tempo of the song in beats per minute", "Type": "float", "Source": "Original Data"},
    {"Variable": "sec_duration", "Description": "Song length in seconds", "Type": "float", "Source": "Original Data"},
]

lyrical_tropes = [
    {"Variable": "fight", "Description": "Song contains the word 'fight'", "Type": "binary", "Source": "Original Data"},
    {"Variable": "number_fights", "Description": "Count of 'fight' occurrences", "Type": "integer", "Source": "Original Data"},
    {"Variable": "victory", "Description": "Mentions of victory language", "Type": "binary", "Source": "Original Data"},
    {"Variable": "win_won", "Description": "Mentions of win/won phrasing", "Type": "binary", "Source": "Original Data"},
    {"Variable": "rah", "Description": "Includes 'rah' chant", "Type": "binary", "Source": "Original Data"},
    {"Variable": "nonsense", "Description": "Contains non-lexical/cheer syllables", "Type": "binary", "Source": "Original Data"},
    {"Variable": "colors", "Description": "Calls out school colors", "Type": "binary", "Source": "Original Data"},
    {"Variable": "men", "Description": "References to 'men'", "Type": "binary", "Source": "Original Data"},
    {"Variable": "opponents", "Description": "Mentions opponents/foes", "Type": "binary", "Source": "Original Data"},
    {"Variable": "spelling", "Description": "Spells school name/initials", "Type": "binary", "Source": "Original Data"},
    {"Variable": "victory_win_won", "Description": "Combined flag for victory or win/won phrasing", "Type": "binary", "Source": "Original Data"},
    {"Variable": "trope_count", "Description": "Sum of all trope flags present in lyrics", "Type": "integer", "Source": "Original Data"},
]

misc_variables = [
    {"Variable": "spotify_id", "Description": "Spotify track identifier for the song", "Type": "string", "Source": "Original Data"},
]

computed_metrics = [
    {"Variable": "Tempo Rank", "Description": "Rank of a song's BPM relative to Big Ten peers", "Type": "integer", "Source": "Computed in-app"},
    {"Variable": "Duration Rank", "Description": "Rank of song length relative to Big Ten peers", "Type": "integer", "Source": "Computed in-app"},
    {"Variable": "Year Written Rank", "Description": "Rank of composition year (older vs newer)", "Type": "integer", "Source": "Computed in-app"},
    {"Variable": "Trope Density Rank", "Description": "Rank of trope_count relative to conference", "Type": "integer", "Source": "Computed in-app"},
    {"Variable": "Battle deltas", "Description": "Head-to-head differences in tempo, duration, year, tropes", "Type": "string", "Source": "Computed in-app"},
    {"Variable": "Radar normalization", "Description": "Scaled trope values for radar plots", "Type": "float", "Source": "Computed in-app"},
]

external_metadata = [
    {"Variable": "primary_color", "Description": "School's primary brand color", "Type": "string (hex/RGB)", "Source": "Online School Sources"},
    {"Variable": "secondary_color", "Description": "School's secondary brand color", "Type": "string (hex/RGB)", "Source": "Online School Sources"},
    {"Variable": "secondary_text_color", "Description": "Text color to pair with secondary background", "Type": "string (hex/RGB)", "Source": "Manual Entry"},
    {"Variable": "logo", "Description": "Resized logo used for displays", "Type": "image", "Source": "Manual Entry"},
    {"Variable": "yt_url", "Description": "YouTube preview link per school", "Type": "URL", "Source": "YouTube"},
]

# color pallette (bg is unfazed)
palette = {
    "header_bg": "#0B3C5D",
    "header_text": "#FFFFFF",
    "name_color": "#0085CE",
}

# show all the dataframes
st.header("Core Metadata")
st.dataframe(
    styled_section_df(core_metadata, **palette),
    hide_index=True,
    width="stretch",
)

st.header("Audio Metrics")
st.dataframe(
    styled_section_df(audio_metrics, **palette),
    hide_index=True,
    width="stretch",
)

st.header("Lyrical / Trope Features")
st.dataframe(
    styled_section_df(lyrical_tropes, **palette),
    hide_index=True,
    width="stretch",
)

st.header("Miscellaneous Variables")
st.dataframe(
    styled_section_df(misc_variables, **palette),
    hide_index=True,
    width="stretch",
)

st.header("Computed Metrics (not stored)")
st.dataframe(
    styled_section_df(computed_metrics, **palette),
    hide_index=True,
    width="stretch",
)

st.header("External Metadata (colors, images)")
st.dataframe(
    styled_section_df(external_metadata, **palette),
    hide_index=True,
    width="stretch",
)

'---'

# explore other pages
st.header("Explore the Data")
st.subheader("Big Ten Dataset (cleaned)")
big_ten_df = pd.read_csv("data/B1G/big_ten_fight_songs.csv")
st.dataframe(big_ten_df, width="stretch")

st.subheader("Raw Dataset (original)")
raw_df = pd.read_csv("data/raw/fight-songs-updated.csv")
st.dataframe(raw_df, width="stretch")
st.caption("Tip: click column headers to sort or use the search box to filter rows.")

'---'

st.header("Explore More Pages")
st.markdown("""Navigate through the sidebar or buttons below to access these additional pages 
            and enhance your understanding of the fight songs that represent the spirit of the Big Ten!""")
pill_button_styler("#0085CE", "#B3B3B3", "#000000")
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("Home", width="stretch"):
        st.switch_page("Home.py")

with col2:
    if st.button("School Profiles", width="stretch"):
        st.switch_page("pages/2_School_Profiles.py")

with col3:
    if st.button("Battle of the Bands", width="stretch"):
        st.switch_page("pages/3_Battle_of_the_Bands.py")

with col4:
    if st.button("Methodology", width="stretch"):
        st.switch_page("pages/5_Methodology.py")


# sidebar
st.sidebar.header("Fight Song Data Dcitionary")
st.sidebar.caption("Explanation by *Colin Bertrand*")
st.sidebar.markdown('---')
st.sidebar.subheader("About This Page")
st.sidebar.markdown("""
This page gives an explanation for each variable used throughout the project. 
                    It provides *variable name*, *description*, *data type*, and *source*.
                    The variables are also sorted into the following categories:
""")

st.sidebar.markdown("""
        - **Core Metadata**
        - **Audio Metrics**
        - **Lyrical Tropes**
        - **Miscellaneous Variables**
        - **Computed Metrics**
        - **Extrenal Metadata**
            """)

st.sidebar.markdown("The Big Ten dataset and raw fight song dataset are available for exploration at the bottom of the page.")

st.sidebar.markdown(background_band_fill_side(
    subtitle="Navigate between pages using the buttons at the bottom of the page or the sidebar navigation.",
        secondary_color="#B3B3B3",
        text_color="#000000",
        border=True,
        border_color="#0085CE"), unsafe_allow_html=True)
