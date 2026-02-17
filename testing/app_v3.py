"""
MARKTIVO GROWTH OS — MODULE 2: ORGANIC ARCHITECTURE
Section: The Data Architecture (The Aggregator)
- View Mode 1: Cross-Channel Pulse (Ticker Tape)
- View Mode 2: Content Library (Table with Thumbnails)
"""

import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta

# ──────────────────────────────────────────────
# PAGE CONFIG & DARK THEME
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="Marktivo Growth OS — Organic Architecture",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ──────────────────────────────────────────────
# CUSTOM CSS — "Financial Terminal" Dark Aesthetic
# ──────────────────────────────────────────────
st.markdown("""
<style>
    /* ── Global ── */
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&family=Inter:wght@400;500;600;700&display=swap');

    :root {
        --bg-primary: #0a0e17;
        --bg-card: #111827;
        --bg-card-hover: #1a2235;
        --border: #1e2a3a;
        --text-primary: #e2e8f0;
        --text-secondary: #8892a4;
        --text-muted: #4a5568;
        --neon-cyan: #00f0ff;
        --neon-green: #00ff88;
        --neon-red: #ff3b5c;
        --neon-purple: #a855f7;
        --neon-orange: #ff8c00;
        --neon-pink: #ff006e;
        --neon-yellow: #facc15;
    }

    .stApp {
        background-color: var(--bg-primary) !important;
        color: var(--text-primary) !important;
        font-family: 'Inter', sans-serif !important;
    }

    /* Hide default streamlit elements */
    #MainMenu, footer, header {visibility: hidden;}
    .stDeployButton {display: none;}

    /* ── Section Header ── */
    .section-header {
        font-family: 'JetBrains Mono', monospace;
        font-size: 13px;
        font-weight: 500;
        color: var(--neon-cyan);
        letter-spacing: 3px;
        text-transform: uppercase;
        margin-bottom: 4px;
    }
    .section-title {
        font-family: 'Inter', sans-serif;
        font-size: 28px;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 6px;
    }
    .section-subtitle {
        font-size: 14px;
        color: var(--text-secondary);
        margin-bottom: 28px;
    }

    /* ── View Mode Toggle ── */
    .view-toggle-container {
        display: flex;
        gap: 0;
        margin-bottom: 24px;
        border: 1px solid var(--border);
        border-radius: 8px;
        overflow: hidden;
        width: fit-content;
    }
    
    /* ── Ticker Tape (View Mode 1) ── */
    .ticker-container {
        display: flex;
        gap: 16px;
        overflow-x: auto;
        padding: 4px 0;
    }
    .ticker-card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 20px 24px;
        min-width: 220px;
        flex: 1;
        transition: all 0.2s ease;
        position: relative;
        overflow: hidden;
    }
    .ticker-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        border-radius: 12px 12px 0 0;
    }
    .ticker-card.instagram::before { background: linear-gradient(90deg, #f09433, #e6683c, #dc2743, #cc2366, #bc1888); }
    .ticker-card.tiktok::before    { background: var(--neon-cyan); }
    .ticker-card.youtube::before   { background: var(--neon-red); }
    .ticker-card.linkedin::before  { background: #0a66c2; }

    .ticker-platform {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 14px;
    }
    .ticker-platform-icon {
        font-size: 22px;
        width: 36px;
        height: 36px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: rgba(255,255,255,0.05);
        border-radius: 8px;
    }
    .ticker-platform-name {
        font-family: 'Inter', sans-serif;
        font-size: 14px;
        font-weight: 600;
        color: var(--text-primary);
    }
    .ticker-followers {
        font-family: 'JetBrains Mono', monospace;
        font-size: 26px;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 6px;
    }
    .ticker-growth {
        font-family: 'JetBrains Mono', monospace;
        font-size: 15px;
        font-weight: 600;
        display: inline-flex;
        align-items: center;
        gap: 4px;
        padding: 3px 10px;
        border-radius: 6px;
    }
    .ticker-growth.positive {
        color: var(--neon-green);
        background: rgba(0, 255, 136, 0.1);
    }
    .ticker-growth.negative {
        color: var(--neon-red);
        background: rgba(255, 59, 92, 0.1);
    }
    .ticker-period {
        font-size: 12px;
        color: var(--text-muted);
        margin-top: 8px;
        font-family: 'JetBrains Mono', monospace;
    }

    /* ── Content Library Table (View Mode 2) ── */
    .content-table-wrapper {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 12px;
        overflow: hidden;
    }
    .content-table {
        width: 100%;
        border-collapse: separate;
        border-spacing: 0;
        font-size: 13px;
    }
    .content-table thead th {
        background: #0d1525;
        color: var(--text-secondary);
        font-family: 'JetBrains Mono', monospace;
        font-size: 11px;
        font-weight: 500;
        letter-spacing: 1px;
        text-transform: uppercase;
        padding: 14px 16px;
        text-align: left;
        border-bottom: 1px solid var(--border);
        position: sticky;
        top: 0;
        white-space: nowrap;
    }
    .content-table thead th.metric-col {
        text-align: right;
    }
    .content-table tbody tr {
        transition: background 0.15s ease;
    }
    .content-table tbody tr:hover {
        background: var(--bg-card-hover);
    }
    .content-table tbody td {
        padding: 14px 16px;
        border-bottom: 1px solid rgba(30,42,58,0.5);
        color: var(--text-primary);
        vertical-align: middle;
    }
    .content-table tbody td.metric-col {
        text-align: right;
        font-family: 'JetBrains Mono', monospace;
        font-size: 13px;
    }

    /* Thumbnail cell */
    .post-cell {
        display: flex;
        align-items: center;
        gap: 14px;
    }
    .post-thumbnail {
        width: 56px;
        height: 56px;
        border-radius: 8px;
        object-fit: cover;
        border: 1px solid var(--border);
        flex-shrink: 0;
    }
    .post-info {
        display: flex;
        flex-direction: column;
        gap: 3px;
    }
    .post-title {
        font-weight: 600;
        font-size: 13px;
        color: var(--text-primary);
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        max-width: 200px;
    }
    .post-meta {
        font-size: 11px;
        color: var(--text-muted);
        display: flex;
        align-items: center;
        gap: 8px;
    }

    /* Platform badge */
    .platform-badge {
        font-size: 10px;
        font-weight: 600;
        padding: 2px 8px;
        border-radius: 4px;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        font-family: 'JetBrains Mono', monospace;
    }
    .platform-badge.ig   { background: rgba(225,48,108,0.15); color: #e1306c; }
    .platform-badge.tt   { background: rgba(0,240,255,0.1);  color: var(--neon-cyan); }
    .platform-badge.yt   { background: rgba(255,59,92,0.1);  color: var(--neon-red); }
    .platform-badge.li   { background: rgba(10,102,194,0.15); color: #5b9bd5; }

    /* Score badges */
    .score-badge {
        font-family: 'JetBrains Mono', monospace;
        font-weight: 700;
        font-size: 13px;
        padding: 4px 10px;
        border-radius: 6px;
        display: inline-block;
    }
    .score-badge.high   { background: rgba(0,255,136,0.12); color: var(--neon-green); }
    .score-badge.medium { background: rgba(250,204,21,0.12); color: var(--neon-yellow); }
    .score-badge.low    { background: rgba(255,59,92,0.1);  color: var(--neon-red); }

    /* Engagement rate color */
    .er-value.good { color: var(--neon-green); }
    .er-value.avg  { color: var(--neon-yellow); }
    .er-value.bad  { color: var(--neon-red); }

    /* ── Sort Button Styles ── */
    .sort-pills {
        display: flex;
        gap: 8px;
        margin-bottom: 16px;
    }
    .sort-pill {
        font-family: 'JetBrains Mono', monospace;
        font-size: 11px;
        padding: 6px 14px;
        border-radius: 6px;
        border: 1px solid var(--border);
        background: transparent;
        color: var(--text-secondary);
        cursor: pointer;
        letter-spacing: 0.5px;
    }
    .sort-pill.active {
        border-color: var(--neon-cyan);
        color: var(--neon-cyan);
        background: rgba(0,240,255,0.08);
    }

    /* ── Streamlit overrides ── */
    .stRadio > div { flex-direction: row !important; gap: 0 !important; }
    .stRadio > div > label {
        background: var(--bg-card) !important;
        border: 1px solid var(--border) !important;
        color: var(--text-secondary) !important;
        padding: 8px 20px !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 12px !important;
        letter-spacing: 1px !important;
        cursor: pointer !important;
        margin: 0 !important;
        border-radius: 0 !important;
    }
    .stRadio > div > label:first-child { border-radius: 8px 0 0 8px !important; }
    .stRadio > div > label:last-child  { border-radius: 0 8px 8px 0 !important; }
    .stRadio > div > label[data-checked="true"],
    .stRadio > div > label:has(input:checked) {
        background: rgba(0,240,255,0.08) !important;
        border-color: var(--neon-cyan) !important;
        color: var(--neon-cyan) !important;
    }
    div[data-baseweb="select"] > div {
        background: var(--bg-card) !important;
        border-color: var(--border) !important;
        color: var(--text-primary) !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 12px !important;
    }
    .stSelectbox label {
        color: var(--text-secondary) !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 11px !important;
        letter-spacing: 1px !important;
        text-transform: uppercase !important;
    }

    /* ── Divider ── */
    .terminal-divider {
        border: none;
        border-top: 1px solid var(--border);
        margin: 32px 0;
    }
</style>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────
# DUMMY DATA GENERATION
# ──────────────────────────────────────────────

# -- Ticker Data (View Mode 1) --
TICKER_DATA = [
    {
        "platform": "Instagram",
        "icon": "📸",
        "css_class": "instagram",
        "followers": 48_520,
        "growth": +1_234,
        "growth_pct": +2.6,
    },
    {
        "platform": "TikTok",
        "icon": "🎵",
        "css_class": "tiktok",
        "followers": 127_800,
        "growth": +5_670,
        "growth_pct": +4.6,
    },
    {
        "platform": "YouTube",
        "icon": "▶️",
        "css_class": "youtube",
        "followers": 15_300,
        "growth": -120,
        "growth_pct": -0.8,
    },
    {
        "platform": "LinkedIn",
        "icon": "💼",
        "css_class": "linkedin",
        "followers": 9_840,
        "growth": +312,
        "growth_pct": +3.3,
    },
]


def format_number(n: int) -> str:
    """Format large numbers with K/M suffix."""
    if abs(n) >= 1_000_000:
        return f"{n / 1_000_000:.1f}M"
    if abs(n) >= 1_000:
        return f"{n / 1_000:.1f}K"
    return str(n)


# -- Content Library Data (View Mode 2) --
CONTENT_POSTS = [
    {
        "title": "Summer Sale Launch — 50% OFF 🔥",
        "platform": "Instagram",
        "platform_code": "ig",
        "type": "Reel",
        "date": "2025-02-03",
        "thumbnail": "https://placehold.co/112x112/1a1a2e/00f0ff?text=AD1&font=montserrat",
        "views": 245_000,
        "likes": 12_400,
        "comments": 890,
        "shares": 3_200,
        "saves": 1_800,
        "clicks": 4_500,
        "impressions": 310_000,
    },
    {
        "title": "Behind the Scenes — Product Photoshoot",
        "platform": "TikTok",
        "platform_code": "tt",
        "type": "Video",
        "date": "2025-02-01",
        "thumbnail": "https://placehold.co/112x112/1a1a2e/a855f7?text=AD2&font=montserrat",
        "views": 892_000,
        "likes": 54_200,
        "comments": 3_100,
        "shares": 12_800,
        "saves": 5_400,
        "clicks": 8_900,
        "impressions": 1_050_000,
    },
    {
        "title": "Customer Testimonial — Sarah's Story",
        "platform": "YouTube",
        "platform_code": "yt",
        "type": "Short",
        "date": "2025-01-29",
        "thumbnail": "https://placehold.co/112x112/1a1a2e/ff3b5c?text=AD3&font=montserrat",
        "views": 67_000,
        "likes": 3_800,
        "comments": 420,
        "shares": 980,
        "saves": 620,
        "clicks": 2_100,
        "impressions": 89_000,
    },
    {
        "title": "5 Tips to Style Our New Collection",
        "platform": "Instagram",
        "platform_code": "ig",
        "type": "Carousel",
        "date": "2025-01-27",
        "thumbnail": "https://placehold.co/112x112/1a1a2e/ff8c00?text=AD4&font=montserrat",
        "views": 134_000,
        "likes": 8_200,
        "comments": 1_050,
        "shares": 2_600,
        "saves": 4_100,
        "clicks": 3_800,
        "impressions": 178_000,
    },
    {
        "title": "Q&A Live — Ask Our Founder Anything",
        "platform": "LinkedIn",
        "platform_code": "li",
        "type": "Article",
        "date": "2025-01-25",
        "thumbnail": "https://placehold.co/112x112/1a1a2e/5b9bd5?text=AD5&font=montserrat",
        "views": 12_400,
        "likes": 980,
        "comments": 310,
        "shares": 450,
        "saves": 280,
        "clicks": 1_600,
        "impressions": 18_000,
    },
    {
        "title": "Valentine Promo — Gift Guide 💝",
        "platform": "TikTok",
        "platform_code": "tt",
        "type": "Video",
        "date": "2025-02-05",
        "thumbnail": "https://placehold.co/112x112/1a1a2e/ff006e?text=AD6&font=montserrat",
        "views": 1_320_000,
        "likes": 78_500,
        "comments": 5_200,
        "shares": 18_900,
        "saves": 9_200,
        "clicks": 15_300,
        "impressions": 1_580_000,
    },
    {
        "title": "Unboxing Our Premium Box — ASMR",
        "platform": "YouTube",
        "platform_code": "yt",
        "type": "Short",
        "date": "2025-02-04",
        "thumbnail": "https://placehold.co/112x112/1a1a2e/facc15?text=AD7&font=montserrat",
        "views": 198_000,
        "likes": 11_200,
        "comments": 780,
        "shares": 2_100,
        "saves": 1_500,
        "clicks": 5_200,
        "impressions": 240_000,
    },
    {
        "title": "Employee Spotlight — Meet Our Designer",
        "platform": "Instagram",
        "platform_code": "ig",
        "type": "Story",
        "date": "2025-01-31",
        "thumbnail": "https://placehold.co/112x112/1a1a2e/00ff88?text=AD8&font=montserrat",
        "views": 38_500,
        "likes": 2_400,
        "comments": 180,
        "shares": 420,
        "saves": 310,
        "clicks": 890,
        "impressions": 52_000,
    },
]


def compute_scores(post: dict) -> dict:
    """Compute derived metrics for a post."""
    impressions = post["impressions"] or 1
    interactions = post["likes"] + post["comments"] + post["shares"]
    er = (interactions / impressions) * 100
    sov = ((post["saves"] + post["shares"]) / impressions) * 100
    virality = post["views"]  # raw views as virality proxy
    conversion = post["clicks"]  # raw clicks as conversion proxy
    return {
        **post,
        "engagement_rate": round(er, 2),
        "share_of_voice": round(sov, 2),
        "virality_score": virality,
        "conversion_score": conversion,
    }


POSTS_WITH_SCORES = [compute_scores(p) for p in CONTENT_POSTS]


# ──────────────────────────────────────────────
# RENDER: SECTION HEADER
# ──────────────────────────────────────────────
st.markdown("""
<div style="margin-bottom:8px;">
    <div class="section-header">Module 2 · Organic Architecture</div>
    <div class="section-title">📡 The Data Aggregator</div>
    <div class="section-subtitle">Cross-channel audience growth & content performance at a glance.</div>
</div>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────
# VIEW MODE TOGGLE
# ──────────────────────────────────────────────
view_mode = st.radio(
    "VIEW MODE",
    ["📊 Cross-Channel Pulse", "📋 Content Library"],
    horizontal=True,
    label_visibility="collapsed",
)


# ══════════════════════════════════════════════
# VIEW MODE 1: CROSS-CHANNEL PULSE (Ticker Tape)
# ══════════════════════════════════════════════
if view_mode == "📊 Cross-Channel Pulse":

    st.markdown('<hr class="terminal-divider">', unsafe_allow_html=True)

    # Build ticker HTML
    cards_html = ""
    for t in TICKER_DATA:
        growth_class = "positive" if t["growth"] >= 0 else "negative"
        growth_sign = "+" if t["growth"] >= 0 else ""
        arrow = "▲" if t["growth"] >= 0 else "▼"

        cards_html += f"""
        <div class="ticker-card {t['css_class']}">
            <div class="ticker-platform">
                <div class="ticker-platform-icon">{t['icon']}</div>
                <div class="ticker-platform-name">{t['platform']}</div>
            </div>
            <div class="ticker-followers">{format_number(t['followers'])}</div>
            <div class="ticker-growth {growth_class}">
                {arrow} {growth_sign}{format_number(t['growth'])} ({growth_sign}{t['growth_pct']}%)
            </div>
            <div class="ticker-period">Last 7 days</div>
        </div>
        """

    st.markdown(f'<div class="ticker-container">{cards_html}</div>', unsafe_allow_html=True)

    # Mini summary row
    total_growth = sum(t["growth"] for t in TICKER_DATA)
    total_followers = sum(t["followers"] for t in TICKER_DATA)
    net_class = "positive" if total_growth >= 0 else "negative"
    net_sign = "+" if total_growth >= 0 else ""
    net_color = "var(--neon-green)" if total_growth >= 0 else "var(--neon-red)"

    st.markdown(f"""
    <div style="
        margin-top:20px;
        padding:14px 20px;
        background:var(--bg-card);
        border:1px solid var(--border);
        border-radius:10px;
        display:flex;
        justify-content:space-between;
        align-items:center;
        font-family:'JetBrains Mono',monospace;
        font-size:13px;
    ">
        <span style="color:var(--text-secondary);">TOTAL AUDIENCE</span>
        <span style="color:var(--text-primary);font-weight:700;font-size:16px;">
            {format_number(total_followers)}
        </span>
        <span style="color:var(--text-secondary);">NET GROWTH (7D)</span>
        <span style="color:{net_color};font-weight:700;font-size:16px;">
            {net_sign}{format_number(total_growth)}
        </span>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════
# VIEW MODE 2: CONTENT LIBRARY (Table)
# ══════════════════════════════════════════════
else:

    st.markdown('<hr class="terminal-divider">', unsafe_allow_html=True)

    # ── Controls Row ──
    col_sort, col_platform, col_spacer = st.columns([2, 2, 6])

    with col_sort:
        sort_by = st.selectbox(
            "SORT BY",
            ["Virality Score (Views)", "Conversion Score (Clicks)", "Engagement Rate", "Share of Voice"],
        )

    with col_platform:
        platform_filter = st.selectbox(
            "PLATFORM",
            ["All Platforms", "Instagram", "TikTok", "YouTube", "LinkedIn"],
        )

    # ── Filter & Sort ──
    posts = POSTS_WITH_SCORES.copy()

    if platform_filter != "All Platforms":
        posts = [p for p in posts if p["platform"] == platform_filter]

    sort_key_map = {
        "Virality Score (Views)": "virality_score",
        "Conversion Score (Clicks)": "conversion_score",
        "Engagement Rate": "engagement_rate",
        "Share of Voice": "share_of_voice",
    }
    posts.sort(key=lambda x: x[sort_key_map[sort_by]], reverse=True)

    # ── Build Table HTML ──
    def er_class(val: float) -> str:
        if val >= 5.0:
            return "good"
        elif val >= 2.5:
            return "avg"
        return "bad"

    def score_class(val: float, thresholds: tuple) -> str:
        if val >= thresholds[1]:
            return "high"
        elif val >= thresholds[0]:
            return "medium"
        return "low"

    rows_html = ""
    for i, p in enumerate(posts):
        rank = i + 1

        # Badges for top 3
        badges = ""
        if rank == 1:
            badges = ' <span style="font-size:14px;">🏆</span>'
        elif rank == 2:
            badges = ' <span style="font-size:14px;">🥈</span>'
        elif rank == 3:
            badges = ' <span style="font-size:14px;">🥉</span>'

        # Virality score class
        v_cls = score_class(p["virality_score"], (100_000, 500_000))
        c_cls = score_class(p["conversion_score"], (3_000, 8_000))

        rows_html += f"""
        <tr>
            <td style="width:36px; text-align:center; color:var(--text-muted); font-family:'JetBrains Mono',monospace; font-size:12px;">
                {rank}
            </td>
            <td style="min-width:280px;">
                <div class="post-cell">
                    <img class="post-thumbnail" src="{p['thumbnail']}" alt="thumb" />
                    <div class="post-info">
                        <div class="post-title">{p['title']}{badges}</div>
                        <div class="post-meta">
                            <span class="platform-badge {p['platform_code']}">{p['platform']}</span>
                            <span>{p['type']}</span>
                            <span>·</span>
                            <span>{p['date']}</span>
                        </div>
                    </div>
                </div>
            </td>
            <td class="metric-col">{format_number(p['views'])}</td>
            <td class="metric-col">{format_number(p['likes'])}</td>
            <td class="metric-col">{format_number(p['comments'])}</td>
            <td class="metric-col">{format_number(p['shares'])}</td>
            <td class="metric-col">{format_number(p['saves'])}</td>
            <td class="metric-col">{format_number(p['clicks'])}</td>
            <td class="metric-col">
                <span class="er-value {er_class(p['engagement_rate'])}">{p['engagement_rate']:.1f}%</span>
            </td>
            <td class="metric-col">
                <span class="score-badge {v_cls}">{format_number(p['virality_score'])}</span>
            </td>
            <td class="metric-col">
                <span class="score-badge {c_cls}">{format_number(p['conversion_score'])}</span>
            </td>
        </tr>
        """

    table_html = f"""
    <div class="content-table-wrapper">
        <table class="content-table">
            <thead>
                <tr>
                    <th style="width:36px;">#</th>
                    <th>Post / Ad</th>
                    <th class="metric-col">Views</th>
                    <th class="metric-col">Likes</th>
                    <th class="metric-col">Comments</th>
                    <th class="metric-col">Shares</th>
                    <th class="metric-col">Saves</th>
                    <th class="metric-col">Clicks</th>
                    <th class="metric-col">ER %</th>
                    <th class="metric-col">Virality</th>
                    <th class="metric-col">Conversion</th>
                </tr>
            </thead>
            <tbody>
                {rows_html}
            </tbody>
        </table>
    </div>
    """
    st.markdown(table_html, unsafe_allow_html=True)

    # ── Legend ──
    st.markdown("""
    <div style="
        margin-top:16px;
        padding:12px 18px;
        background:var(--bg-card);
        border:1px solid var(--border);
        border-radius:8px;
        font-family:'JetBrains Mono',monospace;
        font-size:11px;
        color:var(--text-muted);
        display:flex;
        gap:24px;
        flex-wrap:wrap;
    ">
        <span><strong style="color:var(--text-secondary);">ER%</strong> = (Likes + Comments + Shares) ÷ Impressions</span>
        <span><strong style="color:var(--text-secondary);">Virality</strong> = Total Views (sortable)</span>
        <span><strong style="color:var(--text-secondary);">Conversion</strong> = Total Link Clicks (sortable)</span>
        <span>Color: <span style="color:var(--neon-green);">■</span> High &nbsp; <span style="color:var(--neon-yellow);">■</span> Medium &nbsp; <span style="color:var(--neon-red);">■</span> Low</span>
    </div>
    """, unsafe_allow_html=True)