import streamlit as st
import pandas as pd
from utils.visuals import RANK_CONFIG


# custom html for colored metrics
def colored_metric(label=None, 
                   value=None,
                   lab_color="#000000", 
                   val_color= "#000000", 
                   delta=None, 
                   delta_b_color="#FFFFFF", 
                   delta_t_color="#000000",
                   align="left"):
    align_map = {
        "left": ("flex-start", "left"),
        "center": ("center", "center"),
        "right": ("flex-end", "right"),
        }
    flex_align, text_align = align_map.get(align, ("flex-start", "left"))
    delta_html = ""
    if delta:
        delta_html = f"""<div style="
            display: flex;
            justify-content: {flex_align};
            margin-top: 4px;
        ">
            <div style="
                display: inline-block;
                background-color: {delta_b_color};
                color: {delta_t_color};
                padding: 4px 8px;
                border-radius: 20px;
                font-family: 'Source Sans Pro', sans-serif;
                font-size: 14px;
                font-weight: 600;
                white-space: nowrap;
                overflow: hidden;
                text-overflow: ellipsis;
            ">
                {delta}
            </div>
        </div>
        """
    html = f"""
    <div style="
        margin-bottom: 12px;
        text-align: {text_align};
    ">
        <div style="
            font-family: 'Source Sans Pro', sans-serif;
            font-size: 14px; 
            color: {lab_color}; 
            line-height: normal;
            margin: 0;
            padding: 0;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            height: auto;
            min-height: 1.5rem;
            display: flex;
            justify-content: {flex_align};
            align-items: center;
            font-weight: 500;">
            {label}
        </div>
        <div style="
            font-size: 36px; 
            font-weight: 500; 
            color: {val_color};
            line-height: normal;
            padding-bottom: 0.25rem;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            justify-content: {flex_align};
            width: 100%;">
            {value}
        </div>
    {delta_html}
    </div>
    """
    return html


# custom html injection for colored text
def colored_text(text, size="h3", weight="normal", color="#000000", align="left"):
    st.markdown(
        f"""
        <{size} style="font-weight: {weight}; color: {color}; text-align: {align}">
            {text}
        </{size}>
        """,
        unsafe_allow_html=True
    )


# custom html injection for colored divider
def divider(color="#000000"):
    st.markdown(
        f"<hr style='border: 1px solid {color};'>",
        unsafe_allow_html=True
)


# custom html injection for background wth border and color control
def background_band_fill(
    subtitle: str | None = None,
    secondary_color: str = "#FFFFFF",
    text_color: str = "#000000",
    border: bool = False,
    border_color: str = "#000000",
    size="16px"
):
    border_style = f"border: 5px solid {border_color};" if border else ""
    html = f"""
    <div style="
        background: {secondary_color};
        padding: 24px;  
        border-radius: 14px;
        margin-bottom: 24px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        {border_style}
    ">
        {"<p style='color: " + text_color + "; margin-top: 6px; font-size: {size};'>" + subtitle + "</p>" if subtitle else ""}
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


# custom html injection for just border (may delete later)
def background_band_border(
    subtitle,
    border_color: str = "#000000",
    text_color: str = "#000000"
):
    html = f"""
    <div style="
        border: 2px solid {border_color};
        padding: 24px;  
        border-radius: 14px;
        margin-bottom: 24px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    ">
        {"<p style='color: " + text_color + "; margin-top: 6px; font-size: 1.1rem;'>" + subtitle + "</p>" if subtitle else ""}
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

# create paragraphs out of string values, helper function for errors in other html injections
def text_to_paragraphs(text, color):
    return "".join(
        f"<p style='margin:6px 0; font-size:1.05rem; color:{color};'>{line}</p>"
        for line in text.split("\n") if line.strip()
    )

# custom html injection to style the tabs to switch between charts
def tab_styler(primary: str, secondary: str, sectext: str):
    st.markdown(
        f"""
        <style>

        /* outer tabs container */
        div[data-testid="stTabs"] {{
            margin-top: 1.25rem;
        }}

        /* tab list (controls layout) */
        div[data-testid="stTabs"] div[role="tablist"] {{
            display: flex;
            justify-content: center;
            gap: 32px;
            margin: 0 auto;
            border-bottom: none !important;
            box-shadow: none !important;
            overflow: visible !important;
        }}

        /* base (unselected) */
        button[data-baseweb="tab"] {{
            background-color: transparent !important;
            color: {primary} !important;
            font-weight: 700 !important;
            font-size: 1.5rem !important;
            padding: 12px 26px !important;
            border-radius: 999px !important;
            border: 3px solid {primary} !important;
            transition: all 0.15s ease;
        }}

        /* hover */
        button[data-baseweb="tab"]:hover {{
            background-color: {secondary} !important;
            color: {sectext} !important;
        }}

        /* active */
        button[data-baseweb="tab"][aria-selected="true"] {{
            background-color: {primary} !important;
            color: white !important;
            transform: scale(1.25);
        }}

        div[data-testid="stTabs"] div[data-baseweb="tab-border"],
        div[data-testid="stTabs"] div[data-baseweb="tab-highlight"],
        div[data-testid="stTabs"] hr {{
            display: none !important;
        }}

        div[data-testid="stTabs"] div[role="tablist"]::after {{
            display: none !important;
            content: none !important;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


# custom html injection to control the color and style of buttons (navigates to other pages)
def pill_button_styler(
    primary: str,
    secondary: str,
    font_size: str = "1.05rem",
    padding_y: str = "10px",
    border_width: str = "3px",
    scale_active: float = 1.05,
):

    st.markdown(
        f"""
        <style>
        /* base pill button */
        div.stButton > button {{
            background-color: transparent !important;
            color: {primary} !important;
            font-weight: 700 !important;
            font-size: {font_size} !important;
            padding: {padding_y} 0 !important;
            border-radius: 999px !important;
            border: {border_width} solid {primary} !important;
            transition: all 0.15s ease;
            width: 100%;
        }}

        /* hover */
        div.stButton > button:hover {{
            background-color: {secondary} !important;
            color: white !important;
        }}

        /* focus (keyboard nav) */
        div.stButton > button:focus {{
            outline: none !important;
            box-shadow: none !important;
        }}

        /* pressed / active click */
        div.stButton > button:active {{
            transform: scale({scale_active});
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


# same custom injection as before, but safe for sidebar use
def background_band_fill_side(
    subtitle: str | None = None,
    secondary_color: str = "#FFFFFF",
    text_color: str = "#000000",
    border: bool = False,
    border_color: str = "#000000",
):
    border_style = f"border: 5px solid {border_color};" if border else ""
    html = f"""
    <div style="
        background: {secondary_color};
        padding: 24px;  
        border-radius: 14px;
        margin-bottom: 24px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        {border_style}
    ">
        {"<p style='color: " + text_color + "; margin-top: 6px; font-size: 1.1rem;'>" + subtitle + "</p>" if subtitle else ""}
    </div>
    """
    return html


# custom html injection for dataframes in streamlit (may delete later)
def styled_section_df(
    rows,
    header_bg: str = "#003366",
    header_text: str = "#ffffff",
    name_color: str = "#0085CA",
):
    df = pd.DataFrame(rows)[["Variable", "Description", "Type", "Source"]]
    styler = (
        df.style
        .set_table_styles(
            [
                {"selector": "th", "props": [("background-color", header_bg), ("color", header_text)]},
                {"selector": "td", "props": [("font-size", "14px")]},
            ]
        )
        .set_properties(subset=["Variable"], **{"color": name_color, "font-weight": "600"})
    )
    return styler
