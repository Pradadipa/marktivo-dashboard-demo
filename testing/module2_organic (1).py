"""
MODULE 2: ORGANIC ARCHITECTURE (The Brand Terminal)
Mission: Measure Brand Resonance, Community Loyalty, and Traffic Contribution.
Platforms: Instagram, TikTok, YouTube, LinkedIn

CSS: assets/module2_organic.css (loaded via load_module2_css())
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import random

# ============================================================
# 1. DARK MODE & THEME CONFIGURATION
# ============================================================

DARK_BG = "#0E1117"
CARD_BG = "#1B1F2B"
CARD_BORDER = "#2D3348"
NEON_BLUE = "#00D4FF"
NEON_GREEN = "#00FF88"
NEON_PURPLE = "#A855F7"
NEON_ORANGE = "#FF6B35"
NEON_RED = "#FF3B5C"
NEON_YELLOW = "#FFD700"
TEXT_PRIMARY = "#FFFFFF"
TEXT_SECONDARY = "#8892A0"
TEXT_MUTED = "#5A6577"

# Platform Colors
PLATFORM_COLORS = {
    "Instagram": "#E1306C",
    "TikTok": "#00F2EA",
    "YouTube": "#FF0000",
    "LinkedIn": "#0A66C2"
}

PLATFORM_ICONS = {
    "Instagram": "📸",
    "TikTok": "🎵",
    "YouTube": "🎬",
    "LinkedIn": "💼"
}


def load_module2_css():
    """Load Module 2 CSS from external file in assets/ folder."""
    import os
    css_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'module2_organic.css')
    try:
        with open(css_path) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        # Fallback: try relative path from working directory
        try:
            with open('assets/module2_organic.css') as f:
                st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
        except FileNotFoundError:
            st.warning("⚠️ CSS file not found: assets/module2_organic.css")


# ============================================================
# 2. DUMMY DATA GENERATOR
# ============================================================

@st.cache_data
def generate_organic_data(days=30):
    """
    Generate comprehensive dummy data for all 4 platforms.
    Data includes: followers, impressions, likes, comments, shares,
    saves, link_clicks, profile_visits, posts_published, views.
    """
    np.random.seed(42)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    dates = pd.date_range(start=start_date, end=end_date, freq='D')

    platforms_config = {
        "Instagram": {
            "base_followers": 45200,
            "daily_growth_range": (50, 250),
            "base_impressions": (15000, 35000),
            "engagement_multiplier": 0.065,
            "posts_per_week": 5,
            "base_views": (8000, 25000),
        },
        "TikTok": {
            "base_followers": 28500,
            "daily_growth_range": (80, 400),
            "base_impressions": (25000, 80000),
            "engagement_multiplier": 0.08,
            "posts_per_week": 4,
            "base_views": (20000, 100000),
        },
        "YouTube": {
            "base_followers": 12800,
            "daily_growth_range": (10, 80),
            "base_impressions": (5000, 20000),
            "engagement_multiplier": 0.045,
            "posts_per_week": 2,
            "base_views": (3000, 15000),
        },
        "LinkedIn": {
            "base_followers": 8900,
            "daily_growth_range": (5, 40),
            "base_impressions": (3000, 12000),
            "engagement_multiplier": 0.055,
            "posts_per_week": 3,
            "base_views": (2000, 8000),
        }
    }

    all_data = []

    for platform, config in platforms_config.items():
        followers = config["base_followers"]

        for i, date in enumerate(dates):
            # Follower growth (with some variance)
            daily_growth = np.random.randint(*config["daily_growth_range"])
            # Occasional dips (unfollows)
            if np.random.random() < 0.15:
                daily_growth = -np.random.randint(10, 50)
            followers += daily_growth

            # Impressions
            impressions = np.random.randint(*config["base_impressions"])
            # Weekend boost
            if date.weekday() >= 5:
                impressions = int(impressions * 1.2)

            # Engagement based on impressions
            em = config["engagement_multiplier"]
            likes = int(impressions * em * np.random.uniform(0.6, 1.4))
            comments = int(likes * np.random.uniform(0.05, 0.15))
            shares = int(likes * np.random.uniform(0.03, 0.10))
            saves = int(likes * np.random.uniform(0.08, 0.20))

            # Traffic metrics
            profile_visits = int(impressions * np.random.uniform(0.02, 0.06))
            link_clicks = int(profile_visits * np.random.uniform(0.10, 0.30))

            # Views (video views)
            views = np.random.randint(*config["base_views"])

            # Posts published (not every day)
            posts_goal_weekly = config["posts_per_week"]
            posts_published = 1 if np.random.random() < (posts_goal_weekly / 7) else 0

            all_data.append({
                "date": date,
                "platform": platform,
                "followers": followers,
                "follower_growth": daily_growth,
                "impressions": impressions,
                "likes": likes,
                "comments": comments,
                "shares": shares,
                "saves": saves,
                "views": views,
                "profile_visits": profile_visits,
                "link_clicks": link_clicks,
                "posts_published": posts_published,
                "posts_goal_weekly": posts_goal_weekly,
            })

    df = pd.DataFrame(all_data)

    # Calculate derived metrics
    df["engagement_rate"] = (
        (df["likes"] + df["comments"] + df["shares"]) / df["impressions"] * 100
    )
    df["share_of_voice"] = (
        (df["saves"] + df["shares"]) / df["impressions"] * 100
    )
    df["profile_conversion_rate"] = (
        df["link_clicks"] / df["profile_visits"] * 100
    )

    return df


@st.cache_data
def generate_content_library(num_posts=48):
    """
    Generate dummy content library data (individual posts).
    Each post has: title, platform, type, views, likes, comments, 
    shares, saves, link_clicks, date.
    """
    np.random.seed(123)

    content_types = {
        "Instagram": ["Reel", "Story", "Carousel", "Feed Post"],
        "TikTok": ["Short Video", "Duet", "Stitch"],
        "YouTube": ["Short", "Long Video", "Live"],
        "LinkedIn": ["Article", "Post", "Document"],
    }

    post_titles = [
        "Behind the Scenes: How We Build Products",
        "5 Tips for Better Engagement",
        "Customer Success Story: Brand X",
        "Weekly Motivation Monday",
        "Product Launch Teaser",
        "Q&A Session with the Team",
        "Industry Trend Breakdown",
        "Day in the Life at Office",
        "Tutorial: Getting Started Guide",
        "Community Spotlight Feature",
        "New Feature Announcement",
        "Weekend Vibes & Culture",
        "Expert Interview Series Ep.1",
        "Before vs After Transformation",
        "Myth Busters: Common Mistakes",
        "Flash Sale Announcement",
        "User Generated Content Reshare",
        "Infographic: Key Statistics",
        "Team Celebration Moment",
        "Throwback Thursday Classic",
        "How-to: Advanced Tips & Tricks",
        "Live Q&A Recap Highlights",
        "Partner Collaboration Post",
        "Seasonal Campaign Launch",
        "Data Report: Monthly Insights",
        "Sneak Peek: Upcoming Release",
        "Challenge: Join the Trend",
        "Thank You 10K Followers!",
        "Case Study: ROI Results",
        "Friday Fun: Memes & Laughs",
        "CEO Interview: Vision 2025",
        "Customer Review Compilation",
        "Quick Hack: Productivity Tip",
        "Year in Review Highlights",
        "Unboxing New Product Line",
        "Top 10 FAQs Answered",
        "Workshop Recap: Key Takeaways",
        "Brand Story: Our Origin",
        "Weekly Roundup: Best Moments",
        "Poll Results: What You Told Us",
        "Collaboration Announcement",
        "Event Highlights Montage",
        "Pro Tips from Our Experts",
        "Behind the Brand: Team Intro",
        "Trend Alert: What's Next",
        "Success Metrics: This Month",
        "Holiday Special Campaign",
        "Milestone: 50K Followers!",
    ]

    posts = []
    for i in range(num_posts):
        platform = random.choice(list(content_types.keys()))
        content_type = random.choice(content_types[platform])
        days_ago = random.randint(0, 29)
        post_date = datetime.now() - timedelta(days=days_ago)

        views = np.random.randint(500, 150000)
        likes = int(views * np.random.uniform(0.03, 0.12))
        comments = int(likes * np.random.uniform(0.05, 0.20))
        shares = int(likes * np.random.uniform(0.02, 0.15))
        saves = int(likes * np.random.uniform(0.05, 0.25))
        link_clicks = int(views * np.random.uniform(0.005, 0.03))

        # Use modulo to cycle through titles if num_posts > len(post_titles)
        title = post_titles[i % len(post_titles)]

        posts.append({
            "post_id": f"POST-{i+1:03d}",
            "title": title,
            "platform": platform,
            "content_type": content_type,
            "date": post_date.strftime("%Y-%m-%d"),
            "views": views,
            "likes": likes,
            "comments": comments,
            "shares": shares,
            "saves": saves,
            "link_clicks": link_clicks,
            "virality_score": round((shares + saves) / max(views, 1) * 100, 2),
            "conversion_score": round(link_clicks / max(views, 1) * 100, 2),
        })

    return pd.DataFrame(posts)


# ============================================================
# 3. COMPONENT RENDERERS
# ============================================================

def render_cross_channel_pulse(df):
    """
    View Mode 1: Cross-Channel Pulse — Ticker Tape
    Shows net follower growth (+/-) across all platforms.
    """
    st.markdown('<div class="section-header">📡 CROSS-CHANNEL PULSE — FOLLOWER GROWTH</div>', unsafe_allow_html=True)

    cols = st.columns(4)

    for idx, platform in enumerate(["Instagram", "TikTok", "YouTube", "LinkedIn"]):
        platform_data = df[df["platform"] == platform]
        current_followers = platform_data["followers"].iloc[-1]
        total_growth = platform_data["follower_growth"].sum()
        growth_pct = (total_growth / (current_followers - total_growth)) * 100 if (current_followers - total_growth) > 0 else 0
        avg_daily_growth = platform_data["follower_growth"].mean()

        # Determine growth class
        is_positive = total_growth >= 0
        growth_class = "ticker-growth-positive" if is_positive else "ticker-growth-negative"
        growth_arrow = "▲" if is_positive else "▼"
        color = PLATFORM_COLORS[platform]

        with cols[idx]:
            st.markdown(f"""
            <div class="ticker-card" style="border-top: 3px solid {color};">
                <div class="ticker-platform">{PLATFORM_ICONS[platform]} {platform}</div>
                <div class="ticker-followers">{current_followers:,}</div>
                <div class="{growth_class}">
                    {growth_arrow} {abs(total_growth):,} ({growth_pct:+.1f}%)
                </div>
                <div style="font-size: 11px; color: #5A6577; margin-top: 4px;">
                    Avg {avg_daily_growth:+.0f}/day · 30d
                </div>
            </div>
            """, unsafe_allow_html=True)


def render_north_star_ribbon(df):
    """
    North Star Ribbon — Top KPI Metrics Row
    Engagement Rate, Share of Voice, Profile CVR, Consistency Score
    """
    st.markdown('<div class="section-header">⭐ NORTH STAR METRICS — ORGANIC HEALTH</div>', unsafe_allow_html=True)

    # Calculate aggregated metrics
    total_likes = df["likes"].sum()
    total_comments = df["comments"].sum()
    total_shares = df["shares"].sum()
    total_saves = df["saves"].sum()
    total_impressions = df["impressions"].sum()
    total_link_clicks = df["link_clicks"].sum()
    total_profile_visits = df["profile_visits"].sum()
    total_posts = df["posts_published"].sum()
    # Assume total goal = sum of daily goals
    # posts_goal_weekly varies by platform, approximate: total_days * avg_posts_per_day
    total_days = df["date"].nunique()
    total_posts_goal = sum([
        df[df["platform"] == p]["posts_goal_weekly"].iloc[0] / 7 * total_days
        for p in df["platform"].unique()
    ])

    # KPI Calculations
    engagement_rate = (total_likes + total_comments + total_shares) / total_impressions * 100
    share_of_voice = (total_saves + total_shares) / total_impressions * 100
    profile_cvr = total_link_clicks / total_profile_visits * 100 if total_profile_visits > 0 else 0
    consistency_score = total_posts / total_posts_goal * 100 if total_posts_goal > 0 else 0

    # Benchmarks
    er_benchmark = 5.0
    sov_benchmark = 2.0
    pcvr_benchmark = 15.0
    cs_benchmark = 80.0

    kpis = [
        {
            "label": "Engagement Rate",
            "value": f"{engagement_rate:.1f}%",
            "benchmark": f"Benchmark: >{er_benchmark}%",
            "status": "good" if engagement_rate >= er_benchmark else ("warning" if engagement_rate >= er_benchmark * 0.7 else "bad"),
            "color": NEON_BLUE,
        },
        {
            "label": "Share of Voice",
            "value": f"{share_of_voice:.2f}%",
            "benchmark": f"Benchmark: >{sov_benchmark}%",
            "status": "good" if share_of_voice >= sov_benchmark else ("warning" if share_of_voice >= sov_benchmark * 0.7 else "bad"),
            "color": NEON_PURPLE,
        },
        {
            "label": "Profile Conversion Rate",
            "value": f"{profile_cvr:.1f}%",
            "benchmark": f"Benchmark: >{pcvr_benchmark}%",
            "status": "good" if profile_cvr >= pcvr_benchmark else ("warning" if profile_cvr >= pcvr_benchmark * 0.7 else "bad"),
            "color": NEON_ORANGE,
        },
        {
            "label": "Consistency Score",
            "value": f"{consistency_score:.0f}%",
            "benchmark": f"Target: >{cs_benchmark}%",
            "status": "good" if consistency_score >= cs_benchmark else ("warning" if consistency_score >= cs_benchmark * 0.7 else "bad"),
            "color": NEON_GREEN,
        },
    ]

    cols = st.columns(4)
    for idx, kpi in enumerate(kpis):
        status_color = {"good": NEON_GREEN, "warning": NEON_YELLOW, "bad": NEON_RED}[kpi["status"]]
        status_icon = {"good": "●", "warning": "●", "bad": "●"}[kpi["status"]]

        with cols[idx]:
            st.markdown(f"""
            <div class="kpi-card" style="border-top: 3px solid {kpi['color']};">
                <div class="kpi-label">{kpi['label']}</div>
                <div class="kpi-value" style="color: {status_color};">{kpi['value']}</div>
                <div class="kpi-benchmark">
                    <span style="color: {status_color};">{status_icon}</span> {kpi['benchmark']}
                </div>
            </div>
            """, unsafe_allow_html=True)


def render_metric_stack(df):
    """
    Section 2: Metric Stack (Depth & Traffic)
    Shows 4 key metrics PER PLATFORM in a detailed breakdown:
    - Engagement Rate (ER)
    - Share of Voice (SoV)
    - Profile Conversion Rate (PCR)
    - Consistency Score
    Includes comparison bars, sparklines, and benchmark indicators.
    """
    st.markdown('<div class="section-header">📊 METRIC STACK — DEPTH & TRAFFIC</div>', unsafe_allow_html=True)

    platforms = df["platform"].unique().tolist()

    # --- Aggregated Summary (All Platforms Combined) ---
    total_likes = df["likes"].sum()
    total_comments = df["comments"].sum()
    total_shares = df["shares"].sum()
    total_saves = df["saves"].sum()
    total_impressions = df["impressions"].sum()
    total_link_clicks = df["link_clicks"].sum()
    total_profile_visits = df["profile_visits"].sum()
    total_posts = df["posts_published"].sum()
    total_days = df["date"].nunique()

    total_posts_goal = sum([
        df[df["platform"] == p]["posts_goal_weekly"].iloc[0] / 7 * total_days
        for p in platforms
        if len(df[df["platform"] == p]) > 0
    ])

    agg_er = (total_likes + total_comments + total_shares) / max(total_impressions, 1) * 100
    agg_sov = (total_saves + total_shares) / max(total_impressions, 1) * 100
    agg_pcr = total_link_clicks / max(total_profile_visits, 1) * 100
    agg_cs = total_posts / max(total_posts_goal, 1) * 100

    # Benchmarks
    benchmarks = {
        "er": 5.0,
        "sov": 2.0,
        "pcr": 15.0,
        "cs": 80.0
    }

    # --- Per-Platform Breakdown ---
    platform_metrics = []
    for platform in platforms:
        pdf = df[df["platform"] == platform]
        p_impressions = pdf["impressions"].sum()
        p_likes = pdf["likes"].sum()
        p_comments = pdf["comments"].sum()
        p_shares = pdf["shares"].sum()
        p_saves = pdf["saves"].sum()
        p_link_clicks = pdf["link_clicks"].sum()
        p_profile_visits = pdf["profile_visits"].sum()
        p_posts = pdf["posts_published"].sum()
        p_goal = pdf["posts_goal_weekly"].iloc[0] / 7 * total_days if len(pdf) > 0 else 1

        er = (p_likes + p_comments + p_shares) / max(p_impressions, 1) * 100
        sov = (p_saves + p_shares) / max(p_impressions, 1) * 100
        pcr = p_link_clicks / max(p_profile_visits, 1) * 100
        cs = p_posts / max(p_goal, 1) * 100

        # Daily ER for sparkline
        daily_er = pdf.groupby("date").apply(
            lambda x: (x["likes"].sum() + x["comments"].sum() + x["shares"].sum()) / max(x["impressions"].sum(), 1) * 100
        ).tolist()

        platform_metrics.append({
            "platform": platform,
            "er": er,
            "sov": sov,
            "pcr": pcr,
            "cs": cs,
            "daily_er": daily_er,
            "total_impressions": p_impressions,
            "total_engagement": p_likes + p_comments + p_shares,
            "total_traffic": p_link_clicks,
        })

    # --- Render Comparison Bar Chart ---
    _render_metric_comparison_chart(platform_metrics, benchmarks)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- Render Per-Platform Detail Cards ---
    _render_platform_metric_cards(platform_metrics, benchmarks)


def _render_metric_comparison_chart(platform_metrics, benchmarks):
    """Horizontal grouped bar chart comparing all 4 metrics across platforms."""

    metrics_list = [
        {"key": "er", "label": "Engagement Rate (%)", "benchmark": benchmarks["er"], "color": NEON_BLUE},
        {"key": "sov", "label": "Share of Voice (%)", "benchmark": benchmarks["sov"], "color": NEON_PURPLE},
        {"key": "pcr", "label": "Profile CVR (%)", "benchmark": benchmarks["pcr"], "color": NEON_ORANGE},
        {"key": "cs", "label": "Consistency (%)", "benchmark": benchmarks["cs"], "color": NEON_GREEN},
    ]

    # Create 2x2 grid of charts
    col1, col2 = st.columns(2)

    for idx, metric in enumerate(metrics_list):
        target_col = col1 if idx % 2 == 0 else col2

        with target_col:
            platforms = [m["platform"] for m in platform_metrics]
            values = [m[metric["key"]] for m in platform_metrics]
            colors = [PLATFORM_COLORS[p] for p in platforms]

            fig = go.Figure()

            # Platform bars
            fig.add_trace(go.Bar(
                x=values,
                y=[f"{PLATFORM_ICONS[p]} {p}" for p in platforms],
                orientation="h",
                marker=dict(
                    color=colors,
                    line=dict(width=0),
                    cornerradius=4,
                ),
                text=[f"{v:.1f}%" for v in values],
                textposition="auto",
                textfont=dict(color=TEXT_PRIMARY, size=11, family="monospace"),
                hovertemplate="%{y}: %{x:.2f}%<extra></extra>",
            ))

            # Benchmark line
            fig.add_vline(
                x=metric["benchmark"],
                line_dash="dash",
                line_color=NEON_YELLOW,
                line_width=1.5,
                annotation_text=f"Target: {metric['benchmark']}%",
                annotation_position="top",
                annotation_font=dict(color=NEON_YELLOW, size=9),
            )

            fig.update_layout(
                title=dict(
                    text=metric["label"],
                    font=dict(color=TEXT_SECONDARY, size=12),
                    x=0,
                ),
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color=TEXT_SECONDARY, size=11),
                xaxis=dict(
                    gridcolor="#1E2330",
                    showgrid=True,
                    zeroline=False,
                ),
                yaxis=dict(
                    gridcolor="rgba(0,0,0,0)",
                    showgrid=False,
                    autorange="reversed",
                ),
                height=200,
                margin=dict(l=10, r=20, t=35, b=10),
                showlegend=False,
            )

            st.plotly_chart(fig, use_container_width=True)


def _render_platform_metric_cards(platform_metrics, benchmarks):
    """Render detailed metric cards per platform with all 4 KPIs.
    Uses smaller HTML chunks to avoid Streamlit rendering issues.
    """

    def get_status(value, benchmark):
        if value >= benchmark:
            return NEON_GREEN, "▲ On Track"
        elif value >= benchmark * 0.7:
            return NEON_YELLOW, "● Near Target"
        else:
            return NEON_RED, "▼ Below Target"

    def metric_row_html(label, value_str, value_color, fill_pct, status_text):
        """Generate a single metric row HTML."""
        fill_w = min(fill_pct, 100)
        return f"""
        <div style="margin-bottom: 14px;">
            <div style="font-size: 10px; color: #8892A0; text-transform: uppercase; 
                        letter-spacing: 1px; margin-bottom: 4px;">{label}</div>
            <div style="font-size: 20px; font-weight: 700; color: {value_color}; 
                        margin-bottom: 6px;">{value_str}</div>
            <div style="width: 100%; height: 4px; background: #2D3348; 
                        border-radius: 4px; overflow: hidden; margin-bottom: 4px;">
                <div style="height: 100%; width: {fill_w:.0f}%; background: {value_color}; 
                            border-radius: 4px;"></div>
            </div>
            <div style="font-size: 9px; font-weight: 600; color: {value_color}; 
                        text-transform: uppercase; letter-spacing: 0.8px;">{status_text}</div>
        </div>
        """

    cols = st.columns(len(platform_metrics))

    for idx, pm in enumerate(platform_metrics):
        platform = pm["platform"]
        color = PLATFORM_COLORS[platform]
        icon = PLATFORM_ICONS[platform]

        er_color, er_status = get_status(pm["er"], benchmarks["er"])
        sov_color, sov_status = get_status(pm["sov"], benchmarks["sov"])
        pcr_color, pcr_status = get_status(pm["pcr"], benchmarks["pcr"])
        cs_color, cs_status = get_status(pm["cs"], benchmarks["cs"])

        with cols[idx]:
            # Card container with border-top
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #1B1F2B 0%, #222838 100%);
                        border: 1px solid #2D3348; border-top: 3px solid {color};
                        border-radius: 12px; padding: 20px;">
                <div style="display: flex; align-items: center; gap: 8px; 
                            margin-bottom: 16px; padding-bottom: 12px; 
                            border-bottom: 1px solid #2D3348;">
                    <span style="font-size: 18px;">{icon}</span>
                    <span style="font-size: 14px; font-weight: 600; color: #FFFFFF; 
                                 text-transform: uppercase; letter-spacing: 1px;">{platform}</span>
                </div>
                {metric_row_html("Engagement Rate", f"{pm['er']:.1f}%", er_color,
                                 pm['er'] / benchmarks['er'] * 100, er_status)}
                {metric_row_html("Share of Voice", f"{pm['sov']:.2f}%", sov_color,
                                 pm['sov'] / benchmarks['sov'] * 100, sov_status)}
                {metric_row_html("Profile CVR", f"{pm['pcr']:.1f}%", pcr_color,
                                 pm['pcr'] / benchmarks['pcr'] * 100, pcr_status)}
                {metric_row_html("Consistency", f"{pm['cs']:.0f}%", cs_color,
                                 pm['cs'] / 100 * 100, cs_status)}
                <div style="margin-top: 16px; padding-top: 12px; border-top: 1px solid #2D3348;">
                    <div style="display: flex; justify-content: space-between; font-size: 11px; margin-bottom: 6px;">
                        <span style="color: #5A6577;">Impressions</span>
                        <span style="color: #FFFFFF; font-weight: 600;">{pm['total_impressions']:,.0f}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; font-size: 11px; margin-bottom: 6px;">
                        <span style="color: #5A6577;">Engagement</span>
                        <span style="color: #FFFFFF; font-weight: 600;">{pm['total_engagement']:,.0f}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; font-size: 11px;">
                        <span style="color: #5A6577;">Traffic</span>
                        <span style="color: #FFFFFF; font-weight: 600;">{pm['total_traffic']:,.0f}</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)


def render_platform_overview_chart(df):
    """
    Quick overview chart: Follower Growth Trend per Platform (30 days)
    Plotly line chart with dark mode styling.
    """
    st.markdown('<div class="section-header">📈 FOLLOWER GROWTH TREND — 30 DAYS</div>', unsafe_allow_html=True)

    fig = go.Figure()

    for platform in ["Instagram", "TikTok", "YouTube", "LinkedIn"]:
        platform_data = df[df["platform"] == platform].sort_values("date")
        fig.add_trace(go.Scatter(
            x=platform_data["date"],
            y=platform_data["followers"],
            mode="lines",
            name=f"{PLATFORM_ICONS[platform]} {platform}",
            line=dict(color=PLATFORM_COLORS[platform], width=2.5),
            hovertemplate=(
                f"<b>{platform}</b><br>"
                "Date: %{x|%b %d}<br>"
                "Followers: %{y:,.0f}<br>"
                "<extra></extra>"
            ),
        ))

    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color=TEXT_SECONDARY, size=12),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            font=dict(color=TEXT_PRIMARY, size=12),
        ),
        xaxis=dict(
            gridcolor="#1E2330",
            showgrid=True,
            tickformat="%b %d",
        ),
        yaxis=dict(
            gridcolor="#1E2330",
            showgrid=True,
            tickformat=",",
        ),
        height=380,
        margin=dict(l=20, r=20, t=40, b=20),
        hovermode="x unified",
    )

    st.plotly_chart(fig, use_container_width=True)


def render_daily_engagement_chart(df):
    """
    Daily Engagement Rate per Platform — Area Chart
    """
    st.markdown('<div class="section-header">💬 DAILY ENGAGEMENT RATE — BY PLATFORM</div>', unsafe_allow_html=True)

    fig = go.Figure()

    for platform in ["Instagram", "TikTok", "YouTube", "LinkedIn"]:
        platform_data = df[df["platform"] == platform].sort_values("date")
        fig.add_trace(go.Scatter(
            x=platform_data["date"],
            y=platform_data["engagement_rate"],
            mode="lines",
            name=f"{PLATFORM_ICONS[platform]} {platform}",
            line=dict(color=PLATFORM_COLORS[platform], width=2),
            fill="tozeroy",
            fillcolor=f"rgba({int(PLATFORM_COLORS[platform][1:3], 16)}, "
                      f"{int(PLATFORM_COLORS[platform][3:5], 16)}, "
                      f"{int(PLATFORM_COLORS[platform][5:7], 16)}, 0.08)",
            hovertemplate=(
                f"<b>{platform}</b><br>"
                "Date: %{x|%b %d}<br>"
                "ER: %{y:.2f}%<br>"
                "<extra></extra>"
            ),
        ))

    # Add benchmark line
    fig.add_hline(
        y=5.0,
        line_dash="dash",
        line_color=NEON_YELLOW,
        annotation_text="Benchmark: 5%",
        annotation_position="top right",
        annotation_font_color=NEON_YELLOW,
        annotation_font_size=11,
    )

    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color=TEXT_SECONDARY, size=12),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            font=dict(color=TEXT_PRIMARY, size=12),
        ),
        xaxis=dict(
            gridcolor="#1E2330",
            showgrid=True,
            tickformat="%b %d",
        ),
        yaxis=dict(
            gridcolor="#1E2330",
            showgrid=True,
            title="Engagement Rate (%)",
            titlefont=dict(color=TEXT_MUTED, size=11),
        ),
        height=350,
        margin=dict(l=20, r=20, t=40, b=20),
        hovermode="x unified",
    )

    st.plotly_chart(fig, use_container_width=True)


# ============================================================
# 3B. COMMUNITY HEALTH — ENGAGEMENT FUNNEL & LEADERBOARD
# ============================================================

def render_engagement_funnel(df):
    """
    Visualization A: The Engagement Funnel
    Horizontal funnel: Reach → Interaction → Click
    Shows conversion at each stage across all platforms or per platform.
    """
    st.markdown('<div class="section-header">🔄 ENGAGEMENT FUNNEL — REACH → INTERACTION → CLICK</div>', unsafe_allow_html=True)

    # Calculate funnel stages
    platforms = df["platform"].unique().tolist()

    # Aggregated funnel
    total_reach = df["impressions"].sum()
    total_interaction = (df["likes"] + df["comments"] + df["shares"] + df["saves"]).sum()
    total_clicks = df["link_clicks"].sum()

    reach_to_interaction = total_interaction / max(total_reach, 1) * 100
    interaction_to_click = total_clicks / max(total_interaction, 1) * 100
    reach_to_click = total_clicks / max(total_reach, 1) * 100

    # --- Aggregated Funnel Chart ---
    col_funnel, col_rates = st.columns([3, 1])

    with col_funnel:
        fig = go.Figure()

        # Funnel stages
        stages = ["👁️ Reach (Impressions)", "💬 Interaction (Engagement)", "🔗 Click (Link Clicks)"]
        values = [total_reach, total_interaction, total_clicks]
        colors = [NEON_BLUE, NEON_PURPLE, NEON_ORANGE]

        fig.add_trace(go.Funnel(
            y=stages,
            x=values,
            textposition="auto",
            textinfo="value+percent initial",
            texttemplate="%{value:,.0f}<br>(%{percentInitial:.1%})",
            textfont=dict(color=TEXT_PRIMARY, size=13),
            marker=dict(
                color=colors,
                line=dict(width=0),
            ),
            connector=dict(
                line=dict(color="#2D3348", width=1),
                fillcolor="rgba(45, 51, 72, 0.3)",
            ),
        ))

        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color=TEXT_SECONDARY, size=12),
            height=280,
            margin=dict(l=10, r=10, t=10, b=10),
            showlegend=False,
        )

        st.plotly_chart(fig, use_container_width=True)

    with col_rates:
        # Conversion rate cards
        st.markdown(f"""
        <div style="padding: 12px 0;">
            <div style="background: linear-gradient(135deg, #1B1F2B 0%, #222838 100%);
                        border: 1px solid #2D3348; border-left: 3px solid {NEON_BLUE};
                        border-radius: 8px; padding: 14px 16px; margin-bottom: 10px;">
                <div style="font-size: 9px; color: #8892A0; text-transform: uppercase; 
                            letter-spacing: 1px;">Reach → Interaction</div>
                <div style="font-size: 22px; font-weight: 700; color: {NEON_BLUE};">
                    {reach_to_interaction:.2f}%</div>
            </div>
            <div style="background: linear-gradient(135deg, #1B1F2B 0%, #222838 100%);
                        border: 1px solid #2D3348; border-left: 3px solid {NEON_PURPLE};
                        border-radius: 8px; padding: 14px 16px; margin-bottom: 10px;">
                <div style="font-size: 9px; color: #8892A0; text-transform: uppercase; 
                            letter-spacing: 1px;">Interaction → Click</div>
                <div style="font-size: 22px; font-weight: 700; color: {NEON_PURPLE};">
                    {interaction_to_click:.2f}%</div>
            </div>
            <div style="background: linear-gradient(135deg, #1B1F2B 0%, #222838 100%);
                        border: 1px solid #2D3348; border-left: 3px solid {NEON_ORANGE};
                        border-radius: 8px; padding: 14px 16px;">
                <div style="font-size: 9px; color: #8892A0; text-transform: uppercase; 
                            letter-spacing: 1px;">Total Reach → Click</div>
                <div style="font-size: 22px; font-weight: 700; color: {NEON_ORANGE};">
                    {reach_to_click:.3f}%</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # --- Per-Platform Funnel Comparison ---
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="font-size: 11px; color: #5A6577; text-transform: uppercase; 
                letter-spacing: 1.5px; margin-bottom: 12px;">
        📊 Per-Platform Funnel Breakdown
    </div>
    """, unsafe_allow_html=True)

    # Grouped bar chart comparing funnel stages per platform
    platform_funnel_data = []
    for platform in platforms:
        pdf = df[df["platform"] == platform]
        p_reach = pdf["impressions"].sum()
        p_interaction = (pdf["likes"] + pdf["comments"] + pdf["shares"] + pdf["saves"]).sum()
        p_clicks = pdf["link_clicks"].sum()

        platform_funnel_data.append({
            "platform": platform,
            "Reach": p_reach,
            "Interaction": p_interaction,
            "Clicks": p_clicks,
            "reach_to_int_pct": p_interaction / max(p_reach, 1) * 100,
            "int_to_click_pct": p_clicks / max(p_interaction, 1) * 100,
        })

    fig2 = go.Figure()

    # Normalize to percentages for comparison
    stage_configs = [
        {"key": "Reach", "color": NEON_BLUE, "label": "Reach"},
        {"key": "Interaction", "color": NEON_PURPLE, "label": "Interaction"},
        {"key": "Clicks", "color": NEON_ORANGE, "label": "Clicks"},
    ]

    for stage in stage_configs:
        vals = [d[stage["key"]] for d in platform_funnel_data]
        platform_labels = [f"{PLATFORM_ICONS[d['platform']]} {d['platform']}" for d in platform_funnel_data]

        fig2.add_trace(go.Bar(
            name=stage["label"],
            x=platform_labels,
            y=vals,
            marker=dict(color=stage["color"], cornerradius=4),
            text=[format_number(v) for v in vals],
            textposition="auto",
            textfont=dict(color=TEXT_PRIMARY, size=10),
        ))

    fig2.update_layout(
        barmode="group",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color=TEXT_SECONDARY, size=11),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            font=dict(color=TEXT_PRIMARY, size=11),
        ),
        xaxis=dict(gridcolor="rgba(0,0,0,0)", showgrid=False),
        yaxis=dict(gridcolor="#1E2330", showgrid=True, tickformat=","),
        height=300,
        margin=dict(l=10, r=10, t=40, b=10),
    )

    st.plotly_chart(fig2, use_container_width=True)

    # --- Conversion Rate Table ---
    rate_cols = st.columns(len(platform_funnel_data))
    for idx, pf in enumerate(platform_funnel_data):
        platform = pf["platform"]
        color = PLATFORM_COLORS[platform]
        icon = PLATFORM_ICONS[platform]

        with rate_cols[idx]:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #1B1F2B 0%, #222838 100%);
                        border: 1px solid #2D3348; border-top: 2px solid {color};
                        border-radius: 8px; padding: 14px; text-align: center;">
                <div style="font-size: 12px; color: #8892A0; margin-bottom: 8px;">
                    {icon} {platform}
                </div>
                <div style="display: flex; justify-content: space-around;">
                    <div>
                        <div style="font-size: 16px; font-weight: 700; color: {NEON_BLUE};">
                            {pf['reach_to_int_pct']:.1f}%</div>
                        <div style="font-size: 8px; color: #5A6577; text-transform: uppercase;">
                            R→I Rate</div>
                    </div>
                    <div style="width: 1px; background: #2D3348;"></div>
                    <div>
                        <div style="font-size: 16px; font-weight: 700; color: {NEON_ORANGE};">
                            {pf['int_to_click_pct']:.1f}%</div>
                        <div style="font-size: 8px; color: #5A6577; text-transform: uppercase;">
                            I→C Rate</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)


def render_content_leaderboard(platform_filter):
    """
    Visualization B: The Content Leaderboard
    Top 3 Posts of the Week with badges:
    - 🏆 Most Shared (Brand Awareness Winner)
    - 💬 Most Commented (Community Winner)
    - 🔗 Most Clicked (Traffic Winner)
    Split into small st.markdown() calls to avoid Streamlit rendering issues.
    """
    st.markdown('<div class="section-header">🏅 CONTENT LEADERBOARD — TOP PERFORMERS THIS WEEK</div>', unsafe_allow_html=True)

    # Generate content data
    content_df = generate_content_library(num_posts=48)

    # Apply platform filter
    if platform_filter:
        content_df = content_df[content_df["platform"].isin(platform_filter)]

    if content_df.empty:
        st.info("No content available for selected platforms.")
        return

    # Filter to last 7 days
    seven_days_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    week_df = content_df[content_df["date"] >= seven_days_ago]

    # If not enough data in last 7 days, use all data
    if len(week_df) < 3:
        week_df = content_df

    # Find winners
    most_shared = week_df.loc[week_df["shares"].idxmax()]
    most_commented = week_df.loc[week_df["comments"].idxmax()]
    most_clicked = week_df.loc[week_df["link_clicks"].idxmax()]

    winners = [
        {
            "badge": "🏆",
            "badge_label": "MOST SHARED",
            "badge_subtitle": "Brand Awareness Winner",
            "post": most_shared,
            "highlight_metric": "shares",
            "highlight_value": most_shared["shares"],
            "accent_color": NEON_YELLOW,
            "rank_bg": "linear-gradient(135deg, rgba(255, 215, 0, 0.12) 0%, rgba(255, 215, 0, 0.03) 100%)",
            "border_color": "rgba(255, 215, 0, 0.4)",
        },
        {
            "badge": "💬",
            "badge_label": "MOST COMMENTED",
            "badge_subtitle": "Community Winner",
            "post": most_commented,
            "highlight_metric": "comments",
            "highlight_value": most_commented["comments"],
            "accent_color": NEON_PURPLE,
            "rank_bg": "linear-gradient(135deg, rgba(168, 85, 247, 0.12) 0%, rgba(168, 85, 247, 0.03) 100%)",
            "border_color": "rgba(168, 85, 247, 0.4)",
        },
        {
            "badge": "🔗",
            "badge_label": "MOST CLICKED",
            "badge_subtitle": "Traffic Winner",
            "post": most_clicked,
            "highlight_metric": "link_clicks",
            "highlight_value": most_clicked["link_clicks"],
            "accent_color": NEON_ORANGE,
            "rank_bg": "linear-gradient(135deg, rgba(255, 107, 53, 0.12) 0%, rgba(255, 107, 53, 0.03) 100%)",
            "border_color": "rgba(255, 107, 53, 0.4)",
        },
    ]

    cols = st.columns(3)

    for idx, winner in enumerate(winners):
        post = winner["post"]
        platform = post["platform"]
        p_color = PLATFORM_COLORS.get(platform, "#444")
        p_icon = PLATFORM_ICONS.get(platform, "📄")
        accent = winner["accent_color"]
        highlight_label = winner["highlight_metric"].replace("_", " ").title()

        with cols[idx]:
            # Part 1: Badge Header
            st.markdown(f"""<div style="background: {winner['rank_bg']}; border: 1px solid {winner['border_color']}; border-radius: 12px 12px 0 0; padding: 16px 20px; text-align: center;">
<div style="font-size: 36px; margin-bottom: 4px;">{winner['badge']}</div>
<div style="font-size: 12px; font-weight: 700; color: {accent}; text-transform: uppercase; letter-spacing: 2px;">{winner['badge_label']}</div>
<div style="font-size: 10px; color: #8892A0; margin-top: 2px;">{winner['badge_subtitle']}</div>
</div>""", unsafe_allow_html=True)

            # Part 2: Post Info
            st.markdown(f"""<div style="background: rgba(0,0,0,0.15); border-left: 1px solid {winner['border_color']}; border-right: 1px solid {winner['border_color']}; padding: 14px 20px 0 20px;">
<div style="display: flex; align-items: center; gap: 10px;">
<div style="width: 36px; height: 36px; border-radius: 8px; background: {p_color}; display: flex; align-items: center; justify-content: center; font-size: 18px; flex-shrink: 0;">{p_icon}</div>
<div>
<div style="font-size: 12px; font-weight: 600; color: #FFFFFF; line-height: 1.3;">{post['title']}</div>
<div style="font-size: 9px; color: #5A6577; margin-top: 2px;">{platform} · {post['content_type']} · {post['date']}</div>
</div>
</div>
</div>""", unsafe_allow_html=True)

            # Part 3: Highlight Metric
            st.markdown(f"""<div style="background: rgba(0,0,0,0.15); border-left: 1px solid {winner['border_color']}; border-right: 1px solid {winner['border_color']}; padding: 8px 20px;">
<div style="text-align: center; padding: 12px 0; background: rgba(0,0,0,0.25); border-radius: 8px;">
<div style="font-size: 28px; font-weight: 700; color: {accent};">{format_number(winner['highlight_value'])}</div>
<div style="font-size: 9px; color: #8892A0; text-transform: uppercase; letter-spacing: 1px;">{highlight_label}</div>
</div>
</div>""", unsafe_allow_html=True)

            # Part 4: Metrics Grid (Views, Likes, Saves)
            st.markdown(f"""<div style="background: rgba(0,0,0,0.15); border-left: 1px solid {winner['border_color']}; border-right: 1px solid {winner['border_color']}; padding: 0 20px 8px 20px;">
<table style="width: 100%; border-collapse: separate; border-spacing: 4px 0;">
<tr>
<td style="text-align: center; padding: 8px 4px; background: rgba(0,0,0,0.2); border-radius: 6px; width: 33%;">
<div style="font-size: 13px; font-weight: 600; color: #FFFFFF;">{format_number(post['views'])}</div>
<div style="font-size: 8px; color: #5A6577; text-transform: uppercase;">Views</div>
</td>
<td style="text-align: center; padding: 8px 4px; background: rgba(0,0,0,0.2); border-radius: 6px; width: 33%;">
<div style="font-size: 13px; font-weight: 600; color: #FFFFFF;">{format_number(post['likes'])}</div>
<div style="font-size: 8px; color: #5A6577; text-transform: uppercase;">Likes</div>
</td>
<td style="text-align: center; padding: 8px 4px; background: rgba(0,0,0,0.2); border-radius: 6px; width: 33%;">
<div style="font-size: 13px; font-weight: 600; color: #FFFFFF;">{format_number(post['saves'])}</div>
<div style="font-size: 8px; color: #5A6577; text-transform: uppercase;">Saves</div>
</td>
</tr>
</table>
</div>""", unsafe_allow_html=True)

            # Part 5: Score Badges + Bottom border
            st.markdown(f"""<div style="background: rgba(0,0,0,0.15); border-left: 1px solid {winner['border_color']}; border-right: 1px solid {winner['border_color']}; border-bottom: 1px solid {winner['border_color']}; border-radius: 0 0 12px 12px; padding: 0 20px 14px 20px;">
<table style="width: 100%; border-collapse: separate; border-spacing: 4px 0;">
<tr>
<td style="text-align: center; padding: 5px 0; border-radius: 6px; background: rgba(168, 85, 247, 0.15); font-size: 10px; font-weight: 600; color: #A855F7; width: 50%;">🔥 Viral: {post['virality_score']}%</td>
<td style="text-align: center; padding: 5px 0; border-radius: 6px; background: rgba(0, 212, 255, 0.15); font-size: 10px; font-weight: 600; color: #00D4FF; width: 50%;">🎯 Conv: {post['conversion_score']}%</td>
</tr>
</table>
</div>""", unsafe_allow_html=True)


# ============================================================
# 3C. AI BRAIN — THE COMMUNITY MANAGER (Placeholder)
# ============================================================

def render_ai_brain(df, platform_filter):
    """
    Section 4: The AI Brain Logic (The Community Manager)
    Placeholder — ready for OpenAI API integration.
    
    Logic A (Sentiment Guard): Negative sentiment detection
    Logic B (Trend Spotter): Trending audio/content detection
    Logic C (SEO Assist): Reach vs retention optimization
    
    Currently generates static demo insights based on data patterns.
    """
    st.markdown('<div class="section-header">🧠 AI BRAIN — THE COMMUNITY MANAGER</div>', unsafe_allow_html=True)

    # --- Generate placeholder insights based on actual data ---
    insights = _generate_placeholder_insights(df, platform_filter)

    # --- Status Bar ---
    st.markdown(f"""<div style="display: flex; align-items: center; justify-content: space-between; padding: 10px 16px; background: linear-gradient(135deg, #1B1F2B 0%, #222838 100%); border: 1px solid #2D3348; border-radius: 8px; margin-bottom: 16px;">
<div style="display: flex; align-items: center; gap: 8px;">
<div style="width: 8px; height: 8px; border-radius: 50%; background: {NEON_GREEN}; animation: pulse 2s infinite;"></div>
<span style="font-size: 11px; color: #8892A0; text-transform: uppercase; letter-spacing: 1px;">AI Engine Status: Active</span>
</div>
<div style="font-size: 10px; color: #5A6577;">Last Analysis: Just now · Powered by OpenAI</div>
</div>""", unsafe_allow_html=True)

    # --- Insight Cards ---
    for insight in insights:
        _render_insight_card(insight)

    # --- Generate Insight Button (Placeholder) ---
    st.markdown("<br>", unsafe_allow_html=True)
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    with col_btn2:
        generate_clicked = st.button(
            "🧠 Generate Fresh Insights",
            key="ai_generate_insights",
            use_container_width=True,
            type="primary"
        )
        if generate_clicked:
            st.info("🔌 OpenAI API integration pending. Insights above are placeholder data based on current metrics.")


def _generate_placeholder_insights(df, platform_filter):
    """
    Generate realistic-looking placeholder insights based on actual data patterns.
    These will be replaced by real OpenAI API calls later.
    """
    insights = []

    # --- Logic A: Sentiment Guard ---
    # Find platform with lowest engagement rate
    platform_er = {}
    for platform in df["platform"].unique():
        pdf = df[df["platform"] == platform]
        er = (pdf["likes"].sum() + pdf["comments"].sum() + pdf["shares"].sum()) / max(pdf["impressions"].sum(), 1) * 100
        platform_er[platform] = er

    if platform_er:
        worst_platform = min(platform_er, key=platform_er.get)
        worst_er = platform_er[worst_platform]
        best_platform = max(platform_er, key=platform_er.get)
        best_er = platform_er[best_platform]

        insights.append({
            "logic_id": "A",
            "logic_name": "Sentiment Guard",
            "icon": "🛡️",
            "severity": "warning" if worst_er < 5.0 else "info",
            "title": f"Low engagement detected on {worst_platform}",
            "body": f"Engagement Rate on {worst_platform} is {worst_er:.1f}%, below the 5% benchmark. "
                    f"Meanwhile {best_platform} is performing at {best_er:.1f}%. "
                    f"This could indicate audience fatigue or content mismatch on {worst_platform}.",
            "recommendation": f"Audit recent {worst_platform} content. Consider A/B testing different content formats "
                             f"or posting times. Review comment sentiment for negative feedback patterns.",
            "accent_color": NEON_YELLOW if worst_er < 5.0 else NEON_BLUE,
        })

    # --- Logic B: Trend Spotter ---
    # Find platform with highest growth
    platform_growth = {}
    for platform in df["platform"].unique():
        pdf = df[df["platform"] == platform]
        growth = pdf["follower_growth"].sum()
        platform_growth[platform] = growth

    if platform_growth:
        trending_platform = max(platform_growth, key=platform_growth.get)
        trending_growth = platform_growth[trending_platform]

        insights.append({
            "logic_id": "B",
            "logic_name": "Trend Spotter",
            "icon": "📈",
            "severity": "success",
            "title": f"{trending_platform} is trending upward",
            "body": f"{trending_platform} gained +{trending_growth:,.0f} followers in the selected period, "
                    f"the highest growth across all platforms. "
                    f"Content resonance is strong — your audience is responding to recent posts.",
            "recommendation": f"Double down on {trending_platform} content strategy. Increase posting frequency "
                             f"by 1-2 posts/week. Repurpose top-performing content from {trending_platform} "
                             f"to other platforms.",
            "accent_color": NEON_GREEN,
        })

    # --- Logic C: SEO Assist ---
    # Find platform with high views but low link clicks (reach vs conversion gap)
    platform_gap = {}
    for platform in df["platform"].unique():
        pdf = df[df["platform"] == platform]
        views = pdf["views"].sum()
        clicks = pdf["link_clicks"].sum()
        gap_ratio = clicks / max(views, 1) * 100
        platform_gap[platform] = {"ratio": gap_ratio, "views": views, "clicks": clicks}

    if platform_gap:
        worst_cvr_platform = min(platform_gap, key=lambda x: platform_gap[x]["ratio"])
        gap_data = platform_gap[worst_cvr_platform]

        insights.append({
            "logic_id": "C",
            "logic_name": "SEO Assist",
            "icon": "🔍",
            "severity": "warning",
            "title": f"High reach but low traffic conversion on {worst_cvr_platform}",
            "body": f"{worst_cvr_platform} has {format_number(gap_data['views'])} views but only "
                    f"{format_number(gap_data['clicks'])} link clicks ({gap_data['ratio']:.2f}% conversion). "
                    f"Content is getting discovered but failing to drive traffic.",
            "recommendation": f"Add stronger CTAs in {worst_cvr_platform} content. "
                             f"Switch generic hashtags for niche SEO keywords. "
                             f"Ensure bio link is updated and link stickers are used in Stories.",
            "accent_color": NEON_ORANGE,
        })

    # --- Logic D: Consistency Check ---
    total_posts = df["posts_published"].sum()
    total_days = df["date"].nunique()
    total_goal = sum([
        df[df["platform"] == p]["posts_goal_weekly"].iloc[0] / 7 * total_days
        for p in df["platform"].unique()
        if len(df[df["platform"] == p]) > 0
    ])
    consistency = total_posts / max(total_goal, 1) * 100

    if consistency < 80:
        insights.append({
            "logic_id": "D",
            "logic_name": "Consistency Monitor",
            "icon": "📅",
            "severity": "critical",
            "title": f"Publishing consistency is below target ({consistency:.0f}%)",
            "body": f"Only {int(total_posts)} of {int(total_goal)} planned posts were published "
                    f"({consistency:.0f}% of target). Inconsistent posting directly impacts "
                    f"algorithm favorability and audience retention.",
            "recommendation": "Create a content calendar with batch-produced posts. "
                             "Use scheduling tools (Later, Buffer) to automate publishing. "
                             "Assign accountability: who posts what, when.",
            "accent_color": NEON_RED,
        })
    else:
        insights.append({
            "logic_id": "D",
            "logic_name": "Consistency Monitor",
            "icon": "📅",
            "severity": "success",
            "title": f"Publishing consistency is on track ({consistency:.0f}%)",
            "body": f"{int(total_posts)} of {int(total_goal)} planned posts published "
                    f"({consistency:.0f}% of target). Good rhythm — keep it up.",
            "recommendation": "Maintain current cadence. Consider testing +1 post/week "
                             "on your highest-performing platform to see if engagement scales.",
            "accent_color": NEON_GREEN,
        })

    return insights


def _render_insight_card(insight):
    """Render a single AI insight card. Split into small markdown chunks."""
    
    severity_config = {
        "critical": {"bg": "rgba(255, 59, 92, 0.08)", "border": "rgba(255, 59, 92, 0.35)", "label_bg": "rgba(255, 59, 92, 0.2)", "label_color": NEON_RED, "label": "CRITICAL"},
        "warning": {"bg": "rgba(255, 215, 0, 0.06)", "border": "rgba(255, 215, 0, 0.3)", "label_bg": "rgba(255, 215, 0, 0.15)", "label_color": NEON_YELLOW, "label": "WARNING"},
        "success": {"bg": "rgba(0, 255, 136, 0.06)", "border": "rgba(0, 255, 136, 0.25)", "label_bg": "rgba(0, 255, 136, 0.15)", "label_color": NEON_GREEN, "label": "POSITIVE"},
        "info": {"bg": "rgba(0, 212, 255, 0.06)", "border": "rgba(0, 212, 255, 0.25)", "label_bg": "rgba(0, 212, 255, 0.15)", "label_color": NEON_BLUE, "label": "INFO"},
    }

    sev = severity_config.get(insight["severity"], severity_config["info"])
    accent = insight["accent_color"]

    # Card Header
    st.markdown(f"""<div style="background: {sev['bg']}; border: 1px solid {sev['border']}; border-radius: 12px 12px 0 0; padding: 14px 20px;">
<div style="display: flex; align-items: center; justify-content: space-between;">
<div style="display: flex; align-items: center; gap: 10px;">
<span style="font-size: 22px;">{insight['icon']}</span>
<div>
<div style="font-size: 13px; font-weight: 600; color: #FFFFFF;">{insight['title']}</div>
<div style="font-size: 10px; color: #5A6577; margin-top: 2px;">Logic {insight['logic_id']}: {insight['logic_name']}</div>
</div>
</div>
<div style="padding: 3px 10px; border-radius: 20px; background: {sev['label_bg']}; font-size: 9px; font-weight: 700; color: {sev['label_color']}; text-transform: uppercase; letter-spacing: 1px;">{sev['label']}</div>
</div>
</div>""", unsafe_allow_html=True)

    # Card Body — Analysis
    st.markdown(f"""<div style="background: {sev['bg']}; border-left: 1px solid {sev['border']}; border-right: 1px solid {sev['border']}; padding: 0 20px 12px 20px;">
<div style="font-size: 12px; color: #C0C7D0; line-height: 1.7; padding: 10px 14px; background: rgba(0,0,0,0.15); border-radius: 8px;">
<span style="font-size: 9px; color: #5A6577; text-transform: uppercase; letter-spacing: 1px; display: block; margin-bottom: 6px;">📊 Analysis</span>
{insight['body']}
</div>
</div>""", unsafe_allow_html=True)

    # Card Footer — Recommendation
    st.markdown(f"""<div style="background: {sev['bg']}; border: 1px solid {sev['border']}; border-top: none; border-radius: 0 0 12px 12px; padding: 0 20px 14px 20px;">
<div style="font-size: 12px; color: #C0C7D0; line-height: 1.7; padding: 10px 14px; background: rgba(0,0,0,0.1); border-radius: 8px; border-left: 3px solid {accent};">
<span style="font-size: 9px; color: {accent}; text-transform: uppercase; letter-spacing: 1px; display: block; margin-bottom: 6px;">💡 Recommendation</span>
{insight['recommendation']}
</div>
</div>""", unsafe_allow_html=True)

    # Spacer
    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)


# ============================================================
# 3D. CONTENT LIBRARY COMPONENTS
# ============================================================

def format_number(num):
    """Format large numbers: 1500 → 1.5K, 1500000 → 1.5M"""
    if num >= 1_000_000:
        return f"{num / 1_000_000:.1f}M"
    elif num >= 1_000:
        return f"{num / 1_000:.1f}K"
    return str(num)


def render_content_library(platform_filter):
    """
    View Mode 2: Content Library
    Thumbnail Grid of posts, sortable by Virality Score or Conversion Score.
    Includes Grid View and Table View toggle, pagination, and platform filter.
    """
    st.markdown('<div class="section-header">📚 CONTENT LIBRARY — POST PERFORMANCE</div>', unsafe_allow_html=True)

    # Generate content data
    content_df = generate_content_library(num_posts=48)

    # Apply platform filter
    if platform_filter:
        content_df = content_df[content_df["platform"].isin(platform_filter)]

    if content_df.empty:
        st.info("No content available for selected platforms.")
        return

    # --- Controls Row ---
    ctrl_col1, ctrl_col2, ctrl_col3, ctrl_col4 = st.columns([2, 2, 2, 4])

    with ctrl_col1:
        view_mode = st.selectbox(
            "👁️ View",
            ["Grid View", "Table View"],
            key="content_view_mode"
        )

    with ctrl_col2:
        sort_by = st.selectbox(
            "📊 Sort By",
            ["Virality Score ↓", "Conversion Score ↓", "Views ↓", "Likes ↓", "Most Recent"],
            key="content_sort_by"
        )

    with ctrl_col3:
        content_type_options = ["All Types"] + sorted(content_df["content_type"].unique().tolist())
        content_type_filter = st.selectbox(
            "🏷️ Content Type",
            content_type_options,
            key="content_type_filter"
        )

    # Apply content type filter
    if content_type_filter != "All Types":
        content_df = content_df[content_df["content_type"] == content_type_filter]

    # Apply sorting
    sort_map = {
        "Virality Score ↓": ("virality_score", False),
        "Conversion Score ↓": ("conversion_score", False),
        "Views ↓": ("views", False),
        "Likes ↓": ("likes", False),
        "Most Recent": ("date", False),
    }
    sort_col, sort_asc = sort_map.get(sort_by, ("virality_score", False))
    content_df = content_df.sort_values(sort_col, ascending=sort_asc).reset_index(drop=True)

    # --- Pagination ---
    ITEMS_PER_PAGE = 12
    total_items = len(content_df)
    total_pages = max(1, (total_items + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE)

    # Initialize session state for page
    if "content_page" not in st.session_state:
        st.session_state.content_page = 1

    # Clamp page
    if st.session_state.content_page > total_pages:
        st.session_state.content_page = total_pages

    current_page = st.session_state.content_page
    start_idx = (current_page - 1) * ITEMS_PER_PAGE
    end_idx = min(start_idx + ITEMS_PER_PAGE, total_items)
    page_df = content_df.iloc[start_idx:end_idx]

    # --- Summary Bar ---
    st.markdown(f"""
    <div style="display: flex; justify-content: space-between; align-items: center; 
                padding: 8px 0; margin-bottom: 12px;">
        <span style="font-size: 12px; color: #8892A0;">
            Showing {start_idx + 1}-{end_idx} of {total_items} posts
        </span>
        <span style="font-size: 12px; color: #5A6577;">
            Page {current_page} of {total_pages}
        </span>
    </div>
    """, unsafe_allow_html=True)

    # --- Render based on view mode ---
    if view_mode == "Grid View":
        render_content_grid(page_df)
    else:
        render_content_table(page_df, sort_by)

    # --- Pagination Controls ---
    render_pagination(current_page, total_pages)


def render_content_grid(page_df):
    """Render content as visual grid cards with placeholder thumbnails."""

    # Use st.columns for 3-column grid
    cols_per_row = 3
    rows_needed = (len(page_df) + cols_per_row - 1) // cols_per_row

    for row_idx in range(rows_needed):
        cols = st.columns(cols_per_row)
        for col_idx in range(cols_per_row):
            item_idx = row_idx * cols_per_row + col_idx
            if item_idx >= len(page_df):
                break

            post = page_df.iloc[item_idx]
            platform = post["platform"]
            color = PLATFORM_COLORS.get(platform, "#444")
            icon = PLATFORM_ICONS.get(platform, "📄")

            # Generate a gradient based on platform color
            r = int(color[1:3], 16)
            g = int(color[3:5], 16)
            b = int(color[5:7], 16)
            gradient = f"linear-gradient(135deg, rgba({r},{g},{b},0.3) 0%, rgba({r},{g},{b},0.08) 100%)"

            # Virality score color
            vs = post["virality_score"]
            vs_color = NEON_GREEN if vs >= 3.0 else (NEON_YELLOW if vs >= 1.5 else NEON_RED)

            # Conversion score color
            cs = post["conversion_score"]
            cs_color = NEON_GREEN if cs >= 2.0 else (NEON_YELLOW if cs >= 1.0 else NEON_RED)

            with cols[col_idx]:
                st.markdown(f"""
                <div class="content-card">
                    <div class="card-thumbnail" style="background: {gradient};">
                        <span class="card-thumbnail-platform" style="background: {color};">{icon} {platform}</span>
                        <span class="card-thumbnail-date">{post['date']}</span>
                        <span class="card-thumbnail-icon">{icon}</span>
                        <span class="card-thumbnail-type">{post['content_type']}</span>
                    </div>
                    <div class="card-body">
                        <div class="card-title">{post['title']}</div>
                        <div class="card-metrics">
                            <div class="card-metric-item">
                                <div class="card-metric-value">{format_number(post['views'])}</div>
                                <div class="card-metric-label">Views</div>
                            </div>
                            <div class="card-metric-item">
                                <div class="card-metric-value">{format_number(post['likes'])}</div>
                                <div class="card-metric-label">Likes</div>
                            </div>
                            <div class="card-metric-item">
                                <div class="card-metric-value">{format_number(post['shares'])}</div>
                                <div class="card-metric-label">Shares</div>
                            </div>
                        </div>
                        <div class="card-metrics">
                            <div class="card-metric-item">
                                <div class="card-metric-value">{format_number(post['comments'])}</div>
                                <div class="card-metric-label">Comments</div>
                            </div>
                            <div class="card-metric-item">
                                <div class="card-metric-value">{format_number(post['saves'])}</div>
                                <div class="card-metric-label">Saves</div>
                            </div>
                            <div class="card-metric-item">
                                <div class="card-metric-value">{format_number(post['link_clicks'])}</div>
                                <div class="card-metric-label">Clicks</div>
                            </div>
                        </div>
                        <div class="card-scores">
                            <div class="score-badge score-badge-virality">
                                🔥 Virality: {post['virality_score']}%
                            </div>
                            <div class="score-badge score-badge-conversion">
                                🎯 Conv: {post['conversion_score']}%
                            </div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # Small spacer between rows
                st.markdown("<div style='height: 4px;'></div>", unsafe_allow_html=True)


def render_content_table(page_df, current_sort):
    """Render content as interactive table with clickable column headers."""

    # Column definitions
    columns = [
        {"key": "title", "label": "Content", "sortable": False},
        {"key": "views", "label": "Views", "sortable": True},
        {"key": "likes", "label": "Likes", "sortable": True},
        {"key": "comments", "label": "Comments", "sortable": True},
        {"key": "shares", "label": "Shares", "sortable": True},
        {"key": "saves", "label": "Saves", "sortable": True},
        {"key": "virality_score", "label": "Virality", "sortable": True},
        {"key": "conversion_score", "label": "Conv.", "sortable": True},
    ]

    # Determine active sort column
    sort_active_map = {
        "Virality Score ↓": "virality_score",
        "Conversion Score ↓": "conversion_score",
        "Views ↓": "views",
        "Likes ↓": "likes",
        "Most Recent": None,
    }
    active_sort_col = sort_active_map.get(current_sort)

    # Build table header
    header_cells = ""
    for col_def in columns:
        active_class = "active" if col_def["key"] == active_sort_col else ""
        sort_indicator = " ▼" if col_def["key"] == active_sort_col else ""
        header_cells += f'<div class="table-header-cell {active_class}">{col_def["label"]}{sort_indicator}</div>'

    st.markdown(f'<div class="table-header">{header_cells}</div>', unsafe_allow_html=True)

    # Build table rows
    for _, post in page_df.iterrows():
        platform = post["platform"]
        color = PLATFORM_COLORS.get(platform, "#444")
        icon = PLATFORM_ICONS.get(platform, "📄")

        # Virality color
        vs = post["virality_score"]
        vs_color = NEON_GREEN if vs >= 3.0 else (NEON_YELLOW if vs >= 1.5 else TEXT_PRIMARY)

        # Conversion color
        cs = post["conversion_score"]
        cs_color = NEON_GREEN if cs >= 2.0 else (NEON_YELLOW if cs >= 1.0 else TEXT_PRIMARY)

        st.markdown(f"""
        <div class="table-row">
            <div class="table-cell-title">
                <span class="table-platform-dot" style="background: {color};"></span>
                <span style="font-size: 11px;">{icon}</span>
                <span style="overflow: hidden; text-overflow: ellipsis; white-space: nowrap; font-size: 12px;">
                    {post['title']}
                </span>
                <span style="font-size: 9px; color: #5A6577; margin-left: 4px;">
                    {post['content_type']}
                </span>
            </div>
            <div>{format_number(post['views'])}</div>
            <div>{format_number(post['likes'])}</div>
            <div>{format_number(post['comments'])}</div>
            <div>{format_number(post['shares'])}</div>
            <div>{format_number(post['saves'])}</div>
            <div class="table-cell-score" style="color: {vs_color};">
                {post['virality_score']}%
            </div>
            <div class="table-cell-score" style="color: {cs_color};">
                {post['conversion_score']}%
            </div>
        </div>
        """, unsafe_allow_html=True)


def render_pagination(current_page, total_pages):
    """Render pagination controls with Previous/Next buttons."""

    col_prev, col_info, col_next = st.columns([1, 2, 1])

    with col_prev:
        if current_page > 1:
            if st.button("← Previous", key="page_prev", use_container_width=True):
                st.session_state.content_page = current_page - 1
                st.rerun()
        else:
            st.button("← Previous", key="page_prev_disabled", disabled=True, use_container_width=True)

    with col_info:
        # Page number buttons
        page_cols = st.columns(min(total_pages, 7))
        
        # Show at most 7 page buttons
        if total_pages <= 7:
            page_range = range(1, total_pages + 1)
        elif current_page <= 4:
            page_range = range(1, 8)
        elif current_page >= total_pages - 3:
            page_range = range(total_pages - 6, total_pages + 1)
        else:
            page_range = range(current_page - 3, current_page + 4)

        for idx, page_num in enumerate(page_range):
            if idx < len(page_cols):
                with page_cols[idx]:
                    btn_type = "primary" if page_num == current_page else "secondary"
                    if st.button(
                        str(page_num),
                        key=f"page_{page_num}",
                        type=btn_type,
                        use_container_width=True
                    ):
                        st.session_state.content_page = page_num
                        st.rerun()

    with col_next:
        if current_page < total_pages:
            if st.button("Next →", key="page_next", use_container_width=True):
                st.session_state.content_page = current_page + 1
                st.rerun()
        else:
            st.button("Next →", key="page_next_disabled", disabled=True, use_container_width=True)

def show_organic_architecture():
    """
    Main entry point for Module 2: Organic Architecture.
    Called from app.py navigation.
    """
    load_module2_css()

    # --- Module Header ---
    st.markdown("""
    <div style="margin-bottom: 24px;">
        <div class="module-title">📱 Organic Architecture</div>
        <div class="module-subtitle">
            The Brand Terminal — Measuring Brand Resonance, Community Loyalty & Traffic Contribution
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- Date Range Filter ---
    col_filter1, col_filter2, col_filter3 = st.columns([2, 2, 6])
    with col_filter1:
        date_range = st.selectbox(
            "📅 Time Range",
            ["Last 7 Days", "Last 14 Days", "Last 30 Days"],
            index=2,
            key="organic_date_range"
        )
    with col_filter2:
        platform_filter = st.multiselect(
            "🌐 Platforms",
            ["Instagram", "TikTok", "YouTube", "LinkedIn"],
            default=["Instagram", "TikTok", "YouTube", "LinkedIn"],
            key="organic_platform_filter"
        )

    # --- Generate Data ---
    days_map = {"Last 7 Days": 7, "Last 14 Days": 14, "Last 30 Days": 30}
    days = days_map.get(date_range, 30)

    df = generate_organic_data(days=30)  # Always generate 30 days

    # Filter by date range
    cutoff_date = datetime.now() - timedelta(days=days)
    df = df[df["date"] >= cutoff_date]

    # Filter by platform
    if platform_filter:
        df = df[df["platform"].isin(platform_filter)]

    if df.empty:
        st.warning("⚠️ No data available for selected filters.")
        return

    # --- Divider ---
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    # --- Section 1: Cross-Channel Pulse (Ticker Tape) ---
    render_cross_channel_pulse(df)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- Section 2: North Star Ribbon (KPI Metrics) ---
    render_north_star_ribbon(df)

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    # --- Section 3: Metric Stack (Depth & Traffic per Platform) ---
    render_metric_stack(df)

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    # --- Section 4: Follower Growth Trend Chart ---
    render_platform_overview_chart(df)

    # --- Section 5: Daily Engagement Rate Chart ---
    render_daily_engagement_chart(df)

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    # --- Section 6: Engagement Funnel (Community Health) ---
    render_engagement_funnel(df)

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    # --- Section 7: Content Leaderboard (Top 3 Posts) ---
    render_content_leaderboard(platform_filter)

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    # --- Section 8: Content Library Grid ---
    render_content_library(platform_filter)

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    # --- Section 9: AI Brain (The Community Manager) ---
    render_ai_brain(df, platform_filter)


# ============================================================
# 5. STANDALONE TEST MODE
# ============================================================

if __name__ == "__main__":
    st.set_page_config(
        page_title="Marktivo Growth OS — Organic Architecture",
        page_icon="📱",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    show_organic_architecture()
