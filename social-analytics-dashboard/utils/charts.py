import plotly.express as px
import streamlit as st

COLORS = ["#635bff","#f59e0b","#22c55e","#ec4899","#06b6d4","#f97316","#8b5cf6","#14b8a6"]

def get_layout():
    is_light = st.session_state.get("theme") == "Light"
    text_color = "#111827" if is_light else "#e0e0e0"
    grid_color = "rgba(0,0,0,0.1)" if is_light else "rgba(128,128,128,0.15)"
    
    return dict(
        font=dict(family="DM Sans, sans-serif", size=13, color=text_color),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=60, b=40, l=20, r=20),
        xaxis=dict(showgrid=False, color=text_color, gridcolor=grid_color),
        yaxis=dict(gridcolor=grid_color, color=text_color),
        title=dict(font=dict(size=16, color=text_color))
    )

def engagement_chart(df):
    fig = px.bar(df, x="upload_date", y="engagement_rate", color="media_type", barmode="group", title="Daily Engagement Rate (%)", color_discrete_sequence=COLORS)
    fig.update_layout(**get_layout())
    return fig

def follower_growth_chart(df):
    daily = df.groupby("upload_date")["followers_gained"].sum().reset_index()
    fig = px.area(daily, x="upload_date", y="followers_gained", title="Follower Growth Over Time")
    fig.update_traces(fill='tozeroy', fillcolor='rgba(99,91,255,0.15)', line=dict(color="#635bff", width=2))
    fig.update_layout(**get_layout())
    return fig

def media_type_chart(df):
    fig = px.pie(df, names="media_type", values="likes", title="Likes by Media Type", color_discrete_sequence=COLORS, hole=0.45)
    fig.update_traces(textposition='outside', textinfo='percent+label')
    layout = get_layout()
    layout["margin"] = dict(t=60, b=40)
    fig.update_layout(**layout)
    return fig

def category_chart(df):
    cat = df.groupby("content_category")["engagement_rate"].mean().reset_index().sort_values("engagement_rate", ascending=True)
    fig = px.bar(cat, x="engagement_rate", y="content_category", orientation="h", title="Avg Engagement Rate by Category", color="engagement_rate", color_continuous_scale=["#a78bfa","#635bff"])
    
    # Fix the multiple values for xaxis error
    fig.update_layout(**get_layout(), coloraxis_showscale=False)
    fig.update_xaxes(gridcolor="rgba(128,128,128,0.15)", showgrid=True)
    fig.update_yaxes(showgrid=False)
    return fig

def traffic_chart(df):
    fig = px.pie(df, names="traffic_source", values="reach", title="Reach by Traffic Source", color_discrete_sequence=COLORS, hole=0.45)
    fig.update_traces(textposition='outside', textinfo='percent+label')
    layout = get_layout()
    layout["margin"] = dict(t=60, b=40)
    fig.update_layout(**layout)
    return fig

def hashtag_chart(df):
    fig = px.scatter(df, x="hashtags_count", y="engagement_rate", color="media_type", title="Hashtags Count vs Engagement Rate", color_discrete_sequence=COLORS, trendline="ols", opacity=0.7)
    fig.update_layout(**get_layout())
    return fig

def saves_vs_reach_chart(df):
    fig = px.scatter(df, x="reach", y="saves", color="content_category", title="Reach vs Saves by Category", size="likes", color_discrete_sequence=COLORS, hover_data=["media_type","engagement_rate"], opacity=0.75)
    fig.update_layout(**get_layout())
    return fig
