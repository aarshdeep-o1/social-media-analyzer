import streamlit as st
from utils.data_loader import load_data
from utils.sidebar import create_sidebar

st.set_page_config(
    page_title="Instagram Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=Space+Mono:wght@400;700&display=swap');
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
[data-testid="stSidebar"] { background: linear-gradient(180deg, #0f0c29, #302b63, #24243e) !important; }
[data-testid="stSidebar"] * { color: #e0e0e0 !important; }
.kpi-card { background: var(--secondary-background-color); border-radius: 16px; padding: 24px 20px; box-shadow: 0 2px 12px rgba(99,91,255,0.08); border-left: 4px solid #635bff; text-align: center; margin-bottom: 8px; transition: transform 0.2s ease; }
.kpi-card:hover { transform: translateY(-3px); }
.kpi-label { font-size: 12px; color: var(--text-color); opacity: 0.7; font-weight: 500; text-transform: uppercase; letter-spacing: 0.8px; margin-bottom: 6px; }
.kpi-value { font-family: 'Space Mono', monospace; font-size: 26px; font-weight: 700; color: var(--text-color); }
.kpi-delta { font-size: 12px; color: #22c55e; margin-top: 6px; font-weight: 600; }
.hero { background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #635bff 100%); border-radius: 20px; padding: 48px 40px; margin-bottom: 32px; }
.hero h1 { font-size: 36px; font-weight: 700; margin-bottom: 8px; color: white !important; }
.hero p { font-size: 16px; color: rgba(255,255,255,0.75); margin-bottom: 0; }
.hero-badge { display: inline-block; background: rgba(255,255,255,0.15); border: 1px solid rgba(255,255,255,0.25); border-radius: 20px; padding: 4px 14px; font-size: 12px; color: white; margin-bottom: 16px; }
.feature-card { background: var(--secondary-background-color); border-radius: 16px; padding: 24px; box-shadow: 0 2px 12px rgba(0,0,0,0.06); border: 1px solid rgba(99,91,255,0.15); transition: all 0.2s ease; }
.feature-card:hover { border-color: #635bff; transform: translateY(-2px); }
.feature-icon { font-size: 32px; margin-bottom: 12px; }
.feature-title { font-size: 16px; font-weight: 700; color: var(--text-color); margin-bottom: 6px; }
.feature-desc { font-size: 13px; color: var(--text-color); opacity: 0.65; line-height: 1.5; }
.section-header { font-size: 22px; font-weight: 700; color: var(--text-color); margin-bottom: 4px; }
.section-sub { font-size: 14px; color: var(--text-color); opacity: 0.6; margin-bottom: 20px; }
.custom-divider { height: 1px; background: linear-gradient(90deg, rgba(99,91,255,0.1), rgba(99,91,255,0.4), rgba(99,91,255,0.1)); margin: 28px 0; }
#MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

create_sidebar()

st.markdown("""
<div class='hero'>
    <div class='hero-badge'>🚀 Live Analytics</div>
    <h1>Instagram Analytics Dashboard</h1>
    <p>Track engagement, follower growth, and content performance — all in one place.</p>
</div>
""", unsafe_allow_html=True)

df = load_data()
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f"<div class='kpi-card'><div class='kpi-label'>Total Posts</div><div class='kpi-value'>{len(df):,}</div><div class='kpi-delta'>▲ 2024 Dataset</div></div>", unsafe_allow_html=True)
with col2:
    st.markdown(f"<div class='kpi-card' style='border-left-color:#f59e0b;'><div class='kpi-label'>Total Likes</div><div class='kpi-value'>{df['likes'].sum():,}</div><div class='kpi-delta'>▲ All media types</div></div>", unsafe_allow_html=True)
with col3:
    st.markdown(f"<div class='kpi-card' style='border-left-color:#22c55e;'><div class='kpi-label'>Followers Gained</div><div class='kpi-value'>{df['followers_gained'].sum():,}</div><div class='kpi-delta'>▲ Organic growth</div></div>", unsafe_allow_html=True)
with col4:
    st.markdown(f"<div class='kpi-card' style='border-left-color:#ec4899;'><div class='kpi-label'>Avg Engagement</div><div class='kpi-value'>{df['engagement_rate'].mean():.2f}%</div><div class='kpi-delta'>▲ Above industry avg</div></div>", unsafe_allow_html=True)

st.markdown("<div class='custom-divider'></div>", unsafe_allow_html=True)
st.markdown("<div class='section-header'>🗂️ Dashboard Pages</div>", unsafe_allow_html=True)
st.markdown("<div class='section-sub'>Select a page from the sidebar to explore</div>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("<div class='feature-card'><div class='feature-icon'>📈</div><div class='feature-title'>Engagement Analytics</div><div class='feature-desc'>Track daily engagement rate, likes, comments, shares and performance by content category.</div></div>", unsafe_allow_html=True)
with col2:
    st.markdown("<div class='feature-card'><div class='feature-icon'>👥</div><div class='feature-title'>Follower Tracking</div><div class='feature-desc'>Monitor follower growth over time, traffic sources and reach vs saves analysis.</div></div>", unsafe_allow_html=True)
with col3:
    st.markdown("<div class='feature-card'><div class='feature-icon'>🔍</div><div class='feature-title'>Hashtag Analysis</div><div class='feature-desc'>Discover optimal hashtag count, engagement correlation and performance breakdown.</div></div>", unsafe_allow_html=True)

st.markdown("<div class='custom-divider'></div>", unsafe_allow_html=True)
st.markdown("<div class='section-header'>⚡ Quick Stats by Media Type</div>", unsafe_allow_html=True)
summary = df.groupby("media_type").agg(Posts=("post_id","count"), Avg_Likes=("likes","mean"), Avg_Reach=("reach","mean"), Avg_Engagement=("engagement_rate","mean"), Avg_Followers=("followers_gained","mean")).round(1).reset_index()
summary.columns = ["Media Type","Posts","Avg Likes","Avg Reach","Avg Engagement (%)","Avg Followers Gained"]
st.dataframe(summary, use_container_width=True, hide_index=True)
