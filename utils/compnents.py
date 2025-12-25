import streamlit as st

def colored_metric(label, value, color):
    st.markdown(
        f"""
        <div style="
            border-left: 6px solid {color};
            padding-left: 12px;
            margin-bottom: 12px;
        ">
            <div style="font-size: 14px; color: #6e6e6e;">
                {label}
            </div>
            <div style="font-size: 32px; font-weight: 700; color: {color};">
                {value}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

