import streamlit as st
from utils.big_data import get_big_data, up_or_down
from utils.colors import get_school_colors
from utils.components import colored_metric, divider, background_band_fill_side, tab_styler, pill_button_styler
from utils.visuals import dual_school_radar_plot, big_ten_rank_bars_dual, big_tempo_duration_dual

st.set_page_config(page_title="Battle of the Bands", 
                   layout="wide")
# title + caption
st.markdown("<h1 style='text-align:center;'>Battle of the Bands</h1>", unsafe_allow_html=True)

st.markdown("<h4 style='text-align:center;'>A comparative analysis between Big Ten Fight Songs</h3>", unsafe_allow_html=True)

# retrieve data
df = get_big_data()

# get unique school list
schools = sorted(df['school'].unique().tolist())

# persist selections across visits
if "battle_selection" not in st.session_state:
    st.session_state.battle_selection = {"school1": None, "school2": None}

# side-by-side columns to select schools and defaulting to any saved picks
c1, nan, c3 = st.columns([3, 4, 3])
with c1:
    default_left = st.session_state.battle_selection.get("school1")
    school1 = st.selectbox(
        "Select School",
        options=schools,
        index=schools.index(default_left) if default_left in schools else None,
        key="school_left"
    )

with c3:
    default_right = st.session_state.battle_selection.get("school2")
    school2 = st.selectbox(
        "Select School",
        options=schools,
        index=schools.index(default_right) if default_right in schools else None,
        key="school_right"
    )

# update stored selections for future visits
st.session_state.battle_selection["school1"] = school1
st.session_state.battle_selection["school2"] = school2
if (school1 is None and school2 is None):
    with nan:
        st.markdown("")
        st.markdown("<h3 style='text-align:center;'>← Select Schools →</h3>", unsafe_allow_html=True)
        st.sidebar.header('Select Schools!')
        st.stop()
elif school1 == school2:
    with nan: 
        st.info("Cannot select the same school!")
    st.stop()
elif school1 is None:
    st.sidebar.header('Select First School!')
    with nan:
        a, col2, d = st.columns([7.5, 2.5, 1])
        with col2:
            st.image(f"data/logos/resized/{school2}.png", width="stretch")
        with a:
            st.markdown("")
            st.markdown("<h3 style='text-align:center;'>← Select School</h3>", unsafe_allow_html=True)
            st.stop()
elif school2 is None:
    st.sidebar.header('Select Second School!')
    with nan:
        a, col1, d  = st.columns([1, 2.5, 7.5])
        with col1:
            st.image(f"data/logos/resized/{school1}.png", width="stretch")
        with d:
            st.markdown("")
            st.markdown("<h3 style='text-align:center;'>Select School →</h3>", unsafe_allow_html=True)
            st.stop()
else:
    with nan:
        a, col1, b, vs, c, col2, d = st.columns([1, 2.5, 1, 2, 1, 2.5, 1])
        with col1:
            st.image(f"data/logos/resized/{school1}.png", width="stretch")
        with vs:
            #st.markdown("")
            st.markdown("<h1 style='text-align:center;'>VS</h1>", unsafe_allow_html=True)
        with col2:
            st.image(f"data/logos/resized/{school2}.png", width="stretch")

# create session states
if "battle_mode" not in st.session_state:
    st.sidebar.header('Time to Battle!')
    st.session_state.battle_mode = False
# reset battle when selections change
if "prev_s1" not in st.session_state:
    st.session_state.prev_s1 = school1
if "prev_s2" not in st.session_state:
    st.session_state.prev_s2 = school2
if (school1 != st.session_state.prev_s1) or (school2 != st.session_state.prev_s2):
    st.session_state.battle_mode = False
# set previously selected schools
st.session_state.prev_s1 = school1
st.session_state.prev_s2 = school2
# battle button
valid_selection = school1 != school2 and school1 is not None and school2 is not None
a, col, b = st.columns([3, 4, 3])
pill_button_styler("#0085CE", "#B3B3B3", "#000000")
if valid_selection and not st.session_state.battle_mode:
    with col:
        if st.button("Battle!", width="stretch"):
            st.session_state.battle_mode = True
            st.rerun()

if not st.session_state.battle_mode:
    st.stop()
'---'

# set colors1
colors1 = get_school_colors(school1)
PRIMARY1 = colors1["primary"]
SECONDARY1 = colors1["secondary"]
SECTEXT1 = colors1["secondary_text"]

# set colors2
colors2 = get_school_colors(school2)
PRIMARY2 = colors2["primary"]
SECONDARY2 = colors2["secondary"]
SECTEXT2 = colors2["secondary_text"]

# create schools info
row1 = df.loc[df['school'] == school1].iloc[0]
row2 = df.loc[df['school'] == school2].iloc[0]

# song titles + school song info
qs = '"'
col1, col2 = st.columns(2)
with col1:
    st.markdown(f"<h2 style='text-align:left;color:{PRIMARY1}'>{qs}{row1['song_name']}{qs}</h2>", unsafe_allow_html=True)
    # writers
    st.markdown(
        f"""
            <div style="font-size: 1rem;text-align:left">
                <span style="font-weight: 700;">Writers</span>
                <span style="font-weight: 400;">: {row1['writers']}</span>
            </div>
            """,
            unsafe_allow_html=True
    )
    # Writer Shool Status
    st.markdown(
        f"""
            <div style="font-size: 1rem;text-align:left">
                <span style="font-weight: 700;">Writer School Status</span>
                <span style="font-weight: 400;">: {'Student Writer' if row1['student_writer'] == 1 else 'Non-Student Writer'}</span>
            </div>
            """,
            unsafe_allow_html=True
    )
    # Song Status
    st.markdown(
        f"""
            <div style="font-size: 1rem;text-align:left">
                <span style="font-weight: 700;">Song Status</span>
                <span style="font-weight: 400;">: {'Official School Song' if row1['official_song'] == 1 else 'Unofficial School Song'}</span>
            </div>
            """,
            unsafe_allow_html=True
    )
    # Contest Chosen
    st.markdown(
        f"""
            <div style="font-size: 1rem;text-align:left">
                <span style="font-weight: 700;">Song Status</span>
                <span style="font-weight: 400;">: {'Yes' if row1['contest'] == 1 else 'No'}</span>
            </div>
            """,
            unsafe_allow_html=True
    )
with col2:
    st.markdown(f"<h2 style='text-align:right;color:{PRIMARY2}'>{qs}{row2['song_name']}{qs}</h2>", unsafe_allow_html=True)
    # writers
    st.markdown(
        f"""
            <div style="font-size: 1rem;text-align:right">
                <span style="font-weight: 700;">Writers</span>
                <span style="font-weight: 400;">: {row2['writers']}</span>
            </div>
            """,
            unsafe_allow_html=True
    )
    # Writer Shool Status
    st.markdown(
        f"""
            <div style="font-size: 1rem;text-align:right">
                <span style="font-weight: 700;">Writer School Status</span>
                <span style="font-weight: 400;">: {'Student Writer' if row1['student_writer'] == 1 else 'Non-Student Writer'}</span>
            </div>
            """,
            unsafe_allow_html=True
    )
    # Song Status
    st.markdown(
        f"""
            <div style="font-size: 1rem;text-align:right">
                <span style="font-weight: 700;">Song Status</span>
                <span style="font-weight: 400;">: {'Official School Song' if row1['official_song'] == 1 else 'Unofficial School Song'}</span>
            </div>
            """,
            unsafe_allow_html=True
    )
    # Contest Chosen
    st.markdown(
        f"""
            <div style="font-size: 1rem;text-align:right">
                <span style="font-weight: 700;">Song Status</span>
                <span style="font-weight: 400;">: {'Yes' if row1['contest'] == 1 else 'No'}</span>
            </div>
            """,
            unsafe_allow_html=True
    )

# dividers
a, mid, b = st.columns([4, 4, 4])
with a:
    divider(PRIMARY1)
with b:
    divider(PRIMARY2)

# battling metrics
right_b, met1, arrow, met2, left_b = st.columns([2, 2, 2, 2, 2])

with met1:
    
    # tempo
    if (row1['bpm'] > row2['bpm']):
        delta_v = f"{up_or_down(row1['bpm'], row2['bpm'])} {round(100*(row1['bpm'] - row2['bpm']) / row2['bpm'], 2)}%"
        b = SECONDARY1
        t = SECTEXT1
    elif row1['bpm'] == row2['bpm']:
        delta_v = "Tie!"
        b = SECONDARY1
        t = SECTEXT1
    else:
        delta_v = "'"
        t = "#F9F6EE"
        b = "#F9F6EE"
    color1 = (PRIMARY1 if row1['bpm'] >= row2['bpm'] else "grey")
    m1 = colored_metric(label="Tempo (BPM)", value=row1['bpm'], val_color=color1, delta=delta_v, delta_b_color=b, delta_t_color=t)
    for i in range(2):
        st.markdown("")
    st.markdown(m1, unsafe_allow_html=True)

    # duration
    if (row1['sec_duration'] > row2['sec_duration']):
        delta_v = f"{up_or_down(row1['sec_duration'], row2['sec_duration'])} {round(100*(row1['sec_duration'] - row2['sec_duration']) / row2['sec_duration'], 2)}%"
        b = SECONDARY1
        t = SECTEXT1
    elif row1['sec_duration'] == row2['sec_duration']:
        delta_v = "Tie!"
        b = SECONDARY1
        t = SECTEXT1
    else:
        delta_v = "'"
        t = "#F9F6EE"
        b = "#F9F6EE"
    color2 = (PRIMARY1 if row1['sec_duration'] >= row2['sec_duration'] else "grey")
    m2 = colored_metric(label="Duration (Seconds)", value=row1['sec_duration'], val_color=color2, delta=delta_v, delta_b_color=b, delta_t_color=t)
    for i in range(2):
        st.markdown("")
    st.markdown(m2, unsafe_allow_html=True)

    # year written
    if (row1['year'] < row2['year']):
        delta_v = f"{up_or_down(row1['year'], row2['year'])} {(row2['year'] - row1['year'])} Years"
        b = SECONDARY1
        t = SECTEXT1
    elif row1['year'] == row2['year']:
        delta_v = "Tie!"
        b = SECONDARY1
        t = SECTEXT1
    else:
        delta_v = "'"
        t = "#F9F6EE"
        b = "#F9F6EE"
    color3 = (PRIMARY1 if row1['year'] <= row2['year'] else "grey")
    m3 = colored_metric(label="Year Written", value=row1['year'], val_color=color3, delta=delta_v, delta_b_color=b, delta_t_color=t)
    for i in range(2):
        st.markdown("")
    st.markdown(m3, unsafe_allow_html=True)

    # trope count
    if (row1['trope_count'] > row2['trope_count']):
        delta_v = f"{up_or_down(row1['trope_count'], row2['trope_count'])} {(row1['trope_count'] - row2['trope_count'])} Tropes"
        b = SECONDARY1
        t = SECTEXT1
    elif row1['trope_count'] == row2['trope_count']:
        delta_v = "Tie!"
        b = SECONDARY1
        t = SECTEXT1
    else:
        delta_v = "'"
        t = "#F9F6EE"
        b = "#F9F6EE"
    color4 = (PRIMARY1 if row1['trope_count'] >= row2['trope_count'] else "grey")
    m4 = colored_metric(label="Trope Count", value=row1['trope_count'], val_color=color4, delta=delta_v, delta_b_color=b, delta_t_color=t)
    for i in range(2):
        st.markdown("")
    st.markdown(m4, unsafe_allow_html=True)
    
    # fight count
    if (row1['number_fights'] > row2['number_fights']):
        delta_v = f"{up_or_down(row1['number_fights'], row2['number_fights'])} {(row1['number_fights'] - row2['number_fights'])} Fights"
        b = SECONDARY1
        t = SECTEXT1
    elif row1['number_fights'] == row2['number_fights']:
        delta_v = "Tie!"
        b = SECONDARY1
        t = SECTEXT1
    else:
        delta_v = "'"
        t = "#F9F6EE"
        b = "#F9F6EE"
    color5 = (PRIMARY1 if row1['number_fights'] >= row2['number_fights'] else "grey")
    m5 = colored_metric(label="Fight Count", value=row1['number_fights'], val_color=color5, delta=delta_v, delta_b_color=b, delta_t_color=t)
    for i in range(2):
        st.markdown("")
    st.markdown(m5, unsafe_allow_html=True)
    

with met2:
    # tempo
    if (row1['bpm'] < row2['bpm']):
        delta_v = f"{up_or_down(row2['bpm'], row1['bpm'])} {round(100*(row2['bpm'] - row1['bpm'])/row1['bpm'], 2)}%"
        b = SECONDARY2
        t = SECTEXT2
    elif row1['bpm'] == row2['bpm']:
        delta_v = "Tie!"
        b = SECONDARY2
        t = SECTEXT2
    else:
        delta_v = "'"
        t = "#F9F6EE"
        b = "#F9F6EE"
    color = (PRIMARY2 if (row1['bpm'] <= row2['bpm']) else "grey")
    m1 = colored_metric(label="Tempo (BPM)", value=row2['bpm'], val_color=color, align="right", delta=delta_v, delta_b_color=b, delta_t_color=t)
    for i in range(2):
        st.markdown("")
    st.markdown(m1, unsafe_allow_html=True)

    # duration
    if (row1['sec_duration'] < row2['sec_duration']):
        delta_v = f"{up_or_down(row2['sec_duration'], row1['sec_duration'])} {round(100*(row2['sec_duration'] - row1['sec_duration']) / row1['sec_duration'], 2)}%"
        b = SECONDARY2
        t = SECTEXT2
    elif row1['sec_duration'] == row2['sec_duration']:
        delta_v = "Tie!"
        b = SECONDARY2
        t = SECTEXT2
    else:
        delta_v = "'"
        t = "#F9F6EE"
        b = "#F9F6EE"
    color2 = (PRIMARY2 if (row1['sec_duration'] <= row2['sec_duration']) else "grey")
    m2 = colored_metric(label="Duration (Seconds)", value=row2['sec_duration'], val_color=color2, align="right", delta=delta_v, delta_b_color=b, delta_t_color=t)
    for i in range(2):
        st.markdown("")
    st.markdown(m2, unsafe_allow_html=True)

    # year written
    if (row1['year'] > row2['year']):
        delta_v = f"{up_or_down(row2['year'], row1['year'])} {abs(row2['year'] - row1['year'])} Years"
        b = SECONDARY2
        t = SECTEXT2
    elif row1['year'] == row2['year']:
        delta_v = "Tie!"
        b = SECONDARY2
        t = SECTEXT2
    else:
        delta_v = "'"
        t = "#F9F6EE"
        b = "#F9F6EE"
    color3 = (PRIMARY2 if row1['year'] >= row2['year'] else "grey")
    m3 = colored_metric(label="Year Written", value=row2['year'], val_color=color3, align="right", delta=delta_v, delta_b_color=b, delta_t_color=t)
    for i in range(2):
        st.markdown("")
    st.markdown(m3, unsafe_allow_html=True)

    # trope count
    if (row1['trope_count'] < row2['trope_count']):
        delta_v = f"{up_or_down(row2['trope_count'], row1['trope_count'])} {(row2['trope_count'] - row1['trope_count'])} Tropes"
        b = SECONDARY2
        t = SECTEXT2
    elif row1['trope_count'] == row2['trope_count']:
        delta_v = "Tie!"
        b = SECONDARY2
        t = SECTEXT2
    else:
        delta_v = "'"
        t = "#F9F6EE"
        b = "#F9F6EE"
    color4 = (PRIMARY2 if row1['trope_count'] <= row2['trope_count'] else "grey")
    m4 = colored_metric(label="Trope Count", value=row2['trope_count'], val_color=color4, align="right", delta=delta_v, delta_b_color=b, delta_t_color=t)
    for i in range(2):
        st.markdown("")
    st.markdown(m4, unsafe_allow_html=True)
    
    # fight count
    if (row1['number_fights'] < row2['number_fights']):
        delta_v = f"{up_or_down(row2['number_fights'], row1['number_fights'])} {(row2['number_fights'] - row1['number_fights'])} Fights"
        b = SECONDARY2
        t = SECTEXT2
    elif row1['number_fights'] == row2['number_fights']:
        delta_v = "Tie!"
        b = SECONDARY2
        t = SECTEXT2
    else:
        delta_v = "'"
        t = "#F9F6EE"
        b = "#F9F6EE"
    color5 = (PRIMARY2 if row1['number_fights'] <= row2['number_fights'] else "grey")
    m5 = colored_metric(label="Fight Count", value=row2['number_fights'], val_color=color5, align="right", delta=delta_v, delta_b_color=b, delta_t_color=t)
    for i in range(2):
        st.markdown("")
    st.markdown(m5, unsafe_allow_html=True)
    
with arrow:
    # tempo
    if row1['bpm'] == row2['bpm']:
        v = "="
    elif row1['bpm'] > row2['bpm']:
        v = "←"
    else:
        v = "→"
    for i in range(3):
        st.markdown("")
    st.markdown(f"""<div style="font-size: 100px;font-weight: 700;text-align: center;line-height: 1;">{v}</div>""", unsafe_allow_html=True)
    # duration
    if row1['sec_duration'] == row2['sec_duration']:
        v = "="
    elif row1['sec_duration'] > row2['sec_duration']:
        v = "←"
    else:
        v = "→"
    for i in range(3):
        st.markdown("")
    st.markdown(f"""<div style="font-size: 100px;font-weight: 700;text-align: center;line-height: 1;">{v}</div>""", unsafe_allow_html=True)
    # year
    if row1['year'] == row2['year']:
        v = "="
    elif row1['year'] > row2['year']:
        v = "→"
    else:
        v = "←"
    for i in range(3):
        st.markdown("")
    st.markdown(f"""<div style="font-size: 100px;font-weight: 700;text-align: center;line-height: 1;">{v}</div>""", unsafe_allow_html=True)
    # trope count
    if row1['trope_count'] == row2['trope_count']:
        v = "="
    elif row1['trope_count'] > row2['trope_count']:
        v = "←"
    else:
        v = "→"
    for i in range(3):
        st.markdown("")
    st.markdown(f"""<div style="font-size: 100px;font-weight: 700;text-align: center;line-height: 1;">{v}</div>""", unsafe_allow_html=True)
    # fight count
    if row1['number_fights'] == row2['number_fights']:
        v = "="
    elif row1['number_fights'] > row2['number_fights']:
        v = "←"
    else:
        v = "→"
    for i in range(3):
        st.markdown("")
    st.markdown(f"""<div style="font-size: 100px;font-weight: 700;text-align: center;line-height: 1;">{v}</div>""", unsafe_allow_html=True)

st.markdown(f"""
            <p style="text-align:center; font-size:0.9rem; color:#6b6b6b;">
                Delta pills under winning metrics represent the increase or decrease from the opposing school
            </p>
           """, unsafe_allow_html=True)
'---'
# trope radar plot
dual_school_radar_plot(df, school1, school2, PRIMARY1, PRIMARY2)

st.markdown(
    """
    <p style="
        text-align: center;
        color: grey;
        font-size: 0.9rem;
        margin-top: 0.25rem;
    ">
        This radar plot compares the number of tropes present in each school fight song. 
    </p>
    """,
    unsafe_allow_html=True
)

'---'

# ranking chart with both schools
tab_styler("grey", "#969696", "white")
tabs = st.tabs(["**Tempo**", "**Duration**", "**Year**", "**Tropes**"])
col_metric, col_graph =st.columns([0.5, 10])

with tabs[0]:
    rank_choice = "Tempo Rank"
    fig = big_ten_rank_bars_dual(
        df, school1, school2, rank_choice, PRIMARY1, PRIMARY2, "grey"
    )
    st.plotly_chart(fig, width="stretch")
with tabs[1]:
    rank_choice = "Duration Rank"
    fig = big_ten_rank_bars_dual(
        df, school1, school2, rank_choice, PRIMARY1, PRIMARY2, "grey"
    )
    st.plotly_chart(fig, width="stretch")
with tabs[2]:
    rank_choice = "Year Written Rank"
    fig = big_ten_rank_bars_dual(
        df, school1, school2, rank_choice, PRIMARY1, PRIMARY2, "grey"
    )
    st.plotly_chart(fig, width="stretch")
with tabs[3]:
    rank_choice = "Trope Density Rank"
    fig = big_ten_rank_bars_dual(
        df, school1, school2, rank_choice, PRIMARY1, PRIMARY2, "grey"
    )
    st.plotly_chart(fig, width="stretch")

st.markdown(
    f"""
    <p style="
        text-align: center;
        color: grey;
        font-size: 0.9rem;
        margin-top: 0.25rem;
    ">
        These plots compare the two compared schools, <b>{school1}</b> and <b>{school2}</b>, 
        against the rest of the Big Ten. These charts explore the variables of <i>Tempo</i>, <i>Duration</i>, <i>Year Written</i>, and <i>Trope Counts</i>.
        Schools are highlighted in their respective school colors. 
    </p>
    """,
    unsafe_allow_html=True
)

'---'

chart = big_tempo_duration_dual(df, school1, school2, PRIMARY1, PRIMARY2)
st.plotly_chart(chart, theme="streamlit", width="stretch")

st.markdown(
    f"""
    <p style="
        text-align: center;
        color: grey;
        font-size: 0.9rem;
        margin-top: 0.25rem;
    ">
        This scatterplot explores the difference in tempo and length of a fight song between not only <b>{school1}</b> and <b>{school2}</b>, 
        but also the other Big Ten schools and the conference averages. The schools are highlighted in their respective colors.  
    </p>
    """,
    unsafe_allow_html=True
)

'---'

# explore other pages buttons
pill_button_styler("grey", "#969696", "white")
st.header("Navigate to Pages")
st.markdown("""Navigate through the sidebar or buttons below to access these additional pages 
            and enhance your understanding of the fight songs that represent the spirit of the Big Ten!""")
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("Home", width="stretch"):
        st.switch_page("Home.py")

with col2:
    if st.button("School Profiles", width="stretch"):
        st.switch_page("pages/2_School_Profiles.py")

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
        <span style="color:{PRIMARY1};">{school1}</span> vs 
        <span style='color:{PRIMARY2};'>{school2}</span> Battle!
    </h2>
    """,
    unsafe_allow_html=True
)
st.sidebar.caption("Analysis by *Colin Bertrand*")
st.sidebar.markdown('---')
st.sidebar.subheader("About This Page")
st.sidebar.markdown(
    f"""
    <p>
        Compare the fight songs of 
        <span style="color:{PRIMARY1}; font-weight:600;">{row1['song_name']}</span> and 
        <span style="color:{PRIMARY2}; font-weight:600;">{row2['song_name']}</span>.
    </p>
    <p><b>Key Metrics:</b></p>
    <ul>
        <li>Head-to-head tempo, duration, and trope stats</li>
        <li>Big Ten ranking context for each metric</li>
        <li>Scatter, radar, and bar visualizations side-by-side</li>
    </ul>
    <p>
        Use the school selectors up top, then hit <b>Battle!</b> to refresh the comparison.
    </p>
    """,
    unsafe_allow_html=True
)
st.sidebar.markdown(background_band_fill_side(
    subtitle="Tip: switch schools to reset the battle, or use the navigation buttons at the bottom to jump to other pages.",
    secondary_color="#969696",
    text_color="#000000",
    border=True,
    border_color="grey"
), unsafe_allow_html=True)
