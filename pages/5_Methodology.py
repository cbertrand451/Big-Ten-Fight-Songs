import streamlit as st
from utils.components import background_band_fill_side, colored_text, pill_button_styler
from utils.big_data import get_big_data
from utils.colors import get_school_colors, load_json

st.set_page_config(page_title="Methodology", 
                   layout="wide")
# define the big ten blue color
PRIMARY = "#0085CE" 
# get data
df = get_big_data()
# get list of the schools
schools = df['school'].tolist()
# title + caption
st.markdown("<h1 style='text-align:center;'>Methodology</h1>", unsafe_allow_html=True)

st.markdown("<h4 style='text-align:center;'>An explanation of the process taken to build this project</h3>", unsafe_allow_html=True)

'---'

# describe the data pipeline
colored_text("Data Pipeline", "h2", "bold", "#000000")

st.markdown(
    f"""
    <ul style="margin-left: 1.2rem;">
        <li>
            <span style="color:{PRIMARY}; font-weight:600;font-size: 24px;">Creation / Generation</span>
            <span style="color:#000000;">: raw fight song and school metadata ingestion</span>
        </li>
        <li>
            <span style="color:{PRIMARY}; font-weight:600;font-size: 24px;">Collection</span>
            <span style="color:#000000;">: sourcing song and school data</span>
        </li>
        <li>
            <span style="color:{PRIMARY}; font-weight:600;font-size: 24px;">Processing / Cleaning</span>
            <span style="color:#000000;">: normalization and generation</span>
        </li>
        <li>
            <span style="color:{PRIMARY}; font-weight:600;font-size: 24px;">Storage</span>
            <span style="color:#000000;">: structured CSV + JSON persistence</span>
        </li>
        <li>
            <span style="color:{PRIMARY}; font-weight:600;font-size: 24px;">Analysis / Usage</span>
            <span style="color:#000000;">: ranking, comparison, statistical exploration</span>
        </li>
        <li>
            <span style="color:{PRIMARY}; font-weight:600;font-size: 24px;">Sharing / Visualization</span>
            <span style="color:#000000;">: Streamlit dashboards and plots</span>
        </li>
        <li>
            <span style="color:{PRIMARY}; font-weight:600;font-size: 24px;">Archiving / Destruction</span>
            <span style="color:#000000;">: versioned snapshots and cleanup</span>
        </li>
    </ul>
    """,
    unsafe_allow_html=True
)

'---'

# creation and generation
colored_text("Creation / Generation", "h2", "bold", PRIMARY)
st.markdown("""
            Didn't have direct part in creation or generation of data. All data used throughout the process 
            was sourced online or downloaded extrernally. 

            The only data directly created by me was the *secondary_text_colors.json* file, found in **data/colors/secondary_text_colors.json**. 
            This file was made 
            by comparing the most readable color (black or white) against each school's secondary color. This
            data was used for page colors and visualizations. 
            """)


'---'

# collection
colored_text("Collection", "h2", "bold", PRIMARY)
st.subheader("Fight Song Dataset")
st.markdown("""
            [Original dataset]("https://github.com/fivethirtyeight/data/tree/master/fight-songs") was downloaded from FiveThirtyEight. 
            Called "fight-songs-updated.csv", this dataset contained the fight song data from all schools in the Power Five conferences...
            the ACC, Big Ten, Big 12, Pac-12 and SEC, plus Notre Dame. The dataset was put into the project file *raw* with path 
            **data/raw/fight-songs-updated.csv**.
            """)

st.subheader("School Colors")
st.markdown("""
            The colors (primary and secondary) for each school were found manually by searching the official
            schools' braning and images guidelines. The hex codes for each school were found from the respective pages:
            """)
links = load_json("data/colors/color_links.json")
for school in schools:
    st.markdown(
    f"""
    - <span style="color:{get_school_colors(school)['primary']};">{school}</span>
    <span style="color:#000000;">: {links[school]}</span>
    """,
    unsafe_allow_html=True
    )
st.markdown("All hexcodes were put into *school_colors.json* and *secondary_school_colors.json* in the **data/colors** folder")

st.subheader("Big Ten Colors")
st.markdown(
    f"""
    Big Ten colors were found online from [brandcolorcode]("https://www.brandcolorcode.com/big-ten-conference").
    Big Ten accent color was used in the **.streamlit/config.toml** file, which made the base page accent color the Big Ten blue. 
    """)

st.subheader("Images")
st.markdown("""
            All logos for the Big Ten were found on the [Official Big Ten Website]("https://bigten.org/"). 
            School logos were found on the top of the homepage, and Big Ten logo was found further down.
            """)

st.subheader("Videos")
st.markdown("""
            A playlist of Big Ten Fight songs was found on YouTube titled [Big ten fight songs]("https://www.youtube.com/playlist?list=PLdEih-bqJyY2y4tF9434Rlhx4fcvwageX").
            Though not sourced officially from the Big Ten, these videos provided the audio of the instrumentals as well as the 
            lyrics that went along with the song. These videos were not used in analysis or computing of any sort, and were specifically provided
            for the user to hear the fight song easily. 
            """)

'---'

# processing and cleaning
colored_text("Processing / Cleaning", "h2", "bold", PRIMARY)
st.subheader('Big Ten Dataset')
st.markdown("""
            The Big Ten dataset was created by taking the *fight-songs-updated.csv* file and running it through a cleaning function.
            The main function was replacing binary columns with "Yes" and "No" into integers 1 and 0, respectively. This allowed
            for numerical analysis on the binary columns. Visually there was no data missing, and all suspected numerical 
            variables were correctly identified as numerical. This function, when ran, created the Big Ten dataset and put 
            it in the **data/B1G/big_ten_fight_songs.csv** folder.

            Below is the big_data function which creates the dataset. This function needs to be run independently in order 
            for the dataset to be created, if this project were to be reproduced.
            """)
st.code("""def big_data():
    # read in raw data
    df = pd.read_csv("data/raw/fight-songs-updated.csv")
    # create b1g dataset
    df_big = df[df["conference"] == "Big Ten"]
    df_big['spelling'] = df_big['spelling'].map({'Yes': 1, 'No': 0}).astype(int)
    df_big['opponents'] = df_big['opponents'].map({'Yes': 1, 'No': 0}).astype(int)
    df_big['men'] = df_big['men'].map({'Yes': 1, 'No': 0}).astype(int)
    df_big['colors'] = df_big['colors'].map({'Yes': 1, 'No': 0}).astype(int)
    df_big['nonsense'] = df_big['nonsense'].map({'Yes': 1, 'No': 0}).astype(int)
    df_big['rah'] = df_big['rah'].map({'Yes': 1, 'No': 0}).astype(int)
    df_big['win_won'] = df_big['win_won'].map({'Yes': 1, 'No': 0}).astype(int)
    df_big['victory'] = df_big['victory'].map({'Yes': 1, 'No': 0}).astype(int)
    df_big['fight'] = df_big['fight'].map({'Yes': 1, 'No': 0}).astype(int)
    df_big['victory_win_won'] = df_big['victory_win_won'].map({'Yes': 1, 'No': 0}).astype(int)
    df_big['contest'] = df_big['contest'].map({'Yes': 1, 'No': 0}).astype(int)
    df_big['official_song'] = df_big['official_song'].map({'Yes': 1, 'No': 0}).astype(int)
    df_big['student_writer'] = df_big['student_writer'].map({'Yes': 1, 'No': 0}).astype(int)
    df_big['year'] = df_big['year'].astype(int)
    df_big.to_csv("data/B1G/big_ten_fight_songs.csv", index=False)
    
        """)

st.subheader("Images")
st.markdown("""
            The Big Ten schools logos came in many different image sizes. In order for the layout of the page to be consistent, 
            the sizes of the logos had to be proportional. All images were brought into *Adobe Photoshop* and downloaded as 
            a square image, with length and width in a 1 to 1 proportion. This allowed for the images to be displayed consistently across 
            each page and for each school.

            The original images were placed in **data/logos/original** and the new resized images were placed in **data/logos/resized**.
            """)

'---'

# storage
colored_text("Storage", "h2", "bold", PRIMARY)

st.subheader("Datasets")
st.markdown("""
            Both the raw data set and the Big Ten dataset were stored as CSV files in the data folder, 
            under *raw* and *B1G*, respectively. This allowed for pages to read the datasets through the python *Pandas* library. 
            """)

st.subheader("JSON Files")
st.markdown("""
            For characteristics, mainly colors, school variables were kept in JSON files. Instead of creating one 
            large file with multiple JSONs, I chose to have multiple singular files that could be sorted and named easily. School 
            *primary*, *secondary*, and *secondary text* colors were all put into their own JSON files. The links to the YouTube video 
            of each fight song was also kept in a JSON file, as well as the links to the urls of the color and brand guidleines for each school. 
            """)

'---'

# analysis
colored_text("Analysis / Usage", "h2", "bold", PRIMARY)

st.subheader("Conference-Level Exploration")
st.markdown("""
            Aggregated conference metrics were calculated to understand the Big Ten baseline. Average BPM, duration, trope counts, and most common trope were surfaced via summary cards, alongside leaderboard-style metrics for fastest, longest, oldest, most traditional, and most unique songs. Trope usage was profiled visually with a radar plot for the conference identity and a trope heatmap that spotlights how each school leans into or away from specific themes.
            """)

st.subheader("School Profiles & Trope Identity")
st.markdown("""
            Each school profile layers its individual radar plot on top of the conference average to quickly show which lyrical tropes a song emphasizes or avoids. Supporting metrics (tempo, duration, trope count, writer status, contest origins, official/unofficial designation) provide a concise statistical fingerprint for every fight song, grounded in the cleaned Big Ten dataset.
            """)

st.subheader("Tempo & Duration Relationships")
st.markdown("""
            A scatter plot of tempo versus duration (with conference averages annotated) highlights pacing trends across schools and makes it easy to spot outliers. This view is reused in comparisons to contextualize how each selection sits relative to Big Ten norms for speed and length.
            """)

st.subheader("Head-to-Head Battles")
st.markdown("""
            The Battle of the Bands page enables direct comparisons between any two schools. Dual radar plots, paired metrics, and ranking bars show where each song outperforms the other on lyrical tropes, pacing, and trope density, while shared visuals use school color palettes to maintain brand fidelity during side-by-side evaluations.
            """)

'---'

# sharing and visualization
colored_text("Sharing / Visualization", "h2", "bold", PRIMARY)

st.subheader("Streamlit Plot Integration")
st.markdown("""
            Plotly figures (radar charts, scatter plots, bar rankings, heatmaps) are embedded directly into Streamlit, preserving responsive sizing and color theming tied to each school's palette. Layouts use columns and bands to keep visuals centered and readable while matching the broader Big Ten visual identity.
            """)

st.subheader("Interactive Controls")
st.markdown("""
            Dropdowns and buttons drive the Battle of the Bands comparisons, while hover states on Plotly charts expose exact trope values, BPM, durations, and school names. Conference-average guides (horizontal and vertical lines) stay interactive, letting viewers trace how each song compares to the Big Ten baseline without losing context.
            """)

st.subheader("Narrative Storytelling")
st.markdown("""
            Visuals are ordered to move from conference overview (summary cards, trope radar, heatmap) to individual school stories (profile radar overlays, tempo/duration positioning) and finally to direct rivalries (dual radars and ranking bars). This progression mirrors the data pipeline, helping readers see how cleaned data transforms into insights about pace, trope identity, and tradition.
            """)

st.subheader("Figure Contributions Across Pages")
st.markdown("""
            - Conference radar + heatmap: establish trope norms and deviations by school.  
            - Tempo vs. duration scatter: shows pacing landscape and isolates outliers.  
            - School radar overlays: spotlight each song’s lyrical personality against the Big Ten average.  
            - Battle ranking bars and dual radars: explain head-to-head strengths and weaknesses with branded colors for quick scanning.
            """)

'---'

# archiving and destructions
colored_text("Archiving / Destructions", "h2", "bold", PRIMARY)
st.markdown("""
            Archiving was rather insignificant in this project, given the size and scope of the data. 
            This analysis acts entirely on 18 fight songs and the metadata that comes with them. 

            Because this project was made with the incentive to submit to the **Big Ten Data Viz Student Competition**, the 
            data usage couldn't be varied as much as a normal project may have been. 

            Either way, the data used here is simply stored in a CSV file that won't be updated or deleted as time passes,
            since the competition guidelines provide the dataset to be used. 
            """)

'---'

# conclusion + about me
colored_text("Conclusion", "h2", "bold", PRIMARY)

st.subheader("Thank You!!")
st.markdown("""This project was such a fun learning experience, and I hope that every user can discover something new about 
            a Big Ten Fight Song that they may not have known before!
            """)

st.subheader("About Me")
st.markdown(
    f"""
            I am a soon to be graduate of the 
            <span style='color:#FF5F05;weight:bold;'>University of Illinois Urbana - Champaign</span>, 
            majoring in **Data Science + Information Science**. I have previous interning experience in 
            **Data Science** and **Gen AI Architecture**, while building projects that deal with **Explorative Data Dashboards** 
            such as this one, **Geolocation Data**, **Machine Learning Classification**, and **Web Scraping**. 

            Here's my [Porfolio Website]("https://colinbertrand.streamlit.app") which showcases my professional resume 
            and other interesting aspects of my data science work!

            Feel free to check out my [LinkedIn]("https://www.linkedin.com/in/colin-bertrand-512138265/") and my 
            [GitHub]("https://github.com/cbertrand451")!
            """, unsafe_allow_html=True)

'---'

# explore other pages
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
    if st.button("Data Dictionary", width="stretch"):
        st.switch_page("pages/4_Data_Dictionary.py")


# sidebar
st.sidebar.header("Project Methodology")
st.sidebar.caption("by *Colin Bertrand*")
st.sidebar.markdown('---')
st.sidebar.subheader("About This Page")
st.sidebar.markdown("""
                    This page walks through the process taken to collect data and build the dashboard 
                    able to explore the Big Ten Fight Songs. The Methodology highlight the steps of 
                    a common data pipeline for a project like this, including:
                    
""")

st.sidebar.markdown("""
        - **Creating / Generation**
        - **Collection**
        - **Processing / Cleaning**
        - **Storage**
        - **Analysis / Usage**
        - **Sharing / Visualization**
        - **Archiving / Destructions**
            """)

st.sidebar.markdown("The steps here should be able to be followed thoroughly to reproduce a similar project.")

st.sidebar.markdown(background_band_fill_side(
    subtitle="Navigate between pages using the buttons at the bottom of the page or the sidebar navigation.",
        secondary_color="#B3B3B3",
        text_color="#000000",
        border=True,
        border_color="#0085CE"), unsafe_allow_html=True)
