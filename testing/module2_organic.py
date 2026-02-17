"""
MODULE 2: ORGANIC ARCHITECTURE (The Brand Terminal)
Mission: Measure Brand Resonance, Community Loyalty, and Traffic Contribution.
Platforms: Instagram, TikTok, YouTube, LinkedIn

HARI 1: Foundation & Data Layer
- Setup & Dark Mode Config
- Dummy Data Generator (4 platforms × 30 days)
- Cross-Channel Pulse (Ticker Tape)
- North Star Ribbon (KPI Metrics)
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


def inject_custom_css():
    """Inject dark mode CSS styling - Financial Terminal Aesthetic"""
    st.markdown("""
    <style>
        /* Main Background */
        .stApp {
            background-color: #0E1117;
        }
        
        /* Ticker Tape Container */
        .ticker-container {
            display: flex;
            gap: 12px;
            overflow-x: auto;
            padding: 8px 0;
        }
        
        .ticker-card {
            background: linear-gradient(135deg, #1B1F2B 0%, #252A3A 100%);
            border: 1px solid #2D3348;
            border-radius: 12px;
            padding: 16px 20px;
            min-width: 200px;
            flex: 1;
            text-align: center;
            transition: all 0.3s ease;
        }
        
        .ticker-card:hover {
            border-color: #00D4FF;
            box-shadow: 0 0 15px rgba(0, 212, 255, 0.15);
            transform: translateY(-2px);
        }
        
        .ticker-platform {
            font-size: 12px;
            color: #8892A0;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            margin-bottom: 4px;
        }
        
        .ticker-followers {
            font-size: 24px;
            font-weight: 700;
            color: #FFFFFF;
            margin-bottom: 2px;
        }
        
        .ticker-growth-positive {
            font-size: 14px;
            font-weight: 600;
            color: #00FF88;
        }
        
        .ticker-growth-negative {
            font-size: 14px;
            font-weight: 600;
            color: #FF3B5C;
        }
        
        /* KPI Metric Card */
        .kpi-card {
            background: linear-gradient(135deg, #1B1F2B 0%, #252A3A 100%);
            border: 1px solid #2D3348;
            border-radius: 12px;
            padding: 20px;
            text-align: center;
            position: relative;
            overflow: hidden;
        }
        
        .kpi-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            border-radius: 12px 12px 0 0;
        }
        
        .kpi-label {
            font-size: 11px;
            color: #8892A0;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            margin-bottom: 6px;
        }
        
        .kpi-value {
            font-size: 28px;
            font-weight: 700;
            color: #FFFFFF;
            margin-bottom: 4px;
        }
        
        .kpi-benchmark {
            font-size: 11px;
            color: #5A6577;
        }
        
        .kpi-status-good {
            color: #00FF88;
        }
        
        .kpi-status-warning {
            color: #FFD700;
        }
        
        .kpi-status-bad {
            color: #FF3B5C;
        }
        
        /* Section Headers */
        .section-header {
            font-size: 14px;
            color: #8892A0;
            text-transform: uppercase;
            letter-spacing: 2px;
            padding-bottom: 8px;
            border-bottom: 1px solid #2D3348;
            margin-bottom: 16px;
            margin-top: 24px;
        }
        
        /* Module Title */
        .module-title {
            font-size: 32px;
            font-weight: 700;
            color: #FFFFFF;
            margin-bottom: 4px;
        }
        
        .module-subtitle {
            font-size: 14px;
            color: #8892A0;
            margin-bottom: 24px;
        }
        
        /* Date Filter Bar */
        .date-bar {
            background: #1B1F2B;
            border: 1px solid #2D3348;
            border-radius: 8px;
            padding: 10px 16px;
            margin-bottom: 20px;
        }

        /* Divider */
        .custom-divider {
            height: 1px;
            background: linear-gradient(to right, transparent, #2D3348, transparent);
            margin: 24px 0;
        }
    </style>
    """, unsafe_allow_html=True)


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
def generate_content_library(num_posts=30):
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

        posts.append({
            "post_id": f"POST-{i+1:03d}",
            "title": post_titles[i],
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
# 4. MAIN PAGE FUNCTION (Entry Point)
# ============================================================

def show_organic_architecture():
    """
    Main entry point for Module 2: Organic Architecture.
    Called from app.py navigation.
    """
    inject_custom_css()

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

    # --- Section 3: Follower Growth Trend Chart ---
    render_platform_overview_chart(df)

    # --- Section 4: Daily Engagement Rate Chart ---
    render_daily_engagement_chart(df)

    # --- Placeholder for Day 2-4 components ---
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align: center; padding: 40px; color: #5A6577;">
        <div style="font-size: 24px; margin-bottom: 8px;">🚧</div>
        <div style="font-size: 13px; text-transform: uppercase; letter-spacing: 2px;">
            More sections coming: Metric Stack · Engagement Funnel · Content Library · AI Brain
        </div>
    </div>
    """, unsafe_allow_html=True)


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
