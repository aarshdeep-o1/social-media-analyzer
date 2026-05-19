import plotly.express as px

COLORS = [
    "#635bff",
    "#f59e0b",
    "#22c55e",
    "#ec4899",
    "#06b6d4",
    "#f97316",
    "#8b5cf6",
    "#14b8a6"
]

LAYOUT = dict(
    font=dict(
        family="DM Sans, sans-serif",
        size=13
    ),
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    margin=dict(t=60, b=40, l=20, r=20),
    title=dict(font=dict(size=16))
)


def engagement_chart(df):
    fig = px.bar(
        df,
        x="upload_date",
        y="engagement_rate",
        color="media_type",
        barmode="group",
        title="Daily Engagement Rate (%)",
        color_discrete_sequence=COLORS
    )

    fig.update_layout(**LAYOUT)

    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(gridcolor="rgba(128,128,128,0.15)")

    return fig


def follower_growth_chart(df):
    daily = df.groupby("upload_date")["followers_gained"].sum().reset_index()

    fig = px.area(
        daily,
        x="upload_date",
        y="followers_gained",
        title="Follower Growth Over Time"
    )

    fig.update_traces(
        fill='tozeroy',
        fillcolor='rgba(99,91,255,0.15)',
        line=dict(color="#635bff", width=2)
    )

    fig.update_layout(**LAYOUT)

    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(gridcolor="rgba(128,128,128,0.15)")

    return fig


def media_type_chart(df):
    fig = px.pie(
        df,
        names="media_type",
        values="likes",
        title="Likes by Media Type",
        color_discrete_sequence=COLORS,
        hole=0.45
    )

    fig.update_traces(
        textposition='outside',
        textinfo='percent+label'
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="DM Sans", size=13),
        title=dict(font=dict(size=16)),
        margin=dict(t=60, b=40)
    )

    return fig


def category_chart(df):
    cat = df.groupby("content_category")["engagement_rate"] \
        .mean() \
        .reset_index() \
        .sort_values("engagement_rate", ascending=True)

    fig = px.bar(
        cat,
        x="engagement_rate",
        y="content_category",
        orientation="h",
        title="Avg Engagement Rate by Category",
        color="engagement_rate",
        color_continuous_scale=["#a78bfa", "#635bff"]
    )

    # FIX: Do NOT pass xaxis/yaxis inside update_layout when using **LAYOUT
    # Instead call update_xaxes / update_yaxes separately
    fig.update_layout(
        **LAYOUT,
        coloraxis_showscale=False
    )

    fig.update_xaxes(gridcolor="rgba(128,128,128,0.15)")
    fig.update_yaxes(showgrid=False)

    return fig


def traffic_chart(df):
    fig = px.pie(
        df,
        names="traffic_source",
        values="reach",
        title="Reach by Traffic Source",
        color_discrete_sequence=COLORS,
        hole=0.45
    )

    fig.update_traces(
        textposition='outside',
        textinfo='percent+label'
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="DM Sans", size=13),
        title=dict(font=dict(size=16)),
        margin=dict(t=60, b=40)
    )

    return fig


def hashtag_chart(df):
    fig = px.scatter(
        df,
        x="hashtags_count",
        y="engagement_rate",
        color="media_type",
        title="Hashtags Count vs Engagement Rate",
        color_discrete_sequence=COLORS,
        trendline="ols",
        opacity=0.7
    )

    fig.update_layout(**LAYOUT)

    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(gridcolor="rgba(128,128,128,0.15)")

    return fig


def saves_vs_reach_chart(df):
    fig = px.scatter(
        df,
        x="reach",
        y="saves",
        color="content_category",
        title="Reach vs Saves by Category",
        size="likes",
        color_discrete_sequence=COLORS,
        hover_data=["media_type", "engagement_rate"],
        opacity=0.75
    )

    fig.update_layout(**LAYOUT)

    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(gridcolor="rgba(128,128,128,0.15)")

    return fig