import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import json
from pathlib import Path



def big_radar_plot(df: pd.DataFrame):
    # trope columns
    tropes = ['spelling', 
            'opponents', 
            'men', 
            'colors', 
            'nonsense',
            'rah',
            'win_won',
            'victory',
            'fight']
    
    # means of trope columns
    trope_means = df[tropes].mean()

    # get categories and values
    cats = trope_means.index.tolist()
    vals = trope_means.values.tolist()

    # closing looop for radar plot
    cats += [cats[0]]
    vals += [vals[0]]

    # create plot
    fig = go.Figure()
    fig.add_trace(
        go.Scatterpolar(
            r=vals,
            theta=cats,
            fill="toself",
            name="Big Ten",
            line=dict(width=3),
            hovertemplate="<b>%{theta}</b><br>Avg Usage: %{r:.3f}<extra></extra>"
        )
    )

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, max(vals) * 1.15]
            )
        ),
        showlegend=False,
        title=f"Big Ten Trope Identity",
        height=500,
        margin=dict(t=80, b=40, l=40, r=40),
    )

    st.plotly_chart(fig, theme="streamlit", use_container_width=True)


def big_tempo_duration(df: pd.DataFrame):
    # get tempo and duration means
    tempo_mean = df['bpm'].mean()
    duration_mean = df['sec_duration'].mean()
    # loading colors
    COLOR_PATH = Path("data/school_colors.json")
    with open(COLOR_PATH, "r") as f:
        SCHOOL_COLORS = json.load(f)
    
    # create plot
    fig = px.scatter(df, x='sec_duration', y='bpm', title="Big Ten Tempo vs. Duration", 
                     hover_data=['school', 'bpm', 'sec_duration'], labels={'bpm': 'Tempo (BPM)', 'sec_duration': 'Duration (Seconds)'},
                     color='school', color_discrete_map=SCHOOL_COLORS)
    fig.update_traces(marker=dict(size=12, line=dict(width=2, color='DarkSlateGrey')), 
                      selector=dict(mode='markers'))
    
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)

def big_trope_heatmap(df: pd.DataFrame):
    # trope columns
    tropes = ['spelling', 
            'opponents', 
            'men', 
            'colors', 
            'nonsense',
            'rah',
            'win_won',
            'victory',
            'fight']
    
    # get means of trope columns
    df = df.sort_values(by='school')
    heatmap_df = df.set_index('school')[tropes]

    # create heatmap
    fig = px.imshow(heatmap_df, aspect="auto", color_continuous_scale=["#FFFFFF", "#0085CA"],
        labels=dict(
            x="Lyrical Trope",
            y="School",
            color="Frequency"
        )
    )

    fig.update_layout(
        title="Trope Heatmap",
        height=600,
        margin=dict(t=80, b=40, l=120, r=40),
        coloraxis_colorbar=dict(
            title="Usage"
        )
    )
    
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)