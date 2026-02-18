import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import random

from utils.data_loader import DataLoader

# ============================================================
# 1. THEME CONSTANTS
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
    """Load custom CSS for Organic Architecture module"""
    import os
    css_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'module2_organic.css')
    try:
        with open(css_path) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        # Fallback: try loading from relative path
        try:
            with open('assets/module2_organic.css') as f:
                st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
        except FileNotFoundError:
            st.error("CSS file for Organic Architecture module not found.")

def format_number(num):
    """Format large numbers: 1500 -> 1.5K, 1500000 -> 1.5M"""
    if num >= 1_000_000:
        return f"{num / 1_000_000:.1f}M"
    elif num >= 1_000:
        return f"{num / 1_000:.1f}K"
    else:
        return str(num)

# ============================================================
# 2. COMPONENT
# ============================================================

def render_cross_channel_pulse(df):
    """
    View Mode 1: Cross-Channel Pulse — Ticker Tape
    Shows net follower growth (+/-) across all platforms.
    """
    st.markdown('<div class="section-header">📈 Cross-Channel Pulse — Ticker Tape</div>', unsafe_allow_html=True)

    # Create columns for each platform
    cols = st.columns(4)

    for idx, platform in enumerate(['Instagram', 'TikTok', 'YouTube', 'LinkedIn']):
        platform_data = df[df['platform'] == platform]
        current_followers = platform_data['followers'].iloc[-1]
        total_growth = platform_data['follower_growth'].sum()
        growth_pct = (total_growth / (current_followers - total_growth)) * 100 if (current_followers - total_growth) > 0 else 0
        avg_daily_growth = platform_data['follower_growth'].mean()

        # Determine color based on growth
        is_positive = total_growth >= 0
        growth_class = "ticker-growth-positive" if is_positive else "ticker-growth-negative"
        growth_arrow = "▲" if is_positive else "▼"
        color = PLATFORM_COLORS[platform]

        with cols[idx]:
            st.markdown(f"""
            <div class="ticker-card" style="border-top: 3px solid {color};">
                <div class="ticker-platform">{PLATFORM_ICONS[platform]} {platform}</div>
                <div class="metric-value">{current_followers:,}</div>
                <div class="{growth_class}">
                    {growth_arrow} {abs(total_growth):,} ({growth_pct:+.1f}%)
                </div>
                <div style="font-size: 11px; color: #5A6577; margin-top: 4px;">
                    Avg {avg_daily_growth:+.0f}/day - 30d
                </div>
            </div>
            """, unsafe_allow_html=True)

def content_library_section(platform_filter):
    """
    View Mode 2: Content Library
    Thumbnail Grid of posts, sortable by Virality Score or Conversion Score.
    Includes Grid View and Table View toggle, pagination, and platform filter.
    """
    st.markdown('<div class="section-header">📚 CONTENT LIBRARY — POST PERFORMANCE</div>', unsafe_allow_html=True)

    # Generate content library data
    load_data = DataLoader()
    content_df = load_data.load_content_library()  # Assuming social data has post details

    # Apply platform filter
    if platform_filter:
        content_df = content_df[content_df['platform'].isin(platform_filter)]
    
    if content_df.empty:
        st.info("No posts available for the selected filters.")
        return
    
    # --- Controls: View Mode, Sort By ---
    ctrl_col1, ctrl_col2, ctrl_3 = st.columns([2, 2, 1])
    
    with ctrl_col1:
        view_mode = st.selectbox(
            "👁️ View",
            ["Grid View", "Table View"],
            key="content_view_mode"
        )
    
    with ctrl_col2:
        sort_by = st.selectbox(
            "↕️ Sort By",
            ["Virality Score ↓", "Conversion Score ↓", "Views ↓", "Likes ↓", "Most Recent"],
            key="content_sort_by"
        )

    with ctrl_3:
        content_type_options = ["All Types"] + sorted(content_df['content_type'].unique().tolist())
        content_type_filter = st.selectbox(
            "📄 Content Type",
            content_type_options,
            key="content_type_filter"
        )

    # Aplly content type filter
    if content_type_filter != "All Types":
        content_df = content_df[content_df['content_type'] == content_type_filter]
    
    # Apply sorting
    sort_map = {
        "Virality Score ↓": ("virality_score", False),
        "Conversion Score ↓": ("conversion_score", False),
        "Views ↓": ("views", False),
        "Likes ↓": ("likes", False),
        "Most Recent": ("date", False)
    }

    sort_col, sort_asc = sort_map.get(sort_by, ("virality_score", False))
    content_df = content_df.sort_values(by=sort_col, ascending=sort_asc).reset_index(drop=True)

    # Pagination
    ITEMS_PER_PAGE = 9
    total_items = len(content_df)
    total_pages = max(1,(total_items + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE)

    # Initialize session state for pagination
    if "content_page" not in st.session_state: # first load
        st.session_state.content_page = 1 # current page

    # Clamp page number
    if st.session_state.content_page > total_pages:
        st.session_state.content_page = total_pages
    
    current_page = st.session_state.content_page
    start_idx = (current_page - 1) * ITEMS_PER_PAGE
    end_idx = min(start_idx + ITEMS_PER_PAGE, total_items)
    page_df = content_df.iloc[start_idx:end_idx]

    # --- Summary Bar ---
    st.markdown(f"""
    <div style="display: flex; justify-content: space-between; align-items: center;
                padding: 8px 0; margin-bottom: 12px;")>
        <span style="font-size: 12px; color: #8892A0;">
            Showing {start_idx +1}-{end_idx} of {total_items} posts
        </span>
        <span style="font-size: 12px; color: #8892A0;">
            Page {current_page} of {total_pages}
        </span>
    </div>
    """, unsafe_allow_html=True)

    # --- Render Content ---
    if view_mode == "Grid View":
        render_content_grid(page_df)
    else:
        render_content_table(page_df, sort_by)
    
    # --- Pagination Controls ---
    render_pagination(current_page, total_pages)

def render_content_grid(page_df):
    """Render content as visual grid cards with placeholder thumbnails."""

    # Use st.columns to create a grid layout
    cols_per_row = 3
    rows_needed = (len(page_df) + cols_per_row - 1) // cols_per_row

    for row_idx in range (rows_needed):
        cols = st.columns(cols_per_row)
        for col_idx in range(cols_per_row):
            item_idx = row_idx * cols_per_row + col_idx
            if item_idx >= len(page_df):
                break
                
            post = page_df.iloc[item_idx]
            platform = post['platform']
            color = PLATFORM_COLORS.get(platform, "#FFFFFF")
            icon = PLATFORM_ICONS.get(platform, "📄")

            # Generate gradient based on platform color
            r = int(color[1:3], 16)
            g = int(color[3:5], 16)
            b = int(color[5:7], 16)
            gradient = f"linear-gradient(135deg, rgba({r},{g},{b},0.3) 0%, rgba({r},{g},{b},0.08) 100%)"

            # Virality score color
            # Green >=3.0, Yellow >=1.5, Red <1.5
            vs = post['virality_score']
            vs_color = NEON_GREEN if vs >= 3.0 else (NEON_YELLOW if vs >= 1.5 else NEON_RED)

            # Conversion score color
            # Green >=3.0, Yellow >=1.5, Red <1.5
            cs = post['conversion_score']
            cs_color = NEON_GREEN if cs >= 3.0 else (NEON_YELLOW if cs >= 1.5 else NEON_RED)

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
                                <div class="metric-value">{format_number(post['views'])}</div>
                                <div class="card-metric-label">Views</div>
                            </div>
                            <div class="card-metric-item">
                                <div class="metric-value">{format_number(post['likes'])}</div>
                                <div class="card-metric-label">Likes</div>
                            </div>
                            <div class="card-metric-item">
                                <div class="metric-value">{format_number(post['shares'])}</div>
                                <div class="card-metric-label">Shares</div>
                            </div>
                        </div>
                        <div class="card-metrics">
                            <div class="card-metric-item">
                                <div class="metric-value">{format_number(post['comments'])}</div>
                                <div class="card-metric-label">Comments</div>
                            </div>
                            <div class="card-metric-item">
                                <div class="metric-value">{format_number(post['saves'])}</div>
                                <div class="card-metric-label">Saves</div>
                            </div>
                            <div class="card-metric-item">
                                <div class="metric-value">{format_number(post['link_clicks'])}</div>
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
    """Render content as a detailed table view."""
    
    # Column definitions
    columns = [
        {"key": "title", "label": "Content", "sortable": False},
        {"key": "views", "label": "Views", "sortable": True},
        {"key": "likes", "label": "Likes", "sortable": True},
        {"key": "comments", "label": "Comments", "sortable": True},
        {"key": "shares", "label": "Shares", "sortable": True},
        {"key": "saves", "label": "Saves", "sortable": True},
        {"key": "virality_score", "label": "Virality", "sortable": True},
        {"key": "conversion_score", "label": "Conv.", "sortable": True}
    ]

    # Determine sort indicator
    sort_active_map = {
        "Virality Score ↓": "virality_score",
        "Conversion Score ↓": "conversion_score",
        "Views ↓": "views",
        "Likes ↓": "likes",
        "Most Recent": None
    }
    active_sort_col = sort_active_map.get(current_sort, None)

    # Build header
    header_cells = ""
    for col in columns:
        active_class = " active" if col["key"] == active_sort_col else ""
        arrow = " ↓" if col["key"] == active_sort_col else ""
        header_cells += f'<div class="table-header-cell{active_class}">{col["label"]}{arrow}</div>'

    st.markdown(f'<div class="table-header">{header_cells}</div>', unsafe_allow_html=True)

    # Build table rows
    for _, post in page_df.iterrows():
        platform = post['platform']
        color = PLATFORM_COLORS.get(platform, "#FFFFFF")
        icon = PLATFORM_ICONS.get(platform, "📄")
        
        # Virality score color
        # Green >=3.0, Yellow >=1.5, Red <1.5
        vs = post['virality_score']
        vs_color = NEON_GREEN if vs >= 3.0 else (NEON_YELLOW if vs >= 1.5 else TEXT_PRIMARY)

        # Conversion score color
        # Green >=3.0, Yellow >=1.5, Red <1.5
        cs = post['conversion_score']
        cs_color = NEON_GREEN if cs >= 3.0 else (NEON_YELLOW if cs >= 1.5 else TEXT_PRIMARY)

        st.markdown(f"""
        <div class="table-row">
            <div class="table-cell-title">
                <span class="table-platform-dot" style="background: {color};"></span>
                <span style="font-size: 11px;">{icon}</span>
                <span style="overflow: hidden; text-overflow: ellipsis; white-space: nowrap; font-size: 13px; margin-left: 12px;">
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
    """Render pagination controls"""
    
    col_prev, col_info, col_next = st.columns([1, 2, 1])

    with col_prev:
        if current_page > 1:
            if st.button("← Previous", key="page_prev", width='stretch'):
                st.session_state.content_page = current_page - 1
                st.rerun()
        else:
            st.button("← Previous", key="page_prev_disabled", disabled=True, width='stretch')
    
    with col_info:
        # Page number button
        page_cols = st.columns(min(total_pages,7))

        # show at most 7 page buttons
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
                        width='stretch'
                    ):
                        st.session_state.content_page = page_num
                        st.rerun()
    with col_next:
        if current_page < total_pages:
            if st.button("Next →", key="page_next", width='stretch'):
                st.session_state.content_page = current_page + 1
                st.rerun()
        else:
            st.button("Next →", key="page_next_disabled", disabled=True, width='stretch') 

def render_metrics_stacks(df):
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

    platforms = df['platform'].unique().tolist()

    # --- Agregate metrics by platform ---
    total_like = df['likes'].sum()
    total_comments = df['comments'].sum()
    total_shares = df['shares'].sum()
    total_saves = df['saves'].sum()
    total_impressions = df['impressions'].sum()
    total_link_clicks = df['link_clicks'].sum()
    total_profile_visits = df['profile_visits'].sum()
    total_posts = df['posts_published'].sum()
    total_days = df['date'].nunique()

    total_posts_goal = sum([
        df[df['platform'] == p]['posts_goal_weekly'].iloc[0] / 7 * total_days
        for p in platforms
        if len(df[df['platform'] == p]) > 0
    ])

    # enggagement rate
    agg_er = (total_like + total_comments + total_shares) / total_impressions * 100 if total_impressions > 0 else 0

    # share of voice
    agg_sov = (total_saves + total_shares) / total_impressions * 100 if total_impressions > 0 else 0

    # profile conversion rate
    agg_pcr = total_link_clicks / total_profile_visits * 100 if total_profile_visits > 0 else 0

    # consistency score (Post published vs goal)
    agg_cs = total_posts / total_posts_goal * 100 if total_posts_goal > 0 else 0

    # benchmark values (example static values)
    benchmarks = {
        "er": 5.0,
        "sov": 2.0,
        "pcr": 3.0,
        "cs": 80.0
    }

    # --- Render Metric Stacks per platform ---
    platform_metrics = []
    for platform in platforms:
        pdf = df[df['platform'] == platform]
        p_impressions = pdf['impressions'].sum()
        p_likes = pdf['likes'].sum()
        p_comments = pdf['comments'].sum()
        p_shares = pdf['shares'].sum()
        p_saves = pdf['saves'].sum()
        p_link_clicks = pdf['link_clicks'].sum()
        p_profile_visits = pdf['profile_visits'].sum()
        p_posts = pdf['posts_published'].sum()
        p_days = pdf['date'].nunique()
        p_goal = pdf['posts_goal_weekly'].iloc[0] / 7 * p_days if len(pdf) > 0 else 0

        # engagement rate
        er = (p_likes + p_comments + p_shares) / p_impressions * 100 if p_impressions > 0 else 0
        # share of voice
        sov = (p_saves + p_shares) / p_impressions * 100 if p_impressions > 0 else 0
        # profile conversion rate
        pcr = p_link_clicks / p_profile_visits * 100 if p_profile_visits > 0 else 0
        # consistency score
        cs = p_posts / p_goal * 100 if p_goal > 0 else 0

        # Dialy ER trend for sparkline
        dialy_e = pdf.groupby('date').apply(
            lambda x: (x['likes'].sum() + x['comments'].sum() + x['shares'].sum()) / max(x['impressions'].sum(), 1) * 100,
            include_groups=False
        ).tolist()

        platform_metrics.append({
            "platform": platform,
            "er": er,
            "sov": sov,
            "pcr": pcr,
            "cs": cs,
            "daily_er": dialy_e,
            "total_impressions": p_impressions,
            "total_engagement": p_likes + p_comments + p_shares,
            "total_traffic": p_link_clicks
        })

    # --- Render Comparison Bar Chart ---
    # _render_metric_comparison_chart(platform_metrics, benchmarks)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- Render Per-Platform Detail Cards ---
    _render_platform_metric_cards(platform_metrics, benchmarks)

def _render_platform_metric_cards(platform_metrics, benchmarks):
    """Render detailed metric cards per platform."""

    cols = st.columns(len(platform_metrics))

    for idx, pm in enumerate(platform_metrics):
        platform = pm["platform"]
        color = PLATFORM_COLORS[platform]
        icon = PLATFORM_ICONS[platform]

        # Determine status for each metric
        def get_status(value, benchmark):
            if value >= benchmark:
                return NEON_GREEN, "▲ On Track"
            elif value >= benchmark * 0.7:
                return NEON_YELLOW, "● Near Target"
            else:
                return NEON_RED, "▼ Below Target"

        er_color, er_status = get_status(pm["er"], benchmarks["er"])
        sov_color, sov_status = get_status(pm["sov"], benchmarks["sov"])
        pcr_color, pcr_status = get_status(pm["pcr"], benchmarks["pcr"])
        cs_color, cs_status = get_status(pm["cs"], benchmarks["cs"])
    
        with cols[idx]:
            st.markdown(f"""
            <div class="metric-stack-card">
                <div class="metric-stack-card-header" style="border-bottom: 2px solid {color};">
                    <span class="metric-stack-card-icon" style="background: {color};">{icon}</span>
                    <span class="metric-stack-card-title">{platform}</span>
                </div>
                <div class="metric-stack-card-body">
                    <div class="metric-stack-item">
                        <div class="metric-stack-label">Engagement Rate (ER)</div>
                        <div class="metric-value">{pm["er"]:.2f}%</div>
                        <div class="metric-stack-status" style="color: {er_color};">{er_status}</div>
                    </div>
                    <div class="metric-stack-item">
                        <div class="metric-stack-label">Share of Voice (SoV)</div>
                        <div class="metric-value">{pm["sov"]:.2f}%</div>
                        <div class="metric-stack-status" style="color: {sov_color};">{sov_status}</div>
                    </div>
                    <div class="metric-stack-item">
                        <div class="metric-stack-label">Profile Conversion Rate (PCR)</div>
                        <div class="metric-value">{pm["pcr"]:.2f}%</div>
                        <div class="metric-stack-status" style="color: {pcr_color};">{pcr_status}</div>
                    </div>
                    <div class="metric-stack-item">
                        <div class="metric-stack-label">Consistency Score</div>
                        <div class="metric-value">{pm["cs"]:.2f}%</div>
                        <div class="metric-stack-status" style="color: {cs_color};">{cs_status}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

def render_engagement_funnel(df):
    """
    Visualization A: The Engagement Funnel
    Horizontal funnel: Reach → Interaction → Click
    Shows conversion at each stage across all platforms or per platform.
    """

    st.markdown('<div class="section-header">🔄 ENGAGEMENT FUNNEL — REACH → INTERACTION → CLICK</div>', unsafe_allow_html=True)

    # calculate funnel stages
    platforms = df['platform'].unique().tolist()

    # Aggregate metrics by platform
    total_reach = df['impressions'].sum()
    total_interaction = (df['likes'].sum() + df['comments'].sum() + df['shares'].sum())
    total_clicks = df['link_clicks'].sum()

    reach_to_interaction = (total_interaction / total_reach * 100) if total_reach > 0 else 0
    interaction_to_click = (total_clicks / total_interaction * 100) if total_interaction > 0 else 0
    reach_to_click = (total_clicks / total_reach * 100) if total_reach > 0 else 0

    # --- Aggregated Funnel Chart ---
    col_funnel, col_rates = st.columns([3, 1])

    with col_funnel:
        fig = go.Figure()

        # Funnel stages
        stages = ["👁️ Reach (Impressions)", "💬 Interaction (Engagement)", "🔗 Click (Link Clicks)"]
        values = [total_reach, total_interaction, total_clicks]
        colors = [NEON_BLUE, NEON_PURPLE, NEON_GREEN]

        fig.add_trace(go.Funnel(
            y=stages,
            x=values,
            textposition="auto",
            textinfo="value+percent initial",
            texttemplate="%{value:,}<br>(%{percentInitial:.1%})",
            textfont=dict(color=TEXT_PRIMARY, size=14),
            marker=dict(
                color=colors,
                line=dict(width=0),
            ),
            connector=dict(
                line=dict(color=DARK_BG, width=2),
                fillcolor="rgba(45, 51, 72, 1)"
            ),
            ))
        
        # 
        fig.update_layout( 
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color=TEXT_SECONDARY, size=12),
            height=280,
            margin=dict(l=10, r=10, t=10, b=10),
            showlegend=False,
        )
        
        st.plotly_chart(fig, width='stretch')
    
    with col_rates:
        # Conversion Rates cards
        st.markdown(f"""
        <div style="padding: 12px 0;">
            <div style="background: linear-gradient(135deg, #1B1F2B 0%, #222838 100%);
                        border: 1px solid #2D3348; border-left: 3px solid {NEON_BLUE};
                        border-radius: 8px; padding: 14px 16px; margin-bottom: 10px;">
                <div style="font-size: 9px; color: #8892A0; text-transform: uppercase; 
                            letter-spacing: 1px;">Reach → Interaction</div>
                <div style="font-size: 20px; font-weight: 700; color: {NEON_BLUE};">
                    {reach_to_interaction:.2f}%</div>
            </div>
            <div style="background: linear-gradient(135deg, #1B1F2B 0%, #222838 100%);
                        border: 1px solid #2D3348; border-left: 3px solid {NEON_PURPLE};
                        border-radius: 8px; padding: 14px 16px; margin-bottom: 10px;">
                <div style="font-size: 9px; color: #8892A0; text-transform: uppercase; 
                            letter-spacing: 1px;">Interaction → Click</div>
                <div style="font-size: 20px; font-weight: 700; color: {NEON_PURPLE};">
                    {interaction_to_click:.2f}%</div>
            </div>
            <div style="background: linear-gradient(135deg, #1B1F2B 0%, #222838 100%);
                        border: 1px solid #2D3348; border-left: 3px solid {NEON_ORANGE};
                        border-radius: 8px; padding: 14px 16px;">
                <div style="font-size: 9px; color: #8892A0; text-transform: uppercase; 
                            letter-spacing: 1px;">Total Reach → Click</div>
                <div style="font-size: 20px; font-weight: 700; color: {NEON_ORANGE};">
                    {reach_to_click:.3f}%</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    
    # --- Conversion Rate Table ---
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
                        <div style="font-size: 20px; font-weight: 700; color: {NEON_BLUE};">
                            {pf['reach_to_int_pct']:.1f}%</div>
                        <div style="font-size: 15px; color: #5A6577; text-transform: uppercase;">
                            R→I Rate</div>
                    </div>
                    <div style="width: 1px; background: #2D3348;"></div>
                    <div>
                        <div style="font-size: 20px; font-weight: 700; color: {NEON_ORANGE};">
                            {pf['int_to_click_pct']:.1f}%</div>
                        <div style="font-size: 15px; color: #5A6577; text-transform: uppercase;">
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
    loader = DataLoader()
    content_df = loader.load_content_library()

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
                        <div style="font-size: 20px; font-weight: 600; color: #FFFFFF;">{format_number(post['views'])}</div>
                        <div style="font-size: 12px; color: #5A6577; text-transform: initial;">Views</div>
                    </td>
                    <td style="text-align: center; padding: 8px 4px; background: rgba(0,0,0,0.2); border-radius: 6px; width: 33%;">
                        <div style="font-size: 20px; font-weight: 600; color: #FFFFFF;">{format_number(post['likes'])}</div>
                        <div style="font-size: 12px; color: #5A6577; text-transform: initial;">Likes</div>
                    </td>
                    <td style="text-align: center; padding: 8px 4px; background: rgba(0,0,0,0.2); border-radius: 6px; width: 33%;">
                        <div style="font-size: 20px; font-weight: 600; color: #FFFFFF;">{format_number(post['saves'])}</div>
                        <div style="font-size: 12px; color: #5A6577; text-transform: initial;">Saves</div>
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

def render_ai_brain(df, platform_filter):
    """
    Section 4: The AI Brain Logic (The Community Manager)
    Placeholder — ready for OpenAI API integration.
    
    Logic A (Sentiment Guard): Negative sentiment detection
    Logic B (Trend Spotter): Trending audio/content detection
    Logic C (SEO Assist): Reach vs retention optimization
    
    Currently generates static demo insights based on data patterns.
    """
    st.markdown('<div class="section-header">🧠 AI BRAIN — THE ADVISOR</div>', unsafe_allow_html=True)

    # --- Generate placeholder insights ---
    insights = _generate_placeholder_insights(df, platform_filter)

    # --- Status Bar ---
    st.markdown(f"""<div style="display: flex; align-items: center; justify-content: space-between; padding: 10px 16px; background: linear-gradient(135deg, #1B1F2B 0%, #222838 100%); border: 1px solid #2D3348; border-radius: 8px; margin-bottom: 16px;">
        <div style="display: flex; align-items: center; gap: 8px;">
        <div style="width: 8px; height: 8px; border-radius: 50%; background: {NEON_GREEN}; animation: pulse 2s infinite;"></div>
        <span style="font-size: 11px; color: #8892A0; text-transform: uppercase; letter-spacing: 1px;">AI Engine Status: Active</span>
        </div>
        <div style="font-size: 10px; color: #5A6577;">Last Analysis: Just now · Powered by OpenAI</div>
        </div>""", unsafe_allow_html=True)
    
    # --- Insights Cards ---
    for insight in insights:
        _render_insight_card(insight)
    
    # --- Generate Insight Button ---
    st.markdown("<br>", unsafe_allow_html=True)
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    with col_btn2:
        generate_clicked = st.button(
            "🧠 Generate New Insights",
            key="generate_ai_insights",
            use_container_width=True,
            type="primary"
        )
        if generate_clicked:
            st.info("🔌 OpenAI API integration pending. Insights above are placeholder data based on current metrics.")

def _generate_placeholder_insights(df, platform_filter):
    """
    Generate placeholder insights matching the brief's tone:
    Short, punchy, actionable — like a real AI community manager.
    These will be replaced by real OpenAI API calls later.
    """
    insights = []

    # --- Logic A: Sentiment Guard ---
    # Detect platform with sudden engagement drop (simulates negative sentiment)
    platform_er = {}
    for platform in df["platform"].unique():
        pdf = df[df["platform"] == platform]
        er = (pdf["likes"].sum() + pdf["comments"].sum() + pdf["shares"].sum()) / max(pdf["impressions"].sum(), 1) * 100
        platform_er[platform] = er

    if platform_er:
        worst_platform = min(platform_er, key=platform_er.get)
        worst_er = platform_er[worst_platform]

        # Simulate detected negative topic
        negative_topics = {
            "Instagram": "Pricing",
            "TikTok": "Shipping",
            "YouTube": "Product Quality",
            "LinkedIn": "Customer Support",
        }
        detected_topic = negative_topics.get(worst_platform, "Service")

        insights.append({
            "logic_id": "A",
            "logic_name": "Sentiment Guard",
            "icon": "🛡️",
            "severity": "warning" if worst_er < 5.0 else "info",
            "title": f"Negative sentiment spike detected on {worst_platform} regarding '{detected_topic}'",
            "body": f"Comment analysis shows a {worst_er:.1f}% engagement rate with increasing negative mentions "
                    f"around '{detected_topic}' in the last 7 days. This is dragging down overall brand sentiment.",
            "recommendation": f"Address '{detected_topic}' concerns in Stories. Post a transparent Q&A or behind-the-scenes "
                            f"explaining your {detected_topic.lower()} process.",
            "accent_color": NEON_YELLOW if worst_er < 5.0 else NEON_BLUE,
        })

    # --- Logic B: Trend Spotter ---
    # Simulate trending audio/content detection
    platform_growth = {}
    for platform in df["platform"].unique():
        pdf = df[df["platform"] == platform]
        growth = pdf["follower_growth"].sum()
        platform_growth[platform] = growth

    if platform_growth:
        trending_platform = max(platform_growth, key=platform_growth.get)
        trending_growth = platform_growth[trending_platform]
        growth_pct = trending_growth / max(abs(min(platform_growth.values())), 1) * 100

        # Simulate trending content
        trending_content = {
            "Instagram": ("Audio Track 'Espresso — Sabrina Carpenter'", "Reel"),
            "TikTok": ("Sound 'APT. — ROSÉ & Bruno Mars'", "Short Video"),
            "YouTube": ("Format 'Day in My Life ASMR'", "Short"),
            "LinkedIn": ("Hook style 'I quit my job to...'", "Carousel Post"),
        }
        trend_name, trend_format = trending_content.get(trending_platform, ("Trending format", "Post"))

        insights.append({
            "logic_id": "B",
            "logic_name": "Trend Spotter",
            "icon": "📈",
            "severity": "success",
            "title": f"{trend_name} is trending +{min(growth_pct, 85):.0f}% on {trending_platform}",
            "body": f"This trend is gaining momentum fast. Early adopters are seeing 2-3x normal reach. "
                    f"Your audience on {trending_platform} (+{trending_growth:,.0f} new followers) "
                    f"is primed for this type of content.",
            "recommendation": f"Use for next {trend_format}. Post within 48 hours to catch the wave. "
                            f"Add your unique brand twist — don't just copy the trend.",
            "accent_color": NEON_GREEN,
        })

    # --- Logic C: SEO Assist ---
    # High retention but low reach pattern
    platform_gap = {}
    for platform in df["platform"].unique():
        pdf = df[df["platform"] == platform]
        impressions = pdf["impressions"].sum()
        saves = pdf["saves"].sum()
        save_rate = saves / max(impressions, 1) * 100
        platform_gap[platform] = {"impressions": impressions, "saves": saves, "save_rate": save_rate}

    if platform_gap:
        # Find platform with high saves (retention) but low impressions (reach)
        high_retention = max(platform_gap, key=lambda x: platform_gap[x]["save_rate"])
        low_reach = min(platform_gap, key=lambda x: platform_gap[x]["impressions"])
        
        # Use the platform that has the biggest gap
        target_platform = low_reach if platform_gap[low_reach]["save_rate"] > 1.0 else high_retention
        gap_data = platform_gap[target_platform]

        insights.append({
            "logic_id": "C",
            "logic_name": "SEO Assist",
            "icon": "🔍",
            "severity": "warning",
            "title": f"High retention but low reach on last {target_platform} posts",
            "body": f"Save rate on {target_platform} is {gap_data['save_rate']:.1f}% (people love the content), "
                    f"but impressions are only {format_number(gap_data['impressions'])}. "
                    f"The algorithm isn't pushing your content to new audiences.",
            "recommendation": f"Switch generic tags for niche SEO keywords. Replace #marketing #business with "
                            f"specific long-tail hashtags. Add keyword-rich captions and alt-text for discoverability.",
            "accent_color": NEON_ORANGE,
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
    st.markdown(f"""
        <div style="background: {sev['bg']}; border: 1px solid {sev['border']}; border-radius: 12px 12px 0 0; padding: 14px 20px;">
            <div style="display: flex; align-items: center; justify-content: space-between;">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <span style="font-size: 22px;">{insight['icon']}</span>
                    <div>
                        <div style="font-size: 20px; font-weight: 600; color: #FFFFFF;">{insight['title']}</div>
                        <div style="font-size: 15px; color: #5A6577; margin-top: 2px;">Logic {insight['logic_id']}: {insight['logic_name']}</div>
                    </div>
                </div>
                <div style="padding: 3px 10px; border-radius: 20px; background: {sev['label_bg']}; font-size: 9px; font-weight: 700; color: {sev['label_color']}; text-transform: uppercase; letter-spacing: 1px;">{sev['label']}</div>
            </div>
        </div>""", unsafe_allow_html=True)

    # Card Body — Analysis
    st.markdown(f"""
        <div style="background: {sev['bg']}; border-left: 1px solid {sev['border']}; border-right: 1px solid {sev['border']}; padding: 0 20px 12px 20px;">
            <div style="font-size: 15px; color: #C0C7D0; line-height: 1.7; padding: 10px 14px; background: rgba(0,0,0,0.15); border-radius: 8px;">
                <span style="font-size: 9px; color: #5A6577; text-transform: uppercase; letter-spacing: 1px; display: block; margin-bottom: 6px;">📊 Analysis</span>
                {insight['body']}
            </div>
        </div>""", unsafe_allow_html=True)

    # Card Footer — Recommendation
    st.markdown(f"""
        <div style="background: {sev['bg']}; border: 1px solid {sev['border']}; border-top: none; border-radius: 0 0 12px 12px; padding: 0 20px 14px 20px;">
            <div style="font-size: 15px; color: #C0C7D0; line-height: 1.7; padding: 10px 14px; background: rgba(0,0,0,0.1); border-radius: 8px; border-left: 3px solid {accent};">
                <span style="font-size: 9px; color: {accent}; text-transform: uppercase; letter-spacing: 1px; display: block; margin-bottom: 6px;">💡 Recommendation</span>
                {insight['recommendation']}
            </div>
        </div>""", unsafe_allow_html=True)

    # Spacer
    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

# ============================================================
# 3. COMPONENT RENDERERS (Placeholder for visualization)
# ============================================================

def show_organic_architecture():
    """
    Main entry point for Organic Architecture module
    """

    load_module2_css()

    # --- Sticky Header: Title + Filters ---
    with st.container():
        st.markdown('<div id="sticky-header"></div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="header-title-row">
            <span class="module-title-compact">📱 Organic Architecture</span>
            <span class="module-subtitle-compact">Brand Resonance, Community Loyalty & Traffic Contribution</span>
        </div>
        """, unsafe_allow_html=True)
        col_filter1, col_filter2 = st.columns([2, 2])
        with col_filter1:
            date_range = st.selectbox(
                "📅 Time Range",
                ["Last 7 Days", "Last 14 Days", "Last 30 Days"],
                index=2,
                key="organic_date_range"
            )
        with col_filter2:
            platform_filter = st.multiselect(
                "🌐 Platform",
                ['Instagram', 'TikTok', 'YouTube', 'LinkedIn'],
                default=['Instagram', 'TikTok', 'YouTube', 'LinkedIn'],
                key="organic_platform_filter"
            )

    # --- Load Data ---
    days_map = {"Last 7 Days": 7, "Last 14 Days": 14, "Last 30 Days": 30}
    days = days_map.get(date_range, 60)

    data_loader = DataLoader()
    organic_df = data_loader.load_organic_data()
    content_df = data_loader.load_content_library()
    organic_df['date'] = pd.to_datetime(organic_df['date'])

    # Filter data based on selections
    cutoff_date = datetime.now() - timedelta(days=days)
    organic_df = organic_df[organic_df['date'] >= cutoff_date]
    content_df = content_df[content_df['date'] >= cutoff_date]

    # --- Divider ---
    st.markdown('<div style="height: 1px; background: linear-gradient(to right, transparent, #2D3348, transparent); margin: 24px 0;"></div>', unsafe_allow_html=True)

    # --- Section 1.A : Cross-Channel Pulse (all platforms, unfiltered) ---
    render_cross_channel_pulse(organic_df)

    st.markdown('<div style="height: 1px; background: linear-gradient(to right, transparent, #2D3348, transparent); margin: 24px 0;"></div>', unsafe_allow_html=True)

    # filter by platform for subsequent sections
    if platform_filter:
        organic_df = organic_df[organic_df['platform'].isin(platform_filter)]
        content_df = content_df[content_df['platform'].isin(platform_filter)]
    
    # --- Section 1.B: Content Library (detailed posts data) ---
    content_library_section(platform_filter)

    st.markdown('<div style="height: 1px; background: linear-gradient(to right, transparent, #2D3348, transparent); margin: 24px 0;"></div>', unsafe_allow_html=True)

    # --- Section 2: Metric Stacks (key metrics breakdown) ---
    render_metrics_stacks(organic_df)

    st.markdown('<div style="height: 1px; background: linear-gradient(to right, transparent, #2D3348, transparent); margin: 24px 0;"></div>', unsafe_allow_html=True)

    # --- Section 3.A : Engagement Funnel & Leaderboard ---
    render_engagement_funnel(organic_df)

    st.markdown('<div style="height: 1px; background: linear-gradient(to right, transparent, #2D3348, transparent); margin: 24px 0;"></div>', unsafe_allow_html=True)

    # --- Section 3.B : Content Leaderboard (top posts with badges) ---
    render_content_leaderboard(platform_filter)

    st.markdown('<div style="height: 1px; background: linear-gradient(to right, transparent, #2D3348, transparent); margin: 24px 0;"></div>', unsafe_allow_html=True)
    # --- Section 4: AI Brain ---
    render_ai_brain(organic_df, platform_filter)
    
    st.markdown('<div style="height: 1px; background: linear-gradient(to right, transparent, #2D3348, transparent); margin: 24px 0;"></div>', unsafe_allow_html=True)

# ============================================================
# 4. STANDALONE TEST MODE
# ============================================================

if __name__ == "__main__":
    st.set_page_config(
        page_title="Marktivo Growth OS — Organic Architecture",
        page_icon="📱",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    show_organic_architecture()