import streamlit as st
from pathlib import Path
import pandas as pd
from utils.big_data import big_data, big_metrics, big_rankings
from utils.visuals import big_radar_plot, big_tempo_duration, big_trope_heatmap

st.set_page_config(page_title="B1G Fight Songs", 
                   layout="wide")
st.sidebar.header("Big Ten Fight Songs")
st.sidebar.caption("Analysis by *Colin Bertrand*")
df = big_data()

# title
st.markdown("<h1 style='text-align:center;'>Sounds of the B1G Conference</h1>", unsafe_allow_html=True)
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
        st.image(image_path, use_container_width=True)

"---"

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
        st.image("data/logos/Big_Ten_Conference_logo.svg.png", use_container_width=True)

"---"

st.header('Summary Metrics')
big_metrics(df)
'---'
big_tempo_duration(df)
st.caption("A scatterplot representing Big Ten average tempo and duration of fight songs. The further right the values, "
           "the longer the song. The higher up the value, the faster the song.")
'---'
big_radar_plot(df)
st.caption("A radar plot displaying the Big Ten average use of common fight song tropes. Values represent normalized word frequencies")

big_trope_heatmap(df)
st.caption(
        "A heatmap to further help display the use of tropes in a fight song. " 
        "Each cell represents the frequency or normalized presence of a lyrical trope "
        "within a school’s fight song. Blue indicate trope presence."
    )
'---'

st.header("Big Ten Rankings and Extremes")
big_rankings(df)
st.caption(
    "*Traditional* and *Unique* rankings are found by computing the difference between a school's " 
    "trope values and the average trope values of the Big Ten. Traditional is the closest to the average, "
    "while Unique is the furthest from the average."
)
'---'