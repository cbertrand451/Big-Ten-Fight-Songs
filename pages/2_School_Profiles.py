import streamlit as st
from utils.big_data import get_big_data, summary_stats, up_or_down
from utils.colors import get_school_colors, load_json
from utils.components import colored_metric, colored_text, divider, background_band_fill, background_band_fill_side, text_to_paragraphs, tab_styler, pill_button_styler
from utils.visuals import school_radar_plot, big_ten_rank_bars
st.set_page_config(page_title="B1G School Profiles", 
                   layout="wide")

# title section
st.markdown("<h1 style='text-align:center;'>School Profiles</h1>", unsafe_allow_html=True)

st.markdown("<h4 style='text-align:center;'>A detailed look at each Big Ten fight song</h3>", unsafe_allow_html=True)


# retrieve data
df = get_big_data()
# school list
schools = df['school'].unique().tolist()

# persist selection across page visits
if "school_profile_selection" not in st.session_state:
    st.session_state.school_profile_selection = schools[0]

col, nan = st.columns([3, 7])
with col:
    # select a school
    default_idx = schools.index(st.session_state.school_profile_selection) if st.session_state.school_profile_selection in schools else 0
    school = st.selectbox("Select a School", options=schools, index=default_idx, key="school_profile")
    st.session_state.school_profile_selection = school
# school info
row = df.loc[df['school'] == school].iloc[0]
colors = get_school_colors(school)

# set colors
PRIMARY = colors["primary"]
SECONDARY = colors["secondary"]
SECTEXT = colors["secondary_text"]

# school profile title
qs = '"'
col_text, col_pic = st.columns([2.5, 1])
with col_text:
    divider(color=SECONDARY)
    # summary song info
    colored_text(f"{qs}{row['song_name']}{qs}", size="h2", color=PRIMARY, weight="bold")
    st.markdown(f"**Writers**: {row['writers']}")
    st.markdown(f"**Year Written**: {row['year']}")
    st.markdown(f"**Writer School Status**: {'Student Writer' if row['student_writer'] == 1 else 'Non-Student Writer'}")
    st.markdown(f"**Song Status**: {'Official School Song' if row['official_song'] == 1 else 'Unofficial School Song'}")
    st.markdown(f"**Contest Chosen**: {'Yes' if row['contest'] == 1 else 'No'}")
    divider(color=SECONDARY)
with col_pic:
    st.image(f"data/logos/resized/{school}.png", width="stretch")

# Summary Metrics
st.header("**Summary Metrics**")

t1, t2, t3, t4, t5, t6 = summary_stats(df)
c1, c2, c3, c4, c5 = st.columns(5)
with c1:
    # Tempo
    arr = up_or_down(row['bpm'], t1)
    m1 = colored_metric(
        label="Tempo (BPM)",
        value=round(row['bpm'], 2),
        val_color=PRIMARY,
        delta=f"{arr} {abs(round(row['bpm'] - t1, 2))} BPM",
        delta_b_color=SECONDARY,
        delta_t_color=SECTEXT
    )
    st.markdown(m1, unsafe_allow_html=True)
with c2:
    # Duration
    arr = up_or_down(row['sec_duration'], t2)
    m2 = colored_metric(
        label="Duration (seconds)",
        value=round(row['sec_duration'], 2),
        val_color=PRIMARY,
        delta=f"{arr} {abs(round(row['sec_duration'] - t2))}s",
        delta_b_color=SECONDARY,
        delta_t_color=SECTEXT
    )
    st.markdown(m2, unsafe_allow_html=True)
with c3:
    # Trope Count
    arr = up_or_down(row['trope_count'], t3)
    m3 = colored_metric(
        label="Trope Count",
        value=round(row['trope_count'], 2),
        val_color=PRIMARY,
        delta=f"{arr} {abs(round(row['trope_count'] - t3, 2))}",
        delta_b_color=SECONDARY,
        delta_t_color=SECTEXT
    )
    st.markdown(m3, unsafe_allow_html=True)
with c4:
    # fight numbers
    arr = up_or_down(row['number_fights'], df['number_fights'].mean())
    m4 = colored_metric(
        label='Number of "Fights"',
        value=int(row['number_fights']),
        val_color=PRIMARY,
        delta=f"{arr} {abs(round(row['number_fights'] - df['number_fights'].mean(), 2))} Fights",
        delta_b_color=SECONDARY,
        delta_t_color=SECTEXT
    )
    st.markdown(m4, unsafe_allow_html=True)
with c5:
    # Year Written
    arr = up_or_down(row['year'], df['year'].mean())
    m5 = colored_metric(
        label="Year Written",
        value=int(row['year']),
        val_color=PRIMARY,
        delta=f"{arr} {abs(int(row['year'] - df['year'].mean()))} Years",
        delta_b_color=SECONDARY,
        delta_t_color=SECTEXT
    )
    st.markdown(m5, unsafe_allow_html=True)
st.caption("Arrows indicate difference between school and Big Ten **average values**. Year written is compared to average Big Ten year written.")

divider(color=SECONDARY)

# Trope Radar Plot
col_radar, col_text = st.columns([2, 1])
with col_radar:
    school_radar_plot(df, school, school_color=PRIMARY)
with col_text:
    st.header("**Trope Metrics**")
    divider(PRIMARY)
    col_school, mid, col_big = st.columns([1, 2, 1])
    with col_school:
        m1 = colored_metric(
            label="Trope Count",
            value=int(row['trope_count']),
            val_color=PRIMARY
        )
        st.markdown(m1, unsafe_allow_html=True)
        m2 = colored_metric(
            label="Fight Count",
            value=int(row['number_fights']),
            val_color=PRIMARY
        )
        st.markdown(m2, unsafe_allow_html=True)
    with col_big:
        m1 = colored_metric(
            label="B1G Average",
            value=round(df['trope_count'].mean(), 2),
            val_color="rgb(150, 150, 150)"
        )
        st.markdown(m1, unsafe_allow_html=True)
        m2 = colored_metric(
            label="B1G Average",
            value=round(df['number_fights'].mean(), 2),
            val_color="rgb(150, 150, 150)"
        )
        st.markdown(m2, unsafe_allow_html=True)
    with mid:
        trope_delta = round(((row['trope_count'] - df['trope_count'].mean()) / df['trope_count'].mean())*100, 2)
        arr = up_or_down(row['trope_count'], df['trope_count'].mean())
        m1 = f"""
            <div style="
            font-size: 36px; 
            font-weight: 500; 
            color: #000000;
            line-height: normal;
            padding-bottom: 0.25rem;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            width: 100%;">
            {arr} {trope_delta}%
        </div>
        <div style="
            display: inline-block;
            background-color: {SECONDARY};
            color: {SECTEXT};
            padding: 4px 8px;
            border-radius: 20px;
            font-family: 'Source Sans Pro', sans-serif;
            font-size: 14px;
            font-weight: 600;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        ">
        from B1G Avg
        </div>
        """ 
        st.markdown(m1, unsafe_allow_html=True)
        fight_delta = round(((row['number_fights'] - df['number_fights'].mean()) / df['number_fights'].mean())*100, 2)
        arr1 = up_or_down(row['number_fights'], df['number_fights'].mean())
        m2 = f"""
            <div style="
            font-size: 36px; 
            font-weight: 500; 
            color: #000000;
            line-height: normal;
            padding-bottom: 0.25rem;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            width: 100%;">
            {arr1} {fight_delta}%
        </div>
        <div style="
            display: inline-block;
            background-color: {SECONDARY};
            color: {SECTEXT};
            padding: 4px 8px;
            border-radius: 20px;
            font-family: 'Source Sans Pro', sans-serif;
            font-size: 14px;
            font-weight: 600;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        ">
        from B1G Avg
        </div>
        """ 
        st.markdown(m2, unsafe_allow_html=True)
    divider(PRIMARY)

st.caption(f"This radar plot shows the presence of tropes in the **{school}** fight song. The grey plot represents the Big Ten Average use of each trope.")
divider(color=SECONDARY)

# Big Ten Rankings Plots
st.header("Big Ten Rankings")
tab_styler(PRIMARY, SECONDARY, SECTEXT)
tabs = st.tabs(["**Tempo**", "**Duration**", "**Year**", "**Tropes**"])
col_metric, col_graph =st.columns([0.5, 10])

with tabs[0]:
    rank_choice = "Tempo Rank"
    fig = big_ten_rank_bars(
        df, school, rank_choice, PRIMARY, SECONDARY
    )
    st.plotly_chart(fig, width="stretch")
with tabs[1]:
    rank_choice = "Duration Rank"
    fig = big_ten_rank_bars(
        df, school, rank_choice, PRIMARY, SECONDARY
    )
    st.plotly_chart(fig, width="stretch")
with tabs[2]:
    rank_choice = "Year Written Rank"
    fig = big_ten_rank_bars(
        df, school, rank_choice, PRIMARY, SECONDARY
    )
    st.plotly_chart(fig, width="stretch")
with tabs[3]:
    rank_choice = "Trope Density Rank"
    fig = big_ten_rank_bars(
        df, school, rank_choice, PRIMARY, SECONDARY
    )
    st.plotly_chart(fig, width="stretch")

st.caption(f"""These plots show the ranking of the **{school}** fight song amongst the other Big Ten schools. 
           It compares the features of *Tempo*, *Duration*, *Year Written*, and *Trope Counts*. 
           The {school} value is highlighted in the school color. The Big Ten average is shown as a dashed line.
           The specific ranking of **{row['song_name']}** is shown highlighted at the top.""")
divider(SECONDARY)

# Video Preview
st.header("**Preview**")

col_vid, col_text = st.columns([2, 1])
with col_vid:
    yt_url = load_json("data/videos/yt_vids.json").get(school)
    st.video(yt_url)
with col_text:
    description = text_to_paragraphs(f"""
        Watch a preview of {school}'s fight song, sourced from YouTube!

        Content may not match summary statistics exactly due to different recordings.

        Video is for audio purposes only, does not contribute to analysis.
        """, color=SECTEXT)
    
    background_band_fill(
        subtitle=description,
        secondary_color=SECONDARY,
        text_color=SECTEXT,
        border=True,
        border_color=PRIMARY
    )

    colored_text("Video Source:", size="h4", color=PRIMARY, weight="bold")
    st.markdown(f'<a href="https://www.youtube.com/playlist?list=PLdEih-bqJyY2y4tF9434Rlhx4fcvwageX" style="color:black;">Big Ten Fight Songs Playlist</a>', unsafe_allow_html=True)
    st.markdown(f'<a href="{yt_url}" style="color:black;">{row["song_name"]} - Song</a>', unsafe_allow_html=True)
    colored_text("Spotify Link:", size="h4", color=PRIMARY, weight="bold")
    st.markdown(f'<a href="https://open.spotify.com/track/{row["spotify_id"]}" style="color:black;">{row["song_name"]} - Spotify</a>', unsafe_allow_html=True)

#st.caption("Links are provided in the event the media player is not correctly displaying a perview video.")
divider(color=SECONDARY)



# buttons for other pages
pill_button_styler(PRIMARY, SECONDARY, SECTEXT)
st.header("Navigate to Pages")
st.markdown("""Navigate through the sidebar or buttons below to access these additional pages 
            and enhance your understanding of the fight songs that represent the spirit of the Big Ten!""")
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("Home", width="stretch"):
        st.switch_page("Home.py")

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
st.sidebar.markdown(
    f"""
    <h2>
        <span style="color:{PRIMARY};">{school}</span> Fight Song Profile
    </h2>
    """,
    unsafe_allow_html=True
)
st.sidebar.caption("Analysis by *Colin Bertrand*")

# st.sidebar.image(f"data/logos/resized/{school}.png", width=100)
st.sidebar.markdown("---")
st.sidebar.subheader("About This Page")
st.sidebar.markdown(
    f"""
    <p>
        Explore detailed statistics and rankings for
        <span style="color:{PRIMARY}; font-weight:600;">{row['song_name']}</span>
    </p>

    <p><b>Key Metrics:</b></p>
    <ul>
        <li>Tempo, duration, and trope analysis</li>
        <li>Big Ten rankings across multiple categories</li>
        <li>Audio preview from official sources</li>
    </ul>

    <p>Use the dropdown at the top to select a school.</p>
    """,
    unsafe_allow_html=True
)


st.sidebar.markdown(background_band_fill_side(
    subtitle="Navigate between pages using the buttons at the bottom of the page or the sidebar navigation.",
        secondary_color=SECONDARY,
        text_color=SECTEXT,
        border=True,
        border_color=PRIMARY), unsafe_allow_html=True)
