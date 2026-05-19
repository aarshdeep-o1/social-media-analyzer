import pandas as pd
import streamlit as st
import os

@st.cache_data
def load_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "../data/Instagram_Analytics.csv")
    df = pd.read_csv(file_path, parse_dates=["upload_date"])
    return df

def filter_data(df, media_type=None, date_range=None):
    if media_type and media_type != "All":
        df = df[df["media_type"] == media_type]
    if date_range and len(date_range) == 2:
        start = pd.Timestamp(date_range[0])
        end = pd.Timestamp(date_range[1])
        df = df[(df["upload_date"] >= start) & (df["upload_date"] <= end)]
    return df
