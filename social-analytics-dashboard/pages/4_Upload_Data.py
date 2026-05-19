import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Upload & Analyze", page_icon="📂", layout="wide")
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=Space+Mono:wght@400;700&display=swap');
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
[data-testid="stSidebar"] { background: linear-gradient(180deg, #0f0c29, #302b63, #24243e) !important; }
[data-testid="stSidebar"] * { color: #e0e0e0 !important; }
[data-testid="stSidebarContent"] { padding-top: 1rem !important; }

.kpi-card { background: var(--secondary-background-color); border-radius: 16px; padding: 24px 20px; box-shadow: 0 2px 12px rgba(99,91,255,0.08); border-left: 4px solid #635bff; text-align: center; margin-bottom: 8px; }
.kpi-label { font-size: 12px; color: var(--text-color); opacity: 0.7; font-weight: 500; text-transform: uppercase; letter-spacing: 0.8px; margin-bottom: 6px; }
.kpi-value { font-family: 'Space Mono', monospace; font-size: 26px; font-weight: 700; color: var(--text-color); }

.page-header { background: linear-gradient(135deg, #0ea5e9, #6366f1); border-radius: 16px; padding: 28px 32px; margin-bottom: 24px; }
.page-header h2 { color: white !important; font-size: 28px; font-weight: 700; margin: 0; }
.page-header p { color: rgba(255,255,255,0.8); margin: 6px 0 0 0; font-size: 14px; }

.upload-prompt {
    background: linear-gradient(135deg, rgba(99,91,255,0.08), rgba(99,91,255,0.15));
    border: 2px dashed #635bff;
    border-radius: 16px;
    padding: 28px 32px;
    text-align: center;
    margin-bottom: 24px;
}
.upload-prompt h3 { font-size: 20px; font-weight: 700; color: #635bff; margin-bottom: 8px; }
.upload-prompt p { font-size: 14px; color: var(--text-color); opacity: 0.7; margin: 0; }

.insight-box { background: var(--secondary-background-color); border-radius: 12px; padding: 16px 20px; border-left: 4px solid #635bff; margin-bottom: 12px; }
.insight-title { font-size: 14px; font-weight: 700; color: var(--text-color); margin-bottom: 4px; }
.insight-text { font-size: 13px; color: var(--text-color); opacity: 0.7; }

#MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 8px 0 4px 0;'>
        <div style='font-size:36px;'>📊</div>
        <div style='font-size:16px; font-weight:700; color:white; margin-top:4px;'>InstaAnalytics</div>
        <div style='font-size:11px; color:rgba(255,255,255,0.45); margin-top:2px;'>Dashboard v1.0</div>
    </div>
    <hr style='border-color:rgba(255,255,255,0.1); margin: 10px 0 16px 0;'>
    """, unsafe_allow_html=True)

# Page header
st.markdown("<div class='page-header'><h2>📂 Upload & Analyze</h2><p>Upload any CSV dataset — instant insights & charts generated automatically</p></div>", unsafe_allow_html=True)

COLORS = ["#635bff","#f59e0b","#22c55e","#ec4899","#06b6d4","#f97316","#8b5cf6","#14b8a6"]
LAYOUT = dict(
    font=dict(family="DM Sans, sans-serif", size=13),
    plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
    margin=dict(t=60, b=40, l=20, r=20),
    xaxis=dict(showgrid=False),
    yaxis=dict(gridcolor="rgba(128,128,128,0.15)"),
    title=dict(font=dict(size=16))
)

uploaded_file = st.file_uploader("", type=["csv"], label_visibility="collapsed")

if uploaded_file is None:
    # Upload prompt banner
    st.markdown("""
    <div class='upload-prompt'>
        <h3>📁 Upload your CSV dataset to get started</h3>
        <p>Drag & drop or click Browse files above — auto insights, charts & correlation analysis will be generated instantly</p>
    </div>
    """, unsafe_allow_html=True)

    # Clean professional info cards
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class='kpi-card' style='text-align:left; border-left-color:#635bff;'>
            <div style='font-size:24px; margin-bottom:10px;'>📊</div>
            <div class='kpi-label'>Auto Charts</div>
            <div style='font-size:13px; color:var(--text-color); opacity:0.7; margin-top:6px;'>Time series, histogram, scatter, correlation heatmap — all generated automatically</div>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class='kpi-card' style='text-align:left; border-left-color:#22c55e;'>
            <div style='font-size:24px; margin-bottom:10px;'>💡</div>
            <div class='kpi-label'>Smart Insights</div>
            <div style='font-size:13px; color:var(--text-color); opacity:0.7; margin-top:6px;'>Mean, max, min, std deviation, skewness & missing value detection per column</div>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class='kpi-card' style='text-align:left; border-left-color:#f59e0b;'>
            <div style='font-size:24px; margin-bottom:10px;'>🔍</div>
            <div class='kpi-label'>Custom Charts</div>
            <div style='font-size:13px; color:var(--text-color); opacity:0.7; margin-top:6px;'>Choose any X/Y axis and chart type — bar, line, scatter, box, area, histogram</div>
        </div>""", unsafe_allow_html=True)

else:
    try:
        df = pd.read_csv(uploaded_file)

        # Auto parse date columns
        for col in df.columns:
            if any(x in col.lower() for x in ['date','time','day','month','year']):
                try:
                    df[col] = pd.to_datetime(df[col], infer_datetime_format=True)
                except:
                    pass

        numeric_cols = df.select_dtypes(include='number').columns.tolist()
        cat_cols = df.select_dtypes(include='object').columns.tolist()
        date_cols = [c for c in df.columns if pd.api.types.is_datetime64_any_dtype(df[c])]
        missing = df.isnull().sum().sum()

        st.success(f"✅ **{uploaded_file.name}** loaded — {len(df):,} rows, {len(df.columns)} columns")
        st.markdown("---")

        # KPI Cards
        st.markdown("### 📊 Dataset Overview")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"<div class='kpi-card'><div class='kpi-label'>Total Rows</div><div class='kpi-value'>{len(df):,}</div></div>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<div class='kpi-card' style='border-left-color:#f59e0b;'><div class='kpi-label'>Total Columns</div><div class='kpi-value'>{len(df.columns)}</div></div>", unsafe_allow_html=True)
        with col3:
            st.markdown(f"<div class='kpi-card' style='border-left-color:#22c55e;'><div class='kpi-label'>Numeric Columns</div><div class='kpi-value'>{len(numeric_cols)}</div></div>", unsafe_allow_html=True)
        with col4:
            c = "#ec4899" if missing > 0 else "#22c55e"
            st.markdown(f"<div class='kpi-card' style='border-left-color:{c};'><div class='kpi-label'>Missing Values</div><div class='kpi-value'>{missing}</div></div>", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### 👀 Data Preview")
        st.dataframe(df.head(10), use_container_width=True, hide_index=True)
        st.markdown("---")

        # Smart Insights
        if numeric_cols:
            st.markdown("### 💡 Column Insights")
            for col in numeric_cols[:6]:
                skew = df[col].skew()
                skew_text = "Right skewed" if skew > 1 else "Left skewed" if skew < -1 else "Normal distribution"
                st.markdown(f"""
                <div class='insight-box' style='border-left-color:#635bff;'>
                    <div class='insight-title'>📌 {col}</div>
                    <div class='insight-text'>
                        Mean: <b>{df[col].mean():,.2f}</b> &nbsp;|&nbsp;
                        Max: <b>{df[col].max():,.2f}</b> &nbsp;|&nbsp;
                        Min: <b>{df[col].min():,.2f}</b> &nbsp;|&nbsp;
                        Std: <b>{df[col].std():,.2f}</b> &nbsp;|&nbsp;
                        {skew_text}
                    </div>
                </div>""", unsafe_allow_html=True)

        for col in cat_cols[:3]:
            top_val = df[col].value_counts().index[0]
            top_pct = df[col].value_counts().iloc[0] / len(df) * 100
            st.markdown(f"""
            <div class='insight-box' style='border-left-color:#22c55e;'>
                <div class='insight-title'>🏷️ {col}</div>
                <div class='insight-text'>
                    {df[col].nunique()} unique values &nbsp;|&nbsp; Most frequent: <b>{top_val}</b> ({top_pct:.1f}%)
                </div>
            </div>""", unsafe_allow_html=True)

        if missing > 0:
            mc = df.isnull().sum()
            mc = mc[mc > 0]
            st.markdown(f"<div class='insight-box' style='border-left-color:#f59e0b;'><div class='insight-title'>⚠️ Missing Values</div><div class='insight-text'>{', '.join([f'{c}: {v}' for c,v in mc.items()])}</div></div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='insight-box' style='border-left-color:#22c55e;'><div class='insight-title'>✅ Clean Dataset</div><div class='insight-text'>No missing values detected.</div></div>", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### 📈 Auto Charts")

        # Time series
        if date_cols and numeric_cols:
            try:
                fig = px.line(df.sort_values(date_cols[0]), x=date_cols[0], y=numeric_cols[0],
                              title=f"{numeric_cols[0]} Over Time", color_discrete_sequence=COLORS)
                fig.update_layout(**LAYOUT)
                st.plotly_chart(fig, use_container_width=True)
            except: pass

        # Histogram + Scatter
        if len(numeric_cols) >= 2:
            c1, c2 = st.columns(2)
            with c1:
                fig2 = px.histogram(df, x=numeric_cols[0], title=f"Distribution: {numeric_cols[0]}", color_discrete_sequence=["#635bff"])
                fig2.update_layout(**LAYOUT)
                st.plotly_chart(fig2, use_container_width=True)
            with c2:
                fig3 = px.scatter(df, x=numeric_cols[0], y=numeric_cols[1],
                                  title=f"{numeric_cols[0]} vs {numeric_cols[1]}",
                                  color_discrete_sequence=["#f59e0b"], opacity=0.7)
                fig3.update_layout(**LAYOUT)
                st.plotly_chart(fig3, use_container_width=True)

        # Correlation heatmap
        if len(numeric_cols) >= 3:
            corr = df[numeric_cols[:8]].corr().round(2)
            fig_c = px.imshow(corr, title="Correlation Heatmap",
                              color_continuous_scale=["#f59e0b","white","#635bff"],
                              text_auto=True, aspect="auto")
            fig_c.update_layout(paper_bgcolor="rgba(0,0,0,0)", font=dict(family="DM Sans"), title=dict(font=dict(size=16)), margin=dict(t=60,b=40))
            st.plotly_chart(fig_c, use_container_width=True)

        # Category pie
        if cat_cols:
            best_cat = next((c for c in cat_cols if 2 <= df[c].nunique() <= 15), None)
            if best_cat:
                c1, c2 = st.columns(2)
                with c1:
                    fig4 = px.pie(df, names=best_cat, title=f"Breakdown by {best_cat}",
                                  color_discrete_sequence=COLORS, hole=0.4)
                    fig4.update_layout(paper_bgcolor="rgba(0,0,0,0)", font=dict(family="DM Sans"), title=dict(font=dict(size=16)), margin=dict(t=60,b=40))
                    st.plotly_chart(fig4, use_container_width=True)
                with c2:
                    if numeric_cols:
                        best_cat2 = next((c for c in cat_cols if 2 <= df[c].nunique() <= 10), None)
                        if best_cat2:
                            fig5 = px.box(df, x=best_cat2, y=numeric_cols[0], color=best_cat2,
                                          title=f"{numeric_cols[0]} by {best_cat2}",
                                          color_discrete_sequence=COLORS)
                            fig5.update_layout(**LAYOUT)
                            st.plotly_chart(fig5, use_container_width=True)

        st.markdown("---")

        # Custom Chart Builder
        st.markdown("### 🔍 Custom Chart Builder")
        cc1, cc2, cc3 = st.columns(3)
        with cc1:
            col_x = st.selectbox("X-axis", df.columns.tolist())
        with cc2:
            col_y = st.selectbox("Y-axis", numeric_cols if numeric_cols else df.columns.tolist())
        with cc3:
            chart_type = st.selectbox("Chart Type", ["Bar","Line","Scatter","Histogram","Box","Area"])

        color_by = st.selectbox("Color by (optional)", ["None"] + cat_cols)
        color_col = None if color_by == "None" else color_by

        if st.button("📊 Generate Chart", type="primary"):
            try:
                kwargs = dict(title=f"{col_y} by {col_x}", color_discrete_sequence=COLORS)
                if color_col: kwargs["color"] = color_col
                if chart_type == "Bar": fig = px.bar(df, x=col_x, y=col_y, **kwargs)
                elif chart_type == "Line": fig = px.line(df, x=col_x, y=col_y, **kwargs)
                elif chart_type == "Scatter": fig = px.scatter(df, x=col_x, y=col_y, **kwargs, opacity=0.7)
                elif chart_type == "Histogram": fig = px.histogram(df, x=col_x, **kwargs)
                elif chart_type == "Box": fig = px.box(df, x=col_x, y=col_y, **kwargs)
                else: fig = px.area(df, x=col_x, y=col_y, **kwargs)
                fig.update_layout(**LAYOUT)
                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error(f"Chart error: {e}")

        st.markdown("---")
        st.markdown("### 📋 Full Dataset")
        st.dataframe(df, use_container_width=True, hide_index=True)

        st.download_button(
            label="⬇️ Download Processed CSV",
            data=df.to_csv(index=False).encode('utf-8'),
            file_name=f"processed_{uploaded_file.name}",
            mime='text/csv'
        )

    except Exception as e:
        st.error(f"❌ Could not read file: {str(e)}")
        st.info("Please ensure the file is in valid CSV format.")
