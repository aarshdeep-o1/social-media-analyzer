import streamlit as st
import pandas as pd
from utils.data_loader import load_data, filter_data
from utils.charts import hashtag_chart

st.set_page_config(page_title="Hashtag Analysis", page_icon="🔍", layout="wide")
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=Space+Mono:wght@400;700&display=swap');
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }

[data-testid="stSidebar"] { background: linear-gradient(180deg, #0f0c29, #302b63, #24243e) !important; }
[data-testid="stSidebar"] * { color: #e0e0e0 !important; }

/* Logo upar, nav neeche */
[data-testid="stSidebarNav"] { margin-top: 90px !important; }
.sidebar-logo {
    position: absolute; top: 16px; left: 0; right: 0;
    text-align: center; z-index: 10;
}
.sidebar-logo .icon { font-size: 36px; line-height: 1; }
.sidebar-logo .name { font-size: 16px; font-weight: 700; color: white; margin-top: 6px; }

.kpi-card { background: var(--secondary-background-color); border-radius: 16px; padding: 24px 20px; box-shadow: 0 2px 12px rgba(99,91,255,0.08); border-left: 4px solid #f59e0b; text-align: center; margin-bottom: 8px; }
.kpi-label { font-size: 12px; color: var(--text-color); opacity: 0.7; font-weight: 500; text-transform: uppercase; letter-spacing: 0.8px; margin-bottom: 6px; }
.kpi-value { font-family: 'Space Mono', monospace; font-size: 26px; font-weight: 700; color: var(--text-color); }
.page-header { background: linear-gradient(135deg, #d97706, #fbbf24); border-radius: 16px; padding: 28px 32px; margin-bottom: 24px; }
.page-header h2 { color: white !important; font-size: 28px; font-weight: 700; margin: 0; }
.page-header p { color: rgba(255,255,255,0.8); margin: 6px 0 0 0; font-size: 14px; }
#MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# SIDEBAR
with st.sidebar:
    st.markdown("""
    <div class='sidebar-logo'>
        <div class='icon'>📊</div>
        <div class='name'>InstaAnalytics</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("### 🔧 Filters")
    df = load_data()
    media_type = st.selectbox("Media Type", ["All", "Reel", "Photo", "Video", "Carousel"])
    date_range = st.date_input("Date Range", [df["upload_date"].min(), df["upload_date"].max()])

st.markdown("<div class='page-header'><h2>🔍 Hashtag Analysis</h2><p>Optimal hashtag count aur engagement correlation analysis</p></div>", unsafe_allow_html=True)

filtered = filter_data(df, media_type, date_range)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f"<div class='kpi-card'><div class='kpi-label'>Avg Hashtags/Post</div><div class='kpi-value'>{filtered['hashtags_count'].mean():.1f}</div></div>", unsafe_allow_html=True)
with col2:
    st.markdown(f"<div class='kpi-card' style='border-left-color:#635bff;'><div class='kpi-label'>Max Hashtags</div><div class='kpi-value'>{filtered['hashtags_count'].max()}</div></div>", unsafe_allow_html=True)
with col3:
    st.markdown(f"<div class='kpi-card' style='border-left-color:#22c55e;'><div class='kpi-label'>Avg Engagement</div><div class='kpi-value'>{filtered['engagement_rate'].mean():.2f}%</div></div>", unsafe_allow_html=True)
with col4:
    st.markdown(f"<div class='kpi-card' style='border-left-color:#ec4899;'><div class='kpi-label'>Posts Analyzed</div><div class='kpi-value'>{len(filtered):,}</div></div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.plotly_chart(hashtag_chart(filtered), use_container_width=True)

st.markdown("### 📊 Hashtag Count Breakdown")
filtered = filtered.copy()
filtered["hashtag_range"] = pd.cut(
    filtered["hashtags_count"],
    bins=[0, 5, 10, 15, 20, 30],
    labels=["1-5", "6-10", "11-15", "16-20", "21-30"]
)
summary = filtered.groupby("hashtag_range", observed=True).agg(
    avg_engagement=("engagement_rate", "mean"),
    avg_likes=("likes", "mean"),
    total_posts=("post_id", "count")
).reset_index()
summary.columns = ["Hashtag Range", "Avg Engagement (%)", "Avg Likes", "Total Posts"]
summary["Avg Engagement (%)"] = summary["Avg Engagement (%)"].round(2)
summary["Avg Likes"] = summary["Avg Likes"].round(0).astype(int)
st.dataframe(summary, use_container_width=True, hide_index=True)

st.markdown("### 📋 Raw Data")
st.dataframe(
    filtered[["post_id", "upload_date", "media_type", "hashtags_count", "engagement_rate", "likes", "content_category"]]
    .sort_values("engagement_rate", ascending=False).reset_index(drop=True),
    use_container_width=True, hide_index=True
)