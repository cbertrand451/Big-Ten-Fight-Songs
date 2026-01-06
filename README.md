# B1G Fight Songs

An interactive Streamlit dashboard that analyzes Big Ten fight songs by tempo, duration, and lyrical tropes, with head-to-head comparisons and school profiles.

[Dashboard Link]("bigtenfightsongs.streamlit.app")

## How to Use the App
1. Install dependencies: `pip install -r requirements.txt`
2. Create the Big Ten dataset (run once): `python -c "from utils.big_data import big_data; big_data()"`
   - This reads `data/raw/fight-songs-updated.csv` and writes `data/B1G/big_ten_fight_songs.csv`.
3. Launch Streamlit: `streamlit run Home.py`
4. Navigate pages from the sidebar or homepage buttons:
   - **Home**: Summary metrics, tempo vs. duration scatter, trope radar, heatmap, and Big Ten rankings.
   - **School Profiles**: Individual school deep dives with lyrical trope radar overlays and song details.
   - **Battle of the Bands**: Compare any two schools with dual radars, ranking bars, and branded visuals.
   - **Data Dictionary**: Definitions of fields, tropes, and metrics used throughout the app.
   - **Methodology**: Data pipeline, processing steps, analyses performed, and visualization approach.

## Project Overview
- Focuses on the 18 schools in the Big Ten Conference.
- Explores how tempo, duration, and lyrical tropes vary across the conference.
- Uses school color palettes and logos to keep visuals on-brand while highlighting differences and similarities.

## Data Pipeline
- Raw data ingested from FiveThirtyEight and then filtered/cleaned to create the Big Ten dataset (`utils/big_data.big_data`).
- Binary lyric trope fields converted to integers to enable numeric analysis and plotting.
- Colors and branding details stored in JSON files under `data/colors` for consistent theming across pages.

## Visualization Highlights
- Plotly visuals embedded in Streamlit: tempo/duration scatter, trope radar charts, trope heatmap, dual radars, and ranking bars.
- Interactive hovers expose exact trope usage, BPM, and durations; conference-average guides provide quick context.
- Story flows from conference overview to individual profiles to head-to-head comparisons.

## Sources
- FiveThirtyEight Fight Songs dataset: https://github.com/fivethirtyeight/data/tree/master/fight-songs
- School color codes: official branding/image guideline pages (links in `data/colors/color_links.json`).
- Big Ten conference colors: https://www.brandcolorcode.com/big-ten-conference
- Logos: downloaded from https://bigten.org/
- Secondary text color mapping created manually for readability (`data/colors/secondary_text_colors.json`).
- Additional sources (videos, branding and color guidelines) are listed in the **Methodology** page of the app!

## Repository Structure
- `Home.py`: Landing page with summary visuals and navigation.
- `pages/`: Streamlit multipage modules (School Profiles, Battle of the Bands, Data Dictionary, Methodology).
- `utils/`: Data loading, cleaning, plotting helpers, and styling components.
- `data/raw/`: Source CSV from FiveThirtyEight; `data/B1G/`: cleaned Big Ten dataset.
- `data/colors/` and `data/logos/`: Branding assets and references.


