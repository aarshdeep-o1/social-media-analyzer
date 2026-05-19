import streamlit as st
from utils.data_loader import load_data, filter_data
from utils.charts import follower_growth_chart, traffic_chart, saves_vs_reach_chart

st.set_page_config(page_title="Follower Tracking", page_icon="👥", layout="wide")
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=Space+Mono:wght@400;700&display=swap');
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
[data-testid="stSidebar"] { background: linear-gradient(180deg, #0f0c29, #302b63, #24243e) !important; }
[data-testid="stSidebar"] * { color: #e0e0e0 !important; }
.kpi-card { background: var(--secondary-background-color); border-radius: 16px; padding: 24px 20px; box-shadow: 0 2px 12px rgba(99,91,255,0.08); border-left: 4px solid #22c55e; text-align: center; margin-bottom: 8px; }
.kpi-label { font-size: 12px; color: var(--text-color); opacity: 0.7; font-weight: 500; text-transform: uppercase; letter-spacing: 0.8px; margin-bottom: 6px; }
.kpi-value { font-family: 'Space Mono', monospace; font-size: 26px; font-weight: 700; color: var(--text-color); }
.page-header { background: linear-gradient(135deg, #059669, #34d399); border-radius: 16px; padding: 28px 32px; margin-bottom: 24px; }
.page-header h2 { color: white !important; font-size: 28px; font-weight: 700; margin: 0; }
.page-header p { color: rgba(255,255,255,0.8); margin: 6px 0 0 0; font-size: 14px; }
#MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='page-header'><h2>👥 Follower Tracking</h2><p>Growth trends, traffic sources aur reach analysis</p></div>", unsafe_allow_html=True)
df = load_data()
st.sidebar.markdown("""<div style='text-align:center;padding:16px 0 8px 0;'><div style='font-size:32px;'>📊</div><div style='font-size:16px;font-weight:700;color:white;margin-top:6px;'>InstaAnalytics</div></div><hr style='border-color:rgba(255,255,255,0.1);'>""", unsafe_allow_html=True)
st.sidebar.markdown("### 🔧 Filters")
media_type = st.sidebar.selectbox("Media Type", ["All","Reel","Photo","Video","Carousel"])
date_range = st.sidebar.date_input("Date Range", [df["upload_date"].min(), df["upload_date"].max()])
filtered = filter_data(df, media_type, date_range)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f"<div class='kpi-card'><div class='kpi-label'>Total Followers Gained</div><div class='kpi-value'>{filtered['followers_gained'].sum():,}</div></div>", unsafe_allow_html=True)
with col2:
    st.markdown(f"<div class='kpi-card' style='border-left-color:#635bff;'><div class='kpi-label'>Avg Per Post</div><div class='kpi-value'>{filtered['followers_gained'].mean():.0f}</div></div>", unsafe_allow_html=True)
with col3:
    st.markdown(f"<div class='kpi-card' style='border-left-color:#f59e0b;'><div class='kpi-label'>Total Reach</div><div class='kpi-value'>{filtered['reach'].sum():,}</div></div>", unsafe_allow_html=True)
with col4:
    st.markdown(f"<div class='kpi-card' style='border-left-color:#ec4899;'><div class='kpi-label'>Total Impressions</div><div class='kpi-value'>{filtered['impressions'].sum():,}</div></div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(follower_growth_chart(filtered), use_container_width=True)
with col2:
    st.plotly_chart(traffic_chart(filtered), use_container_width=True)
st.plotly_chart(saves_vs_reach_chart(filtered), use_container_width=True)
st.markdown("### 📋 Raw Data")
st.dataframe(filtered[["post_id","upload_date","media_type","followers_gained","reach","impressions","traffic_source"]].sort_values("followers_gained", ascending=False).reset_index(drop=True), use_container_width=True, hide_index=True)
