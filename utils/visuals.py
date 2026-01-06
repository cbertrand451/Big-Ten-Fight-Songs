import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import json
from pathlib import Path
from utils.colors import hex_to_rgb


# radar plot for big ten average trpoe values
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

    st.plotly_chart(fig, theme="streamlit", width="stretch")



# scatterplot for all big ten schools (tempo vs duration)
def big_tempo_duration(df: pd.DataFrame):
    # get tempo and duration means
    tempo_mean = df['bpm'].mean()
    duration_mean = df['sec_duration'].mean()
    # loading colors
    COLOR_PATH = Path("data/colors/school_colors.json")
    with open(COLOR_PATH, "r") as f:
        SCHOOL_COLORS = json.load(f)
    
    # create plot
    fig = px.scatter(df, x='sec_duration', y='bpm', title="Big Ten Tempo vs. Duration", 
                     labels={'bpm': 'Tempo (BPM)', 'sec_duration': 'Duration (Seconds)'},
                     color='school', color_discrete_map=SCHOOL_COLORS, custom_data=['school'])
    fig.update_traces(marker=dict(size=12, line=dict(width=2, color='grey')), 
                      selector=dict(mode='markers'),
                      hovertemplate=(
                        "<b>%{customdata[0]}</b><br>"
                        "Tempo (BPM): %{y:.0f}<br>"
                        "Duration: %{x:.0f} seconds"
                        "<extra></extra>"))
    fig.add_vline(
        x=duration_mean,
        line_dash="dash",
        line_color="gray",
        annotation_text=f"Avg Duration: {round(duration_mean, 2)}",
        annotation_position="top"
    )
    fig.add_hline(
        y=tempo_mean,
        line_dash="dash",
        line_color="gray",
        annotation_text=f"Avg Tempo: {round(tempo_mean, 2)}",
        annotation_position="bottom right"
    )
    
    st.plotly_chart(fig, theme="streamlit", width="stretch")


# heatmap for whether or not a trope is present in a big ten fight song
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
    fig = px.imshow(heatmap_df, aspect="auto", color_continuous_scale=["#FFFFFF", "#0085CE"],
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
    
    st.plotly_chart(fig, theme="streamlit", width="stretch")


# creates a radar plot for a school with the trope values present, and overlays it on top of the big ten average trope values
def school_radar_plot(df: pd.DataFrame, school, school_color="FFFFFF"):
    tropes = [
        'spelling',
        'opponents',
        'men',
        'colors',
        'nonsense',
        'rah',
        'win_won',
        'victory',
        'fight'
    ]

    # big ten
    trope_means = df[tropes].mean()
    cats = trope_means.index.tolist()
    big_vals = trope_means.values.tolist()

    # school
    school_row = df.loc[df['school'] == school]
    school_vals = school_row[tropes].iloc[0].tolist()

    # Close loops
    cats_closed = cats + [cats[0]]
    big_vals_closed = big_vals + [big_vals[0]]
    school_vals_closed = school_vals + [school_vals[0]]

    max_val = max(big_vals_closed + school_vals_closed) * 1.15

    fig = go.Figure()

    rgbs = hex_to_rgb(school_color)
    r_ = rgbs[0]
    g_ = rgbs[1]
    b_ = rgbs[2]
    # School trace 
    fig.add_trace(
        go.Scatterpolar(
            r=school_vals_closed,
            theta=cats_closed,
            fill="toself",
            name=school,
            line=dict(width=4, color=school_color),
            fillcolor=f"rgba({r_}, {g_}, {b_}, 0.25)",
            hovertemplate=f"<b>%{{theta}}</b><br>{school}: %{{r:.3f}}<extra></extra>"
        )
    )

    # Big Ten trace 
    fig.add_trace(
        go.Scatterpolar(
            r=big_vals_closed,
            theta=cats_closed,
            fill="toself",
            name="Big Ten Avg",
            line=dict(width=3, color="rgb(150,150,150)"),
            fillcolor=f"rgba(150,150,150,0.25)",
            hovertemplate="<b>%{theta}</b><br>Big Ten Avg: %{r:.3f}<extra></extra>"
        )
    )



    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, max_val],
                tickformat=".2f"
            )
        ),
        title=dict(
            text=f"""
                <span style="color:{school_color};">{school}</span> vs <span style="color:rgb(150,150,150);">Big Ten</span> Trope Identity
            """,
            font=dict(size=16)
        ),
        showlegend=True,
        legend=dict(orientation="h", y=-0.15),
        height=520,
        margin=dict(t=80, b=60, l=40, r=40),
    )

    st.plotly_chart(fig, theme="streamlit", width="stretch")


# rank dictionary used to grab the characertistics of the bar charts
RANK_CONFIG = {
    "Tempo Rank": {
        "col": "bpm",
        "ascending": True, 
        "label": "Tempo (BPM)",
        "xaxis": "Slowest → Fastest",
        "show_avg": True,
        "an_po": "top left"
    },
    "Duration Rank": {
        "col": "sec_duration",
        "ascending": True,
        "label": "Duration (seconds)",
        "xaxis": "Shortest → Longest",
        "show_avg": True,
        "an_po": "top left"
    },
    "Year Written Rank": {
        "col": "year_offset",
        "ascending": False,
        "label": "Year Written",
        "xaxis": "Newest → Oldest",
        "axis_mode": "year_offset",
        "tick_step": 10,
        "original": "year",
        "show_avg": True,
        "an_po": "top right"
    },
    "Trope Density Rank": {
        "col": "trope_count",
        "ascending": True,
        "label": "Total Tropes",
        "xaxis": "Least → Most",
        "show_avg": True,
        "an_po": "top left"
    }
}

# creates bar charts based on a number of variables, specific school highlighted with the rest grey
def big_ten_rank_bars(df: pd.DataFrame, school, rank_key, color, color2):
    year_min = df['year'].min() - 10
    df['year_offset'] = df['year'] - year_min
    cfg = RANK_CONFIG[rank_key]

    plot_df = df.sort_values(cfg['col'], ascending=cfg['ascending']).reset_index(drop=True)

    plot_df['color'] = plot_df['school'].apply(
        lambda x: color if x == school else "rgb(150, 150, 150)"
    )
    
    years = plot_df['year']
    fig = go.Figure(
        go.Bar(
            x=plot_df['school'],
            y=plot_df[cfg['col']],
            marker_color=plot_df['color'],
            hovertemplate=(
                "<b>%{x}</b><br>"
                f"Year Written: %{{customdata}}<extra></extra>"
                if cfg.get("axis_mode") == "year_offset"
                else
                f"<b>%{{x}}</b><br>{cfg['label']}: %{{y}}<extra></extra>"
            ),
            customdata=plot_df['year'] if cfg.get("axis_mode") == "year_offset" else None
        )
    )

    if cfg.get("axis_mode") == "year_offset":
        year_min = df['year'].min() - 10
        year_max = df['year'].max() + 10
        step = cfg.get('tick_step', 10)

        tick_years = list(range(year_min, year_max + 1, step))
        tick_vals = [y - year_min for y in tick_years]

        fig.update_yaxes(
            tickmode="array",
            tickvals=tick_vals,
            ticktext=tick_years,
            title="Year Written"
        )

    else:
        fig.update_yaxes(title=cfg['label'])

    if cfg.get("show_avg", False):
        avg_val = plot_df[cfg['col']].mean()

        fig.add_hline(
            y=avg_val,
            line_dash='dash',
            line_width=2,
            line_color=color2,
            annotation_text=f"Big Ten Average: {round(avg_val)}",
            annotation_position=cfg['an_po']
        )

    plot_df["rank"] = plot_df.index + 1

    # extract selected school's row
    school_row = plot_df.loc[plot_df["school"] == school].iloc[0]

    school_rank = abs(int(school_row["rank"]) - 19)
    n_schools = len(plot_df)

    # handle displayed value (year vs offset)
    if cfg.get("axis_mode") == "year_offset":
        school_value = int(school_row["year"])
        value_label = "Year Written"
    else:
        school_value = round(school_row[cfg["col"]], 2)
        value_label = cfg["label"]
    title_text = (
        #f"<b style='color:{color}; font-size:1.2em;'>{school}</b> — "
        #f"<span style='font-size:24px;'>{value_label}: <span style='color:{color};'>{school_value}</span> "
        f"<span style='font-size:24px;'>Ranked <span style='color:{color}'>{school_rank} <span style='color:black'>of {n_schools}</span>"
    )
    subtitle_text = f"{value_label}: {school_value}"

    fig.update_layout(
        height=500,
        margin=dict(l=120, r=40, t=40, b=40),
        xaxis_title=cfg["xaxis"],
        showlegend=False,
        title={
            "text": (
                title_text
                + "<br>"
                + f"<span style='font-size:16px;color:gray'>{subtitle_text}</span>"
            ),
            "x": 0.5,
            "xanchor": "center",
        }
    )

    return fig


# create a radar plot between two schools with custom colors
def dual_school_radar_plot(
    df: pd.DataFrame,
    school_left: str,
    school_right: str,
    left_color: str,
    right_color: str
):
    tropes = [
        'spelling',
        'opponents',
        'men',
        'colors',
        'nonsense',
        'rah',
        'win_won',
        'victory',
        'fight'
    ]

    #  Extract school rows 
    left_row = df.loc[df['school'] == school_left]
    right_row = df.loc[df['school'] == school_right]

    if left_row.empty or right_row.empty:
        st.error("One or both schools not found in dataframe.")
        return

    left_vals = left_row[tropes].iloc[0].tolist()
    right_vals = right_row[tropes].iloc[0].tolist()

    # Close radar loop
    cats = tropes
    cats_closed = cats + [cats[0]]
    left_vals_closed = left_vals + [left_vals[0]]
    right_vals_closed = right_vals + [right_vals[0]]

    max_val = max(left_vals_closed + right_vals_closed) * 1.15

    fig = go.Figure()

    # Color prep 
    lr, lg, lb = hex_to_rgb(left_color)
    rr, rg, rb = hex_to_rgb(right_color)

    # Left School 
    fig.add_trace(
        go.Scatterpolar(
            r=left_vals_closed,
            theta=cats_closed,
            fill="toself",
            name=school_left,
            line=dict(width=4, color=left_color),
            fillcolor=f"rgba({lr},{lg},{lb},0.25)",
            hovertemplate=(
                f"<b>%{{theta}}</b><br>"
                f"{school_left}: %{{r:.3f}}<extra></extra>"
            )
        )
    )

    # Right School 
    fig.add_trace(
        go.Scatterpolar(
            r=right_vals_closed,
            theta=cats_closed,
            fill="toself",
            name=school_right,
            line=dict(width=4, color=right_color),
            fillcolor=f"rgba({rr},{rg},{rb},0.25)",
            hovertemplate=(
                f"<b>%{{theta}}</b><br>"
                f"{school_right}: %{{r:.3f}}<extra></extra>"
            )
        )
    )

    # Layout (CENTERED EVERYTHING) 
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, max_val],
                tickformat=".2f",
                ticks="outside"
            )
        ),
        title=dict(
            text=(
                f"<span style='color:{left_color};'>{school_left}</span>"
                f" <span style='color:#888;'>vs</span> "
                f"<span style='color:{right_color};'>{school_right}</span>"
                "<br><span style='font-size:13px;color:#666;'>Trope Identity Comparison</span>"
            ),
            x=0.5,
            xanchor="center",
            yanchor="top",
            font=dict(size=18)
        ),
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.12,
            xanchor="center",
            x=0.5
        ),
        height=540,
        margin=dict(t=90, b=70, l=40, r=40),
        showlegend=True
    )

    st.plotly_chart(fig, theme="streamlit", width="stretch")


# create the same bar charts as before but this time inject colors for two battling schools, rest are grey
def big_ten_rank_bars_dual(
    df: pd.DataFrame,
    school_left: str,
    school_right: str,
    rank_key: str,
    color_left: str,
    color_right: str,
    avg_color: str
):
    year_min = df['year'].min() - 10
    df['year_offset'] = df['year'] - year_min
    cfg = RANK_CONFIG[rank_key]

    plot_df = df.sort_values(cfg['col'], ascending=cfg['ascending']).reset_index(drop=True)

    # Color mapping 
    def bar_color(s):
        if s == school_left:
            return color_left
        elif s == school_right:
            return color_right
        else:
            return "rgb(150,150,150)"

    plot_df["color"] = plot_df["school"].apply(bar_color)

    fig = go.Figure(
        go.Bar(
            x=plot_df["school"],
            y=plot_df[cfg["col"]],
            marker_color=plot_df["color"],
            customdata=plot_df["year"] if cfg.get("axis_mode") == "year_offset" else None,
            hovertemplate=(
                "<b>%{x}</b><br>"
                "Year Written: %{customdata}<extra></extra>"
                if cfg.get("axis_mode") == "year_offset"
                else
                f"<b>%{{x}}</b><br>{cfg['label']}: %{{y}}<extra></extra>"
            )
        )
    )

    # Axis handling 
    if cfg.get("axis_mode") == "year_offset":
        year_max = df['year'].max() + 10
        step = cfg.get("tick_step", 10)

        tick_years = list(range(year_min, year_max + 1, step))
        tick_vals = [y - year_min for y in tick_years]

        fig.update_yaxes(
            tickmode="array",
            tickvals=tick_vals,
            ticktext=tick_years,
            title="Year Written"
        )
    else:
        fig.update_yaxes(title=cfg["label"])

    # Conference average 
    if cfg.get("show_avg", False):
        avg_val = plot_df[cfg["col"]].mean()
        fig.add_hline(
            y=avg_val,
            line_dash="dash",
            line_width=2,
            line_color=avg_color,
            annotation_text=f"Big Ten Avg: {round(avg_val)}",
            annotation_position=cfg['an_po']
        )

    # Ranking calculation 
    plot_df["rank"] = plot_df.index + 1
    n_schools = len(plot_df)

    def get_rank_info(school):
        row = plot_df.loc[plot_df["school"] == school].iloc[0]
        rank = abs(int(row["rank"]) - n_schools - 1)
        if cfg.get("axis_mode") == "year_offset":
            val = int(row["year"])
            label = "Year Written"
        else:
            val = round(row[cfg["col"]], 2)
            label = cfg["label"]
        return rank, val, label

    left_rank, left_val, label = get_rank_info(school_left)
    right_rank, right_val, _ = get_rank_info(school_right)

    #  Title 
    title_text = (
        f"<span style='color:{color_left}; font-size:22px;'>{school_left}</span>"
        f"<span style='color:#666; font-size:18px;'> (#{left_rank})</span>"
        " &nbsp;&nbsp;|&nbsp;&nbsp; "
        f"<span style='color:{color_right}; font-size:22px;'>{school_right}</span>"
        f"<span style='color:#666; font-size:18px;'> (#{right_rank})</span>"
    )

    subtitle_text = (
        f"{label}: "
        f"<span style='color:{color_left};'>{left_val}</span>"
        " vs "
        f"<span style='color:{color_right};'>{right_val}</span>"
    )

    fig.update_layout(
        height=520,
        margin=dict(l=120, r=40, t=60, b=40),
        xaxis_title=cfg["xaxis"],
        showlegend=False,
        title=dict(
            text=title_text + "<br><span style='font-size:15px;color:gray'>" + subtitle_text + "</span>",
            x=0.5,
            xanchor="center"
        )
    )

    return fig


# creates a scatterplot which colors two specific schools and makes the rest grey, shows tempo vs duration
def big_tempo_duration_dual(
    df: pd.DataFrame,
    school_left: str,
    school_right: str,
    color_left: str,
    color_right: str
):
    # Conference averages 
    tempo_mean = df['bpm'].mean()
    duration_mean = df['sec_duration'].mean()

    # Assign plotting color 
    def assign_color(s):
        if s == school_left:
            return school_left
        elif s == school_right:
            return school_right
        else:
            return "Other Schools"

    plot_df = df.copy()
    plot_df["highlight"] = plot_df["school"].apply(assign_color)

    color_map = {
        school_left: color_left,
        school_right: color_right,
        "Other Schools": "rgb(150,150,150)"
    }

    # Create plot 
    fig = px.scatter(
        plot_df,
        x="sec_duration",
        y="bpm",
        color="highlight",
        color_discrete_map=color_map,
        hover_data={
            "school": True,
            "bpm": True,
            "sec_duration": True,
            "highlight": False
        },
        labels={
            "bpm": "Tempo (BPM)",
            "sec_duration": "Duration (Seconds)"
        },
        title="Big Ten Tempo vs. Duration",
        custom_data=['school']
    )

    # Marker styling 
    fig.update_traces(
        marker=dict(
            size=12,
            line=dict(width=2, color="grey"),
            opacity=0.9
        ),
        selector=dict(mode="markers"),
        hovertemplate=(
                        "<b>%{customdata[0]}</b><br>"
                        "Tempo (BPM): %{y:.0f}<br>"
                        "Duration: %{x:.0f} seconds"
                        "<extra></extra>")
    )

    # Emphasize highlighted schools 
    fig.update_traces(
        marker=dict(size=16, opacity=1),
        selector=dict(name=school_left)
    )
    fig.update_traces(
        marker=dict(size=16, opacity=1),
        selector=dict(name=school_right)
    )

    # Mean lines 
    fig.add_vline(
        x=duration_mean,
        line_dash="dash",
        line_color="gray",
        annotation_text=f"Avg Duration: {round(duration_mean, 2)}",
        annotation_position="top"
    )
    fig.add_hline(
        y=tempo_mean,
        line_dash="dash",
        line_color="gray",
        annotation_text=f"Avg Tempo: {round(tempo_mean, 2)}",
        annotation_position="right"
    )

    fig.update_layout(
        height=520,
        showlegend=True,
        legend_title_text="",
        margin=dict(t=60, b=40, l=40, r=40)
    )

    return fig
