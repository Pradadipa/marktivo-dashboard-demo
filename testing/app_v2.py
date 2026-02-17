"""
MARKTIVO GROWTH OS — MODULE 2: ORGANIC ARCHITECTURE
Section 1: The Data Architecture (The Aggregator)

View Mode 1: Cross-Channel Pulse (Ticker Tape - Net Follower Growth)
View Mode 2: Content Library (Thumbnail Grid - Sortable by Virality/Conversion Score)

Design: Dark Mode, Financial Terminal Aesthetic, Neon Accents
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import random
import json

# ─────────────────────────────────────────────
# PAGE CONFIG & THEME
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Marktivo Growth OS — Organic Architecture",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────
# CUSTOM CSS - Financial Terminal Dark Theme
# ─────────────────────────────────────────────
st.markdown("""
<style>
/* ===== ROOT VARIABLES ===== */
:root {
    --bg-primary: #0a0b0f;
    --bg-secondary: #11131a;
    --bg-card: #161822;
    --border: #1e2233;
    --text-primary: #e8eaf0;
    --text-secondary: #6b7394;
    --text-muted: #3d4466;
    --neon-green: #00ffaa;
    --neon-blue: #4d8eff;
    --neon-purple: #b44dff;
    --neon-pink: #ff4d8e;
    --neon-orange: #ff8c4d;
    --neon-cyan: #4dfff3;
    --positive: #00ffaa;
    --negative: #ff4d6a;
}

/* ===== GLOBAL ===== */
.stApp {
    background-color: var(--bg-primary) !important;
}

section[data-testid="stSidebar"] {
    background-color: var(--bg-secondary) !important;
}

/* Hide default streamlit elements */
#MainMenu, footer, header {visibility: hidden;}
.block-container {padding-top: 1.5rem !important; padding-bottom: 1rem !important;}

/* ===== MODULE HEADER ===== */
.module-header {
    padding: 20px 0 24px 0;
    border-bottom: 1px solid #1e2233;
    margin-bottom: 28px;
}
.module-tag {
    font-family: 'JetBrains Mono', 'Courier New', monospace;
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    color: #b44dff;
    background: rgba(180,77,255,0.12);
    padding: 5px 12px;
    border-radius: 4px;
    display: inline-block;
    margin-bottom: 10px;
}
.module-title {
    font-family: 'JetBrains Mono', 'Courier New', monospace;
    font-size: 26px;
    font-weight: 700;
    color: #e8eaf0;
    letter-spacing: -0.5px;
    margin: 0;
}
.module-title span { color: #b44dff; }
.module-subtitle {
    font-size: 13px;
    color: #6b7394;
    margin-top: 4px;
}
.live-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-family: 'JetBrains Mono', 'Courier New', monospace;
    font-size: 10px;
    color: #00ffaa;
    letter-spacing: 1.5px;
    float: right;
    margin-top: -40px;
}
.live-dot {
    width: 7px; height: 7px;
    background: #00ffaa;
    border-radius: 50%;
    display: inline-block;
    animation: pulse 2s ease-in-out infinite;
    box-shadow: 0 0 6px #00ffaa;
}
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.4; }
}

/* ===== SECTION LABEL ===== */
.section-label {
    font-family: 'JetBrains Mono', 'Courier New', monospace;
    font-size: 10px;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    color: #3d4466;
    margin-bottom: 16px;
    margin-top: 8px;
}

/* ===== TICKER CARDS (View Mode 1) ===== */
.ticker-card {
    background: #161822;
    border: 1px solid #1e2233;
    border-radius: 10px;
    padding: 20px;
    position: relative;
    overflow: hidden;
    transition: all 0.3s ease;
    height: 100%;
}
.ticker-card:hover {
    border-color: rgba(0,255,170,0.15);
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
}

/* Platform color bars */
.ticker-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
}
.ticker-card.instagram::before { background: linear-gradient(90deg, #f09433, #e6683c, #dc2743, #cc2366, #bc1888); }
.ticker-card.tiktok::before { background: linear-gradient(90deg, #00f2ea, #ff0050); }
.ticker-card.youtube::before { background: #ff0000; }
.ticker-card.linkedin::before { background: #0a66c2; }

.platform-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 14px;
}
.platform-info {
    display: flex;
    align-items: center;
    gap: 10px;
}
.platform-icon {
    width: 36px; height: 36px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
}
.icon-ig { background: linear-gradient(135deg, rgba(240,148,51,0.15), rgba(188,24,136,0.15)); }
.icon-tt { background: rgba(0,242,234,0.12); }
.icon-yt { background: rgba(255,0,0,0.1); }
.icon-li { background: rgba(10,102,194,0.12); }

.platform-name {
    font-family: 'JetBrains Mono', 'Courier New', monospace;
    font-size: 13px;
    font-weight: 600;
    color: #e8eaf0;
}
.platform-handle {
    font-size: 11px;
    color: #6b7394;
}
.status-badge {
    font-family: 'JetBrains Mono', 'Courier New', monospace;
    font-size: 10px;
    padding: 3px 8px;
    border-radius: 4px;
    letter-spacing: 0.5px;
}
.status-up { color: #00ffaa; background: rgba(0,255,170,0.12); }
.status-down { color: #ff4d6a; background: rgba(255,77,106,0.12); }

.followers-count {
    font-family: 'JetBrains Mono', 'Courier New', monospace;
    font-size: 30px;
    font-weight: 700;
    color: #e8eaf0;
    letter-spacing: -1px;
    margin: 2px 0;
}
.followers-label {
    font-size: 11px;
    color: #6b7394;
}
.growth-row {
    display: flex;
    gap: 20px;
    padding-top: 14px;
    border-top: 1px solid #1e2233;
    margin-top: 14px;
}
.growth-item { display: flex; flex-direction: column; gap: 1px; }
.growth-value {
    font-family: 'JetBrains Mono', 'Courier New', monospace;
    font-size: 14px;
    font-weight: 600;
}
.growth-value.positive { color: #00ffaa; }
.growth-value.negative { color: #ff4d6a; }
.growth-label {
    font-size: 10px;
    color: #3d4466;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}

/* ===== CONTENT LIBRARY CARDS (View Mode 2) ===== */
.content-card {
    background: #161822;
    border: 1px solid #1e2233;
    border-radius: 10px;
    overflow: hidden;
    transition: all 0.3s ease;
    height: 100%;
}
.content-card:hover {
    border-color: rgba(255,255,255,0.08);
    box-shadow: 0 12px 40px rgba(0,0,0,0.4);
    transform: translateY(-2px);
}
.content-thumb {
    width: 100%;
    aspect-ratio: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 42px;
    position: relative;
}
.thumb-ig { background: linear-gradient(135deg, #833ab4, #fd1d1d, #fcb045); }
.thumb-tt { background: linear-gradient(135deg, #010101, #00f2ea); }
.thumb-yt { background: linear-gradient(135deg, #1a1a2e, #ff0000); }
.thumb-li { background: linear-gradient(135deg, #0a2647, #0a66c2); }

.content-type-badge {
    position: absolute;
    top: 8px; left: 8px;
    font-family: 'JetBrains Mono', 'Courier New', monospace;
    font-size: 9px;
    letter-spacing: 1px;
    text-transform: uppercase;
    padding: 3px 8px;
    border-radius: 4px;
    background: rgba(0,0,0,0.6);
    color: #e8eaf0;
    backdrop-filter: blur(4px);
}
.content-platform-badge {
    position: absolute;
    top: 8px; right: 8px;
    font-size: 16px;
    background: rgba(0,0,0,0.5);
    border-radius: 6px;
    padding: 4px 6px;
    backdrop-filter: blur(4px);
}
.content-body {
    padding: 14px 16px 16px 16px;
}
.content-title {
    font-size: 13px;
    font-weight: 500;
    color: #e8eaf0;
    margin-bottom: 10px;
    line-height: 1.4;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}
.content-stats {
    display: flex;
    gap: 12px;
    flex-wrap: wrap;
}
.stat-item {
    display: flex;
    flex-direction: column;
    gap: 1px;
}
.stat-value {
    font-family: 'JetBrains Mono', 'Courier New', monospace;
    font-size: 13px;
    font-weight: 600;
    color: #e8eaf0;
}
.stat-label {
    font-size: 9px;
    color: #3d4466;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}
.score-row {
    display: flex;
    gap: 10px;
    margin-top: 12px;
    padding-top: 10px;
    border-top: 1px solid #1e2233;
}
.score-badge {
    font-family: 'JetBrains Mono', 'Courier New', monospace;
    font-size: 10px;
    padding: 3px 8px;
    border-radius: 4px;
    letter-spacing: 0.3px;
}
.score-virality { color: #b44dff; background: rgba(180,77,255,0.12); }
.score-conversion { color: #4d8eff; background: rgba(77,142,255,0.12); }

/* ===== RADIO BUTTON OVERRIDE ===== */
div[data-testid="stRadio"] > div {
    flex-direction: row !important;
    gap: 8px !important;
}
div[data-testid="stRadio"] label {
    background: #161822 !important;
    border: 1px solid #1e2233 !important;
    border-radius: 8px !important;
    padding: 8px 18px !important;
    font-family: 'JetBrains Mono', 'Courier New', monospace !important;
    font-size: 12px !important;
    letter-spacing: 0.5px !important;
    color: #6b7394 !important;
    transition: all 0.2s ease !important;
}
div[data-testid="stRadio"] label[data-checked="true"],
div[data-testid="stRadio"] label:has(input:checked) {
    background: rgba(180,77,255,0.12) !important;
    border-color: rgba(180,77,255,0.3) !important;
    color: #b44dff !important;
}

/* ===== SELECTBOX & MULTISELECT OVERRIDE ===== */
div[data-baseweb="select"] {
    background: #161822 !important;
}
div[data-baseweb="select"] > div {
    background: #161822 !important;
    border-color: #1e2233 !important;
    color: #e8eaf0 !important;
}

/* ===== TABS OVERRIDE ===== */
.stTabs [data-baseweb="tab-list"] {
    gap: 4px;
    background: #11131a;
    border-radius: 10px;
    padding: 4px;
    border: 1px solid #1e2233;
    width: fit-content;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px;
    padding: 8px 20px;
    font-family: 'JetBrains Mono', 'Courier New', monospace;
    font-size: 12px;
    letter-spacing: 0.5px;
    color: #6b7394;
    background: transparent;
}
.stTabs [aria-selected="true"] {
    background: rgba(180,77,255,0.12) !important;
    color: #b44dff !important;
}
.stTabs [data-baseweb="tab-highlight"] { display: none; }
.stTabs [data-baseweb="tab-border"] { display: none; }

/* ===== METRIC OVERRIDE ===== */
[data-testid="stMetric"] {
    background: #161822;
    border: 1px solid #1e2233;
    border-radius: 10px;
    padding: 16px 20px;
}
[data-testid="stMetricLabel"] {
    font-family: 'JetBrains Mono', 'Courier New', monospace !important;
    font-size: 10px !important;
    letter-spacing: 1.5px !important;
    text-transform: uppercase !important;
    color: #3d4466 !important;
}
[data-testid="stMetricValue"] {
    font-family: 'JetBrains Mono', 'Courier New', monospace !important;
    color: #e8eaf0 !important;
}
[data-testid="stMetricDelta"] {
    font-family: 'JetBrains Mono', 'Courier New', monospace !important;
}

/* ===== DIVIDER ===== */
hr { border-color: #1e2233 !important; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# SAMPLE DATA (Replace with real API data)
# ─────────────────────────────────────────────

def get_platform_data():
    """Simulated cross-channel follower data. Replace with real API calls."""
    return {
        "instagram": {
            "name": "Instagram",
            "handle": "@marktivo",
            "icon": "📸",
            "icon_class": "icon-ig",
            "card_class": "instagram",
            "thumb_class": "thumb-ig",
            "followers": 48_520,
            "net_change_7d": +1_230,
            "net_change_30d": +4_870,
            "pct_change_7d": +2.6,
            "pct_change_30d": +11.2,
            "sparkline": [45_800, 46_100, 46_500, 46_900, 47_200, 47_600, 47_900, 48_100, 48_300, 48_520],
            "status": "up",
        },
        "tiktok": {
            "name": "TikTok",
            "handle": "@marktivo",
            "icon": "🎵",
            "icon_class": "icon-tt",
            "card_class": "tiktok",
            "thumb_class": "thumb-tt",
            "followers": 125_400,
            "net_change_7d": +5_620,
            "net_change_30d": +22_100,
            "pct_change_7d": +4.7,
            "pct_change_30d": +21.4,
            "sparkline": [103_000, 106_200, 109_800, 113_500, 116_000, 119_300, 121_800, 123_500, 124_200, 125_400],
            "status": "up",
        },
        "youtube": {
            "name": "YouTube",
            "handle": "@MarktivoHQ",
            "icon": "▶️",
            "icon_class": "icon-yt",
            "card_class": "youtube",
            "thumb_class": "thumb-yt",
            "followers": 12_870,
            "net_change_7d": -140,
            "net_change_30d": +890,
            "pct_change_7d": -1.1,
            "pct_change_30d": +7.4,
            "sparkline": [12_000, 12_200, 12_500, 12_700, 12_900, 13_010, 12_990, 12_920, 12_880, 12_870],
            "status": "down",
        },
        "linkedin": {
            "name": "LinkedIn",
            "handle": "Marktivo Growth",
            "icon": "💼",
            "icon_class": "icon-li",
            "card_class": "linkedin",
            "thumb_class": "thumb-li",
            "followers": 6_340,
            "net_change_7d": +310,
            "net_change_30d": +1_220,
            "pct_change_7d": +5.1,
            "pct_change_30d": +23.8,
            "sparkline": [5_100, 5_250, 5_420, 5_600, 5_780, 5_900, 6_050, 6_150, 6_260, 6_340],
            "status": "up",
        },
    }


def get_content_library():
    """Simulated content library. Replace with real social media API data."""
    posts = [
        {
            "id": 1, "platform": "Instagram", "platform_icon": "📸", "thumb_class": "thumb-ig",
            "type": "Reel", "title": "5 Growth Hacks Your Competitors Don't Want You to Know",
            "date": "2025-02-08", "views": 245_000, "clicks": 3_200,
            "likes": 12_400, "comments": 890, "shares": 2_100, "saves": 4_300,
            "virality_score": 92, "conversion_score": 78,
        },
        {
            "id": 2, "platform": "TikTok", "platform_icon": "🎵", "thumb_class": "thumb-tt",
            "type": "Video", "title": "POV: You finally understand ROAS 💀",
            "date": "2025-02-07", "views": 1_200_000, "clicks": 8_500,
            "likes": 85_200, "comments": 4_300, "shares": 12_600, "saves": 9_800,
            "virality_score": 98, "conversion_score": 65,
        },
        {
            "id": 3, "platform": "YouTube", "platform_icon": "▶️", "thumb_class": "thumb-yt",
            "type": "Short", "title": "The $0 Marketing Strategy That Made Us $50K",
            "date": "2025-02-06", "views": 89_000, "clicks": 5_100,
            "likes": 4_200, "comments": 620, "shares": 890, "saves": 1_500,
            "virality_score": 72, "conversion_score": 88,
        },
        {
            "id": 4, "platform": "Instagram", "platform_icon": "📸", "thumb_class": "thumb-ig",
            "type": "Carousel", "title": "The Ultimate Guide to LTV:CAC Ratio (Save This)",
            "date": "2025-02-05", "views": 67_000, "clicks": 4_800,
            "likes": 5_600, "comments": 1_240, "shares": 3_400, "saves": 8_200,
            "virality_score": 85, "conversion_score": 91,
        },
        {
            "id": 5, "platform": "TikTok", "platform_icon": "🎵", "thumb_class": "thumb-tt",
            "type": "Video", "title": "Stop wasting money on TOF ads. Here's why ⬇️",
            "date": "2025-02-04", "views": 520_000, "clicks": 2_100,
            "likes": 32_100, "comments": 2_800, "shares": 5_400, "saves": 3_200,
            "virality_score": 88, "conversion_score": 42,
        },
        {
            "id": 6, "platform": "LinkedIn", "platform_icon": "💼", "thumb_class": "thumb-li",
            "type": "Article", "title": "Why Your Agency is Lying About Your ROAS Numbers",
            "date": "2025-02-03", "views": 18_500, "clicks": 6_200,
            "likes": 1_240, "comments": 380, "shares": 620, "saves": 290,
            "virality_score": 55, "conversion_score": 95,
        },
        {
            "id": 7, "platform": "YouTube", "platform_icon": "▶️", "thumb_class": "thumb-yt",
            "type": "Long-form", "title": "Full Funnel Breakdown: How We Scaled to $200K/mo",
            "date": "2025-02-02", "views": 42_000, "clicks": 7_800,
            "likes": 3_800, "comments": 920, "shares": 1_100, "saves": 2_400,
            "virality_score": 68, "conversion_score": 94,
        },
        {
            "id": 8, "platform": "Instagram", "platform_icon": "📸", "thumb_class": "thumb-ig",
            "type": "Story", "title": "Behind the scenes: Our Q1 planning session",
            "date": "2025-02-01", "views": 32_000, "clicks": 1_800,
            "likes": 2_100, "comments": 140, "shares": 320, "saves": 180,
            "virality_score": 45, "conversion_score": 52,
        },
    ]
    return pd.DataFrame(posts)


def format_number(n):
    """Format large numbers with K/M suffix."""
    if n >= 1_000_000:
        return f"{n/1_000_000:.1f}M"
    elif n >= 1_000:
        return f"{n/1_000:.1f}K"
    return str(n)


def create_sparkline(data, color="#00ffaa"):
    """Create a minimal sparkline chart using Plotly."""
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        y=data,
        mode="lines",
        line=dict(color=color, width=2),
        fill="tozeroy",
        fillcolor=f"rgba({','.join(str(int(color.lstrip('#')[i:i+2], 16)) for i in (0, 2, 4))},0.08)",
        hoverinfo="skip",
    ))
    fig.update_layout(
        height=50,
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        showlegend=False,
    )
    return fig


# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div class="module-header">
    <div class="module-tag">MODULE 2 — ORGANIC ARCHITECTURE</div>
    <h1 class="module-title">The Data Architecture <span>// The Aggregator</span></h1>
    <p class="module-subtitle">Brand Resonance • Community Loyalty • Traffic Contribution</p>
    <div class="live-badge"><span class="live-dot"></span> LIVE SYNC</div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# VIEW MODE TOGGLE
# ─────────────────────────────────────────────
view_mode = st.tabs(["📡  Cross-Channel Pulse", "📚  Content Library"])


# ═══════════════════════════════════════════════
# VIEW MODE 1: CROSS-CHANNEL PULSE (Ticker Tape)
# ═══════════════════════════════════════════════
with view_mode[0]:
    st.markdown('<div class="section-label">NET FOLLOWER GROWTH — ALL PLATFORMS — 7D / 30D</div>', unsafe_allow_html=True)

    platforms = get_platform_data()

    # ── Total Summary Row ──
    total_followers = sum(p["followers"] for p in platforms.values())
    total_7d = sum(p["net_change_7d"] for p in platforms.values())
    total_30d = sum(p["net_change_30d"] for p in platforms.values())

    summary_cols = st.columns(4)
    with summary_cols[0]:
        st.metric("Total Followers", format_number(total_followers), f"+{format_number(total_7d)} (7d)")
    with summary_cols[1]:
        st.metric("Net Growth (7D)", f"+{format_number(total_7d)}", f"{total_7d/total_followers*100:.1f}%")
    with summary_cols[2]:
        st.metric("Net Growth (30D)", f"+{format_number(total_30d)}", f"{total_30d/total_followers*100:.1f}%")
    with summary_cols[3]:
        best = max(platforms.items(), key=lambda x: x[1]["pct_change_7d"])
        st.metric("Top Grower (7D)", best[1]["name"], f"+{best[1]['pct_change_7d']}%")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Ticker Tape Cards ──
    st.markdown('<div class="section-label">PLATFORM BREAKDOWN — TICKER TAPE</div>', unsafe_allow_html=True)

    cols = st.columns(4, gap="medium")

    sparkline_colors = {
        "instagram": "#e6683c",
        "tiktok": "#00f2ea",
        "youtube": "#ff0000",
        "linkedin": "#0a66c2",
    }

    for idx, (key, p) in enumerate(platforms.items()):
        with cols[idx]:
            sign_7d = "+" if p["net_change_7d"] >= 0 else ""
            sign_30d = "+" if p["net_change_30d"] >= 0 else ""
            status_class = "status-up" if p["status"] == "up" else "status-down"
            status_text = "▲ GROWING" if p["status"] == "up" else "▼ DECLINING"
            val_7d_class = "positive" if p["net_change_7d"] >= 0 else "negative"
            val_30d_class = "positive" if p["net_change_30d"] >= 0 else "negative"

            st.markdown(f"""
            <div class="ticker-card {p['card_class']}">
                <div class="platform-row">
                    <div class="platform-info">
                        <div class="platform-icon {p['icon_class']}">{p['icon']}</div>
                        <div>
                            <div class="platform-name">{p['name']}</div>
                            <div class="platform-handle">{p['handle']}</div>
                        </div>
                    </div>
                    <div class="status-badge {status_class}">{status_text}</div>
                </div>
                <div class="followers-count">{format_number(p['followers'])}</div>
                <div class="followers-label">Total Followers</div>
            </div>
            """, unsafe_allow_html=True)

            # Sparkline chart
            fig = create_sparkline(p["sparkline"], sparkline_colors[key])
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

            # Growth stats
            st.markdown(f"""
            <div class="growth-row">
                <div class="growth-item">
                    <div class="growth-value {val_7d_class}">{sign_7d}{format_number(abs(p['net_change_7d']))}</div>
                    <div class="growth-label">7-Day Net</div>
                </div>
                <div class="growth-item">
                    <div class="growth-value {val_30d_class}">{sign_30d}{format_number(abs(p['net_change_30d']))}</div>
                    <div class="growth-label">30-Day Net</div>
                </div>
                <div class="growth-item">
                    <div class="growth-value {val_7d_class}">{sign_7d}{p['pct_change_7d']}%</div>
                    <div class="growth-label">7D %</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Follower Growth Comparison Chart ──
    st.markdown('<div class="section-label">FOLLOWER GROWTH TRENDLINE — LAST 10 PERIODS</div>', unsafe_allow_html=True)

    fig_trend = go.Figure()
    for key, p in platforms.items():
        fig_trend.add_trace(go.Scatter(
            y=p["sparkline"],
            name=p["name"],
            mode="lines+markers",
            line=dict(color=sparkline_colors[key], width=2),
            marker=dict(size=4),
        ))

    fig_trend.update_layout(
        height=300,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="JetBrains Mono, Courier New, monospace", color="#6b7394", size=11),
        legend=dict(
            orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0,
            font=dict(size=11, color="#6b7394"),
            bgcolor="rgba(0,0,0,0)",
        ),
        xaxis=dict(
            showgrid=True, gridcolor="rgba(30,34,51,0.5)", zeroline=False,
            tickfont=dict(color="#3d4466"),
        ),
        yaxis=dict(
            showgrid=True, gridcolor="rgba(30,34,51,0.5)", zeroline=False,
            tickfont=dict(color="#3d4466"),
        ),
        margin=dict(l=20, r=20, t=40, b=20),
        hovermode="x unified",
    )
    st.plotly_chart(fig_trend, use_container_width=True, config={"displayModeBar": False})


# ═══════════════════════════════════════════════
# VIEW MODE 2: CONTENT LIBRARY (Thumbnail Grid)
# ═══════════════════════════════════════════════
with view_mode[1]:
    st.markdown('<div class="section-label">CONTENT PERFORMANCE LIBRARY — SORTABLE</div>', unsafe_allow_html=True)

    # ── Controls ──
    ctrl_cols = st.columns([2, 2, 2, 6])
    with ctrl_cols[0]:
        sort_by = st.selectbox(
            "Sort By",
            ["🔥 Virality Score (Views)", "🎯 Conversion Score (Clicks)"],
            label_visibility="collapsed",
        )
    with ctrl_cols[1]:
        platform_filter = st.multiselect(
            "Platform",
            ["Instagram", "TikTok", "YouTube", "LinkedIn"],
            default=["Instagram", "TikTok", "YouTube", "LinkedIn"],
            label_visibility="collapsed",
        )
    with ctrl_cols[2]:
        content_type_filter = st.multiselect(
            "Type",
            ["Reel", "Video", "Short", "Carousel", "Story", "Article", "Long-form"],
            default=["Reel", "Video", "Short", "Carousel", "Story", "Article", "Long-form"],
            label_visibility="collapsed",
        )

    df = get_content_library()

    # Apply filters
    df = df[df["platform"].isin(platform_filter)]
    if content_type_filter:
        df = df[df["type"].isin(content_type_filter)]

    # Apply sort
    if "Virality" in sort_by:
        df = df.sort_values("virality_score", ascending=False)
    else:
        df = df.sort_values("conversion_score", ascending=False)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Grid of Content Cards ──
    grid_cols = st.columns(4, gap="medium")

    for idx, (_, post) in enumerate(df.iterrows()):
        col = grid_cols[idx % 4]
        with col:
            st.markdown(f"""
            <div class="content-card">
                <div class="content-thumb {post['thumb_class']}">
                    <span style="font-size: 36px; opacity: 0.6;">
                        {post['platform_icon']}
                    </span>
                    <div class="content-type-badge">{post['type']}</div>
                    <div class="content-platform-badge">{post['platform_icon']}</div>
                </div>
                <div class="content-body">
                    <div class="content-title">{post['title']}</div>
                    <div class="content-stats">
                        <div class="stat-item">
                            <div class="stat-value">{format_number(post['views'])}</div>
                            <div class="stat-label">Views</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-value">{format_number(post['clicks'])}</div>
                            <div class="stat-label">Clicks</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-value">{format_number(post['likes'])}</div>
                            <div class="stat-label">Likes</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-value">{format_number(post['shares'])}</div>
                            <div class="stat-label">Shares</div>
                        </div>
                    </div>
                    <div class="score-row">
                        <div class="score-badge score-virality">🔥 Virality: {post['virality_score']}</div>
                        <div class="score-badge score-conversion">🎯 Conv: {post['conversion_score']}</div>
                    </div>
                </div>
            </div>
            <br>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Content Performance Scatter Plot ──
    st.markdown('<div class="section-label">VIRALITY vs CONVERSION SCORE — CONTENT MAP</div>', unsafe_allow_html=True)

    df_all = get_content_library()

    platform_colors = {
        "Instagram": "#e6683c",
        "TikTok": "#00f2ea",
        "YouTube": "#ff0000",
        "LinkedIn": "#0a66c2",
    }

    fig_scatter = go.Figure()
    for platform, color in platform_colors.items():
        df_p = df_all[df_all["platform"] == platform]
        if not df_p.empty:
            fig_scatter.add_trace(go.Scatter(
                x=df_p["virality_score"],
                y=df_p["conversion_score"],
                mode="markers+text",
                name=platform,
                marker=dict(
                    color=color,
                    size=df_p["views"].apply(lambda v: max(10, min(35, v / 40_000))),
                    opacity=0.85,
                    line=dict(width=1, color="rgba(255,255,255,0.1)"),
                ),
                text=df_p["type"],
                textposition="top center",
                textfont=dict(size=9, color="#6b7394"),
                hovertemplate=(
                    "<b>%{customdata[0]}</b><br>"
                    "Virality: %{x}<br>"
                    "Conversion: %{y}<br>"
                    "Views: %{customdata[1]}<br>"
                    "<extra></extra>"
                ),
                customdata=list(zip(df_p["title"], df_p["views"].apply(format_number))),
            ))

    # Quadrant lines
    fig_scatter.add_hline(y=70, line_dash="dot", line_color="#1e2233", line_width=1)
    fig_scatter.add_vline(x=70, line_dash="dot", line_color="#1e2233", line_width=1)

    # Quadrant labels
    annotations = [
        dict(x=85, y=95, text="⭐ UNICORN", showarrow=False, font=dict(color="#00ffaa", size=10)),
        dict(x=85, y=35, text="👀 VIRAL ONLY", showarrow=False, font=dict(color="#b44dff", size=10)),
        dict(x=40, y=95, text="💰 CONVERTER", showarrow=False, font=dict(color="#4d8eff", size=10)),
        dict(x=40, y=35, text="💤 LOW IMPACT", showarrow=False, font=dict(color="#3d4466", size=10)),
    ]

    fig_scatter.update_layout(
        height=400,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="JetBrains Mono, Courier New, monospace", color="#6b7394", size=11),
        xaxis=dict(
            title="Virality Score (Views-based)",
            showgrid=True, gridcolor="rgba(30,34,51,0.5)", zeroline=False,
            tickfont=dict(color="#3d4466"), range=[20, 100],
        ),
        yaxis=dict(
            title="Conversion Score (Clicks-based)",
            showgrid=True, gridcolor="rgba(30,34,51,0.5)", zeroline=False,
            tickfont=dict(color="#3d4466"), range=[20, 100],
        ),
        legend=dict(
            orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0,
            font=dict(size=11, color="#6b7394"), bgcolor="rgba(0,0,0,0)",
        ),
        margin=dict(l=20, r=20, t=40, b=40),
        annotations=annotations,
    )
    st.plotly_chart(fig_scatter, use_container_width=True, config={"displayModeBar": False})


# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("""
<div style="
    text-align: center;
    padding: 24px 0 12px 0;
    border-top: 1px solid #1e2233;
    margin-top: 32px;
">
    <span style="
        font-family: 'JetBrains Mono', monospace;
        font-size: 10px;
        letter-spacing: 2px;
        color: #3d4466;
    ">
        MARKTIVO GROWTH OS v2.0 — ORGANIC ARCHITECTURE MODULE — DATA REFRESHED EVERY 6H
    </span>
</div>
""", unsafe_allow_html=True)
