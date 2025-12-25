import pandas as pd
import streamlit as st
import numpy as np

#create big ten dataset
def big_data():
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
    return df_big

def get_big_data():
    df_big = pd.read_csv("data/B1G/big_ten_fight_songs.csv")
    return df_big

# find summary metrics
def big_metrics(df: pd.DataFrame):
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    with c1:
        # average bpm
        st.metric(label='Average BPM', value=round(df['bpm'].mean(), 2))
    with c2:
        # average duration
        st.metric(label='Average Duration (seconds)', value=round(df['sec_duration'].mean(), 2))
    with c3:
        # average trope count
        st.metric(label='Average Trope Count', value=round(df['trope_count'].mean(), 2))
    with c4:
        # most common trope
        st.metric(label='Most Common Trope', value=df[['spelling', 
                                                       'opponents', 
                                                       'men', 
                                                       'colors', 
                                                       'nonsense',
                                                       'rah',
                                                       'win_won',
                                                       'victory',
                                                       'fight']].sum().idxmax())
    with c5:
        # oldest song
        row = df.loc[df['year'].idxmin()]
        st.metric(label='Oldest Song', value=f'{row["school"]}: {row["year"]}')
    with c6:
        # newest song
        row = df.loc[df['year'].idxmax()]
        st.metric(label='Newest Song', value=f'{row["school"]}: {row["year"]}')


def big_rankings(df: pd.DataFrame):
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        # fastest song 
        row = df.loc[df['bpm'].idxmax()]
        st.metric(label="Fastest Fight Song (BPM)", value=f'{row["school"]}: {row["bpm"]}')
    with c2:
        # longest song 
        row = df.loc[df['sec_duration'].idxmax()]
        st.metric(label="Longest Fight Song (Seconds)", value=f'{row["school"]}: {row["sec_duration"]}')
    with c3:
        # most tropes 
        row = df.loc[df['trope_count'].idxmax()]
        st.metric(label="Most Trope Heavy Song", value=f'{row["school"]}: {row["trope_count"]}') 
    with c4:
        trope_cols = [
        "fight", "victory", "win_won", "rah",
        "nonsense", "colors", "men",
        "opponents", "spelling"
        ]   
        conf_avg = df[trope_cols].mean().values
        df["distance_to_conf_avg"] = df[trope_cols].apply(
        lambda row: np.linalg.norm(row.values - conf_avg),
        axis=1
        )
        row = df.loc[df['distance_to_conf_avg'].idxmin()]
        st.metric(label="Most *Traditional* Song", value=f'{row["school"]}')
        with c5:
            # most unique song
            row = df.loc[df['distance_to_conf_avg'].idxmax()]
            st.metric(label="Most *Unique* Song", value=f'{row["school"]}')


