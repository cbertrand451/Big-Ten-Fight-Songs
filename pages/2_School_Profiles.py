import streamlit as st
from utils.big_data import get_big_data
from utils.colors import get_school_colors
st.set_page_config(page_title="B1G School Profiles", 
                   layout="wide")

st.title("School Profiles")

# retrieve data
df = get_big_data()
# school list
schools = df['school'].unique().tolist()
col, nan = st.columns([3, 7])
with col:
    # select a school
    school = st.selectbox("Select a School", options=schools)
'---'
# school info
row = df[df['school'] == school]
colors = get_school_colors(school)
# set main color
PRIMARY = colors["primary"]
# set secondary color
SECONDARY = colors["secondary"]
# school profile title
st.markdown(
    f"""
    <h2>
        <span style="color:{PRIMARY};">{school}</span> Profile
    </h2>
    """,
    unsafe_allow_html=True
)