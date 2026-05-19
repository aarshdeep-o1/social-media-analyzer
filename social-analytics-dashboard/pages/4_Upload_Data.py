import streamlit as st
import pandas as pd
import plotly.express as px
from utils.sidebar import create_sidebar
from utils.charts import get_layout, COLORS

st.set_page_config(page_title="Upload & Analyze", page_icon="📂", layout="wide")
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=Space+Mono:wght@400;700&display=swap');
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
[data-testid="stSidebar"] { background: linear-gradient(180deg, #0f0c29, #302b63, #24243e) !important; }
[data-testid="stSidebar"] * { color: #e0e0e0 !important; }
.kpi-card { background: var(--secondary-background-color); border-radius: 16px; padding: 24px 20px; box-shadow: 0 2px 12px rgba(99,91,255,0.08); border-left: 4px solid #635bff; text-align: center; margin-bottom: 8px; }
.kpi-label { font-size: 12px; color: var(--text-color); opacity: 0.7; font-weight: 500; text-transform: uppercase; letter-spacing: 0.8px; margin-bottom: 6px; }
.kpi-value { font-family: 'Space Mono', monospace; font-size: 26px; font-weight: 700; color: var(--text-color); }
.page-header { background: linear-gradient(135deg, #0ea5e9, #6366f1); border-radius: 16px; padding: 28px 32px; margin-bottom: 24px; }
.page-header h2 { color: white !important; font-size: 28px; font-weight: 700; margin: 0; }
.page-header p { color: rgba(255,255,255,0.8); margin: 6px 0 0 0; font-size: 14px; }
.insight-box { background: var(--secondary-background-color); border-radius: 12px; padding: 16px 20px; border-left: 4px solid #635bff; margin-bottom: 12px; }
.insight-title { font-size: 14px; font-weight: 700; color: var(--text-color); margin-bottom: 4px; }
.insight-text { font-size: 13px; color: var(--text-color); opacity: 0.7; }
.insight-good { border-left-color: #22c55e !important; }
.insight-warn { border-left-color: #f59e0b !important; }
.insight-info { border-left-color: #06b6d4 !important; }
#MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='page-header'><h2>📂 Upload & Analyze</h2><p>Apna koi bhi CSV upload karo — dashboard turant analyze karega!</p></div>", unsafe_allow_html=True)

create_sidebar()

# Layout is imported from utils.charts

uploaded_file = st.file_uploader("📁 CSV file yahan upload karo (koi bhi dataset)", type=["csv"])

if uploaded_file is not None:
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

        st.success(f"✅ **{uploaded_file.name}** uploaded successfully! — {len(df):,} rows, {len(df.columns)} columns")
        st.markdown("---")

        # ── Preview ───────────────────────────────────────────────────────────
        st.markdown("### 👀 Dataset Preview")
        st.dataframe(df.head(10), use_container_width=True, hide_index=True)
        st.markdown("---")

        # ── KPI Cards ─────────────────────────────────────────────────────────
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

        # ── Smart Auto Insights ───────────────────────────────────────────────
        st.markdown("### 💡 Smart Auto Insights")

        # Numeric stats
        for col in numeric_cols[:6]:
            mean_val = df[col].mean()
            max_val = df[col].max()
            min_val = df[col].min()
            std_val = df[col].std()
            skew = df[col].skew()
            skew_text = "Right skewed (outliers on high side)" if skew > 1 else "Left skewed (outliers on low side)" if skew < -1 else "Normally distributed"
            st.markdown(f"""
            <div class='insight-box insight-info'>
                <div class='insight-title'>📌 {col}</div>
                <div class='insight-text'>
                    Avg: <b>{mean_val:,.2f}</b> &nbsp;|&nbsp; Max: <b>{max_val:,.2f}</b> &nbsp;|&nbsp;
                    Min: <b>{min_val:,.2f}</b> &nbsp;|&nbsp; Std Dev: <b>{std_val:,.2f}</b> &nbsp;|&nbsp; {skew_text}
                </div>
            </div>""", unsafe_allow_html=True)

        # Categorical insights
        for col in cat_cols[:3]:
            top_val = df[col].value_counts().index[0]
            top_pct = df[col].value_counts().iloc[0] / len(df) * 100
            unique_count = df[col].nunique()
            st.markdown(f"""
            <div class='insight-box insight-good'>
                <div class='insight-title'>🏷️ {col}</div>
                <div class='insight-text'>
                    {unique_count} unique values &nbsp;|&nbsp; Most common: <b>{top_val}</b> ({top_pct:.1f}% of data)
                </div>
            </div>""", unsafe_allow_html=True)

        # Missing values insight
        if missing > 0:
            missing_cols = df.isnull().sum()
            missing_cols = missing_cols[missing_cols > 0]
            st.markdown(f"""
            <div class='insight-box insight-warn'>
                <div class='insight-title'>⚠️ Missing Values Detected</div>
                <div class='insight-text'>
                    {', '.join([f'{c}: {v}' for c,v in missing_cols.items()])}
                </div>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown("<div class='insight-box insight-good'><div class='insight-title'>✅ No Missing Values</div><div class='insight-text'>Dataset is clean — koi bhi missing values nahi hain!</div></div>", unsafe_allow_html=True)

        st.markdown("---")

        # ── Auto Charts ───────────────────────────────────────────────────────
        st.markdown("### 📈 Auto Charts")

        # Time series
        if date_cols and numeric_cols:
            try:
                fig = px.line(df.sort_values(date_cols[0]), x=date_cols[0], y=numeric_cols[0],
                              title=f"{numeric_cols[0]} Over Time", color_discrete_sequence=COLORS)
                fig.update_layout(**get_layout())
                st.plotly_chart(fig, use_container_width=True)
            except:
                pass

        # Histogram + Scatter
        if len(numeric_cols) >= 2:
            c1, c2 = st.columns(2)
            with c1:
                fig2 = px.histogram(df, x=numeric_cols[0], title=f"Distribution: {numeric_cols[0]}", color_discrete_sequence=["#635bff"])
                fig2.update_layout(**get_layout())
                st.plotly_chart(fig2, use_container_width=True)
            with c2:
                y_idx = 1 if len(numeric_cols) > 1 else 0
                fig3 = px.scatter(df, x=numeric_cols[0], y=numeric_cols[y_idx],
                                  title=f"{numeric_cols[0]} vs {numeric_cols[y_idx]}",
                                  color_discrete_sequence=["#f59e0b"], opacity=0.7)
                fig3.update_layout(**get_layout())
                st.plotly_chart(fig3, use_container_width=True)

        # Correlation heatmap
        if len(numeric_cols) >= 3:
            import plotly.figure_factory as ff
            corr = df[numeric_cols[:8]].corr().round(2)
            fig_corr = px.imshow(corr, title="Correlation Heatmap",
                                 color_continuous_scale=["#f59e0b","white","#635bff"],
                                 text_auto=True, aspect="auto")
            fig_corr.update_layout(paper_bgcolor="rgba(0,0,0,0)", font=dict(family="DM Sans"), title=dict(font=dict(size=16)), margin=dict(t=60,b=40))
            st.plotly_chart(fig_corr, use_container_width=True)

        # Category pie
        if cat_cols:
            best_cat = next((c for c in cat_cols if 2 <= df[c].nunique() <= 15), None)
            if best_cat:
                fig4 = px.pie(df, names=best_cat, title=f"Breakdown by {best_cat}",
                              color_discrete_sequence=COLORS, hole=0.4)
                fig4.update_layout(paper_bgcolor="rgba(0,0,0,0)", font=dict(family="DM Sans"), title=dict(font=dict(size=16)), margin=dict(t=60,b=40))
                st.plotly_chart(fig4, use_container_width=True)

        # Box plot
        if numeric_cols and cat_cols:
            best_cat = next((c for c in cat_cols if 2 <= df[c].nunique() <= 10), None)
            if best_cat:
                fig5 = px.box(df, x=best_cat, y=numeric_cols[0], color=best_cat,
                              title=f"{numeric_cols[0]} Distribution by {best_cat}",
                              color_discrete_sequence=COLORS)
                fig5.update_layout(**get_layout())
                st.plotly_chart(fig5, use_container_width=True)

        st.markdown("---")

        # ── Custom Chart Builder ──────────────────────────────────────────────
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
                kwargs = dict(x=col_x, y=col_y, title=f"{col_y} by {col_x}", color_discrete_sequence=COLORS)
                if color_col:
                    kwargs["color"] = color_col
                if chart_type == "Bar":
                    fig = px.bar(df, **kwargs)
                elif chart_type == "Line":
                    fig = px.line(df, **kwargs)
                elif chart_type == "Scatter":
                    fig = px.scatter(df, **kwargs, opacity=0.7)
                elif chart_type == "Histogram":
                    fig = px.histogram(df, x=col_x, title=f"Distribution of {col_x}", color_discrete_sequence=COLORS)
                elif chart_type == "Box":
                    fig = px.box(df, **kwargs)
                else:
                    fig = px.area(df, **kwargs)
                fig.update_layout(**get_layout())
                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error(f"Chart error: {e} — Try different columns!")

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
        st.error(f"❌ File error: {str(e)}")
        st.info("💡 Make sure file proper CSV format mein ho!")

else:
    # Check if we should show toast
    if 'upload_toast_shown' not in st.session_state:
        st.toast("👋 Welcome! Please upload your dataset to begin analysis.", icon="📂")
        st.session_state.upload_toast_shown = True

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
    <div style='text-align: center; padding: 50px 20px; background: var(--secondary-background-color); border-radius: 16px; border: 2px dashed rgba(99,91,255,0.3);'>
        <div style='font-size: 56px; margin-bottom: 16px;'>📂</div>
        <h3 style='margin: 0; color: var(--text-color); font-weight: 700;'>Waiting for your dataset</h3>
        <p style='color: var(--text-color); opacity: 0.7; margin-top: 12px; font-size: 16px; max-width: 500px; margin-left: auto; margin-right: auto;'>
            Drag and drop your CSV file above to unlock the auto-analysis dashboard. You'll instantly get smart KPIs, distribution charts, correlation heatmaps, and a custom chart builder.
        </p>
    </div>
    """, unsafe_allow_html=True)
