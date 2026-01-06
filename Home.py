import streamlit as st
from pathlib import Path
import pandas as pd
from utils.big_data import get_big_data, big_metrics, big_rankings
from utils.visuals import big_radar_plot, big_tempo_duration, big_trope_heatmap
from utils.components import pill_button_styler, background_band_fill_side

st.set_page_config(page_title="B1G Fight Songs", 
                   layout="wide")

# full dataframe
df = get_big_data()

# title
st.markdown("<h1 style='text-align:center;'>Sounds of the Big Ten Conference</h1>", unsafe_allow_html=True)
# caption
st.markdown("<h4 style='text-align:center;'>An interactive analysis of Big Ten fight songs</h3>", unsafe_allow_html=True)
# author
st.markdown("<h5 style='text-align:center;'>By Colin Bertrand</h3>", unsafe_allow_html=True)


"---"

# school logos
folder_path = Path("data/logos/resized") 
image_files = sorted([
    p for p in folder_path.iterdir() if p.is_file()
])
cols = st.columns(len(image_files))
for col, image_path in zip(cols, image_files):
    with col:
        st.image(image_path, width="stretch")

"---"
# overview section
st.header("Overview")
col_para, col_logo = st.columns([2.5, 1])
with col_para:
    st.markdown("""
                Fight songs play a big role in defining the identity and spirit of a university. 
                The 18 schools in the Big Ten each have a fight song whcih reflect their tradition and compeition. 
                Using data from FiveThirtyEight and Spotify Audio features, this dashboard analyzes
                how tempo, duration, and lyrical tropes vary across the conference. 
                
                - **Tropes** are a repeated motif 
                that are found within a fight song. For example, the *fight* trope column represents whether the 
                word 'fight' shows up in a fight song. 

                - **BPM** represents *beats per minute*.

                The features below explore the Big Ten conference through summary statistics, trope identities, sound profiles, and metric rankings. 


                """)
with col_logo:
    # B1G Logo
    nan1, pic, nan2 = st.columns([1, 4, 1])
    with pic:
        st.image("data/logos/Big_Ten_Conference_logo.svg.png", width="stretch")

"---"
# summary metrics
st.header('Summary Metrics')
big_metrics(df)
'---'
# tempo vs duration scatterplot
big_tempo_duration(df)
st.caption("A scatterplot representing Big Ten average tempo and duration of fight songs. The further right the values, "
           "the longer the song. The higher up the value, the faster the song.")
'---'
# average trope usage big ten radar plot
big_radar_plot(df)
st.caption("A radar plot displaying the Big Ten average use of common fight song tropes. Values represent normalized word frequencies")
# trope presence in the big ten heatmap
big_trope_heatmap(df)
st.caption(
        "A heatmap to further help display the use of tropes in a fight song. " 
        "Each cell represents the frequency or normalized presence of a lyrical trope "
        "within a school’s fight song. Blue indicate trope presence."
    )
'---'

# big ten ranking section
st.header("Big Ten Rankings and Extremes")
# metrics
big_rankings(df)
st.caption(
    "*Traditional* and *Unique* rankings are found by computing the difference between a school's " 
    "trope values and the average trope values of the Big Ten. Traditional is the closest to the average, "
    "while Unique is the furthest from the average."
)
'---'

 # buttons to other pages
st.header("Explore More Pages")
st.markdown("""
    This dashboard contains several pages that delve deeper into the analysis of Big Ten fight songs. 
    Each page offers unique insights and visualizations.

    - **School Profiles**: Detailed profiles of each Big Ten school, showcasing their fight song history and unique characteristics.
    - **Battle of the Bands**: A comparative battle of two fight songs across different Big Ten schools, allowing users to visualize and contrast various metrics such as tempo, duration, and lyrical tropes. This page will enable users to identify trends and differences in fight song characteristics among the schools.
    - **Data Dictionary**: An explanation of the data sources and metrics used in the analysis, providing clarity on what the data referes to.
    - **Methodology**: A breakdown of the collection, analytical methods, and visualizations employed to interpret the fight songs and their features.

    Navigate through the sidebar or buttons below to access these additional pages and enhance your understanding of the fight songs that represent the spirit of the Big Ten!
""")

pill_button_styler("#0085CE", "#B3B3B3", "#000000")
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("School Profiles", width="stretch"):
        st.switch_page("pages/2_School_Profiles.py")

with col2:
    if st.button("Battle of the Bands", width="stretch"):
        st.switch_page("pages/3_Battle_of_the_Bands.py")

with col3:
    if st.button("Data Dictionary", width="stretch"):
        st.switch_page("pages/4_Data_Dictionary.py")
with col4:
    if st.button("Methodology", width="stretch"):
        st.switch_page("pages/5_Methodology.py")


# sidebar 
st.sidebar.header("Big Ten Fight Songs")
st.sidebar.caption("Analysis by *Colin Bertrand*")
st.sidebar.markdown('---')
st.sidebar.subheader("About This Page")
st.sidebar.markdown("""
This interactive dashboard analyzes the fight songs of Big Ten Conference schools using audio features and lyrical analysis.

**Features included:**
- Summary metrics and statistics
- Tempo and duration analysis
- Common trope identification
- School rankings by traditionality and uniqueness
""")

st.sidebar.markdown(background_band_fill_side(
    subtitle="Navigate between pages using the buttons at the bottom of the page or the sidebar navigation.",
        secondary_color="#B3B3B3",
        text_color="#000000",
        border=True,
        border_color="#0085CE"), unsafe_allow_html=True)