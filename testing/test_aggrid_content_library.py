import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode

# ============================================
# PAGE CONFIG
# ============================================
st.set_page_config(
    page_title="Content Library - AG Grid Test",
    page_icon="📚",
    layout="wide"
)

# ============================================
# SAMPLE DATA GENERATOR
# ============================================
@st.cache_data
def generate_sample_posts():
    """Generate sample post data for testing"""
    
    platforms = ['Instagram', 'TikTok', 'YouTube', 'LinkedIn']
    post_types = ['Reel', 'Story', 'Feed', 'Video', 'Short', 'Carousel']
    
    posts_data = []
    
    for i in range(50):  # Generate 50 posts
        platform = random.choice(platforms)
        post_type = random.choice(post_types)
        
        # Metrics
        views = random.randint(1000, 500000)
        likes = int(views * random.uniform(0.02, 0.15))
        comments = int(likes * random.uniform(0.05, 0.2))
        shares = int(likes * random.uniform(0.1, 0.3))
        saves = int(likes * random.uniform(0.15, 0.4))
        impressions = int(views * random.uniform(1.2, 2.5))
        profile_visits = int(views * random.uniform(0.01, 0.05))
        link_clicks = int(profile_visits * random.uniform(0.1, 0.4))
        
        # Calculate derived metrics
        engagement_rate = round(((likes + comments + shares) / impressions) * 100, 2)
        share_of_voice = round(((saves + shares) / impressions) * 100, 2)
        profile_conversion = round((link_clicks / profile_visits) * 100, 2) if profile_visits > 0 else 0
        
        # Scores
        virality_score = int(views * 0.6 + shares * 100 + saves * 80)
        conversion_score = int(link_clicks * 500 + profile_visits * 50)
        
        posts_data.append({
            'post_id': f'POST_{i+1:03d}',
            'platform': platform,
            'post_type': post_type,
            'published_date': (datetime.now() - timedelta(days=random.randint(1, 30))).strftime('%Y-%m-%d'),
            'thumbnail_url': f'https://picsum.photos/seed/{i}/300/300',
            'caption': f'Sample post content about {random.choice(["product", "lifestyle", "tutorial", "behind-the-scenes"])}...',
            'views': views,
            'impressions': impressions,
            'likes': likes,
            'comments': comments,
            'shares': shares,
            'saves': saves,
            'profile_visits': profile_visits,
            'link_clicks': link_clicks,
            'engagement_rate': engagement_rate,
            'share_of_voice': share_of_voice,
            'profile_conversion': profile_conversion,
            'virality_score': virality_score,
            'conversion_score': conversion_score
        })
    
    return pd.DataFrame(posts_data)

# ============================================
# CUSTOM CSS
# ============================================
st.markdown("""
<style>
    /* Dark mode styling */
    .stApp {
        background-color: #0e1117;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #667eea !important;
    }
    
    /* Info boxes */
    .info-box {
        background-color: #1a1d29;
        border-left: 4px solid #667eea;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
    }
    
    /* Badge styling */
    .badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 12px;
        margin: 2px 4px;
        font-size: 11px;
        font-weight: 600;
    }
    .badge-instagram { background-color: #E1306C; color: white; }
    .badge-tiktok { background-color: #000000; color: white; }
    .badge-youtube { background-color: #FF0000; color: white; }
    .badge-linkedin { background-color: #0A66C2; color: white; }
</style>
""", unsafe_allow_html=True)

# ============================================
# MAIN APP
# ============================================

st.title("📚 Content Library - AG Grid Test")
st.markdown("---")

# Generate data
df_posts = generate_sample_posts()

# ============================================
# FILTERS & CONTROLS
# ============================================

st.subheader("🎛️ Filters & Controls")

col1, col2, col3 = st.columns([2, 2.5, 1.5])

with col1:
    sort_by = st.selectbox(
        "Default Sort",
        ["Virality Score", "Conversion Score", "Engagement Rate", "Views", "Link Clicks", "Recent First"]
    )

with col2:
    all_platforms = list(df_posts['platform'].unique())
    
    # Sub-columns for filter + toggle buttons
    filter_col, toggle_col1, toggle_col2 = st.columns([5, 1, 1])
    
    with filter_col:
        if 'selected_platforms' not in st.session_state:
            st.session_state.selected_platforms = all_platforms
        
        platform_filter = st.multiselect(
            "Filter by Platform",
            options=all_platforms,
            default=st.session_state.selected_platforms
        )
    
    with toggle_col1:
        st.markdown("<div style='margin-top: 28px;'></div>", unsafe_allow_html=True)
        if st.button("✅ All", key="select_all", use_container_width=True):
            st.session_state.selected_platforms = all_platforms
            st.rerun()
    
    with toggle_col2:
        st.markdown("<div style='margin-top: 28px;'></div>", unsafe_allow_html=True)
        if st.button("❌ None", key="deselect_all", use_container_width=True):
            st.session_state.selected_platforms = []
            st.rerun()

with col3:
    grid_height = st.slider("Table Height", 400, 800, 600, step=50)

# Handle empty selection
if not platform_filter:
    st.warning("⚠️ No platform selected. Showing all platforms.")
    platform_filter = all_platforms

# Apply filters
df_filtered = df_posts[df_posts['platform'].isin(platform_filter)].copy()

# Display active filters as badges
if platform_filter:
    st.markdown("**Active Filters:**")
    badge_html = ""
    platform_colors = {
        'Instagram': 'badge-instagram',
        'TikTok': 'badge-tiktok',
        'YouTube': 'badge-youtube',
        'LinkedIn': 'badge-linkedin'
    }
    
    for platform in platform_filter:
        badge_class = platform_colors.get(platform, '')
        badge_html += f"<span class='badge {badge_class}'>{platform}</span>"
    
    st.markdown(badge_html, unsafe_allow_html=True)

# Info banner
st.info(f"📊 Showing **{len(df_filtered)}** posts from **{len(platform_filter)}** platform(s)")

st.markdown("---")

# ============================================
# AG GRID CONFIGURATION
# ============================================

st.subheader("📊 Interactive Data Table (AG Grid)")

# Apply default sorting to dataframe
sort_mapping = {
    "Virality Score": ('virality_score', False),
    "Conversion Score": ('conversion_score', False),
    "Engagement Rate": ('engagement_rate', False),
    "Views": ('views', False),
    "Link Clicks": ('link_clicks', False),
    "Recent First": ('published_date', False)
}

sort_column, sort_asc = sort_mapping[sort_by]
df_filtered = df_filtered.sort_values(sort_column, ascending=sort_asc)

# Prepare display columns
display_df = df_filtered[[
    'post_id',
    'platform',
    'post_type',
    'published_date',
    'views',
    'impressions',
    'likes',
    'comments',
    'shares',
    'saves',
    'profile_visits',
    'link_clicks',
    'engagement_rate',
    'share_of_voice',
    'profile_conversion',
    'virality_score',
    'conversion_score',
    'thumbnail_url',
    'caption'
]].copy()

# Configure AG Grid
gb = GridOptionsBuilder.from_dataframe(display_df)

# General grid settings
gb.configure_default_column(
    resizable=True,
    filterable=True,
    sortable=True,
    editable=False,
    groupable=True
)

# Enable features
gb.configure_pagination(paginationAutoPageSize=False, paginationPageSize=20)
gb.configure_side_bar()  # Adds filter panel
gb.configure_selection('single', use_checkbox=False)  # Single row selection

# Column-specific configurations
gb.configure_column(
    "post_id",
    header_name="Post ID",
    width=110,
    pinned='left',  # Pin to left side
    cellStyle={'fontWeight': '600', 'color': '#667eea'}
)

gb.configure_column(
    "platform",
    header_name="Platform",
    width=120,
    cellStyle=JsCode("""
        function(params) {
            const colors = {
                'Instagram': '#E1306C',
                'TikTok': '#000000',
                'YouTube': '#FF0000',
                'LinkedIn': '#0A66C2'
            };
            return {
                'color': 'white',
                'backgroundColor': colors[params.value] || '#667eea',
                'fontWeight': '600',
                'borderRadius': '4px',
                'padding': '4px 8px',
                'textAlign': 'center'
            };
        }
    """)
)

gb.configure_column("post_type", header_name="Type", width=100)
gb.configure_column("published_date", header_name="Date", width=120)

# Numeric columns with formatting
numeric_columns = {
    'views': {'header': 'Views', 'width': 110},
    'impressions': {'header': 'Impressions', 'width': 120},
    'likes': {'header': 'Likes', 'width': 100},
    'comments': {'header': 'Comments', 'width': 110},
    'shares': {'header': 'Shares', 'width': 100},
    'saves': {'header': 'Saves', 'width': 100},
    'profile_visits': {'header': 'Profile Visits', 'width': 130},
    'link_clicks': {'header': 'Link Clicks', 'width': 120},
    'virality_score': {'header': 'Virality Score', 'width': 130},
    'conversion_score': {'header': 'Conversion Score', 'width': 150}
}

for col, config in numeric_columns.items():
    gb.configure_column(
        col,
        header_name=config['header'],
        width=config['width'],
        type=["numericColumn", "numberColumnFilter"],
        valueFormatter=JsCode("""
            function(params) {
                return params.value.toLocaleString();
            }
        """)
    )

# Percentage columns
percentage_columns = {
    'engagement_rate': {'header': 'Engagement Rate (%)', 'width': 160},
    'share_of_voice': {'header': 'Share of Voice (%)', 'width': 160},
    'profile_conversion': {'header': 'Profile Conv (%)', 'width': 150}
}

for col, config in percentage_columns.items():
    gb.configure_column(
        col,
        header_name=config['header'],
        width=config['width'],
        type=["numericColumn", "numberColumnFilter"],
        valueFormatter=JsCode("""
            function(params) {
                return params.value.toFixed(2) + '%';
            }
        """),
        cellStyle=JsCode("""
            function(params) {
                if (params.value >= 5) {
                    return {'color': '#4ade80', 'fontWeight': '600'};
                } else if (params.value >= 3) {
                    return {'color': '#fbbf24'};
                } else {
                    return {'color': '#f87171'};
                }
            }
        """)
    )

# Hide thumbnail and caption columns (we'll show them in detail view)
gb.configure_column("thumbnail_url", hide=True)
gb.configure_column("caption", hide=True)

# Build grid options
grid_options = gb.build()

# Custom grid theme
custom_css = {
    ".ag-root-wrapper": {
        "border-radius": "8px",
        "overflow": "hidden"
    },
    ".ag-header": {
        "background-color": "#1e1e1e !important",
        "color": "#667eea !important",
        "font-weight": "600"
    },
    ".ag-row": {
        "border-bottom": "1px solid #2d3142"
    },
    ".ag-row-hover": {
        "background-color": "#1a1d29 !important"
    }
}

# Display AG Grid
grid_response = AgGrid(
    display_df,
    gridOptions=grid_options,
    update_on=['selectionChanged'],  # ✅ Updated syntax
    theme='streamlit',
    height=grid_height,
    allow_unsafe_jscode=True,
    custom_css=custom_css,
    enable_enterprise_modules=False
)

st.markdown("---")

# ============================================
# SELECTED ROW DETAILS
# ============================================

if grid_response['selected_rows'] is not None and len(grid_response['selected_rows']) > 0:
    selected_post = pd.DataFrame(grid_response['selected_rows']).iloc[0]
    
    st.subheader("🔍 Selected Post Details")
    
    detail_col1, detail_col2, detail_col3 = st.columns([2, 3, 3])
    
    with detail_col1:
        st.markdown("### 📸 Thumbnail")
        st.image(selected_post['thumbnail_url'], use_container_width=True)
        
        # Platform badge
        platform_emoji = {
            'Instagram': '📷',
            'TikTok': '🎵',
            'YouTube': '▶️',
            'LinkedIn': '💼'
        }
        st.markdown(f"**{platform_emoji.get(selected_post['platform'], '📱')} {selected_post['platform']}**")
        st.caption(f"{selected_post['post_type']} • {selected_post['published_date']}")
    
    with detail_col2:
        st.markdown("### 📊 Performance Metrics")
        
        metric_col1, metric_col2 = st.columns(2)
        
        with metric_col1:
            st.metric("👁️ Views", f"{int(selected_post['views']):,}")
            st.metric("❤️ Likes", f"{int(selected_post['likes']):,}")
            st.metric("💬 Comments", f"{int(selected_post['comments']):,}")
            st.metric("🔄 Shares", f"{int(selected_post['shares']):,}")
        
        with metric_col2:
            st.metric("🔖 Saves", f"{int(selected_post['saves']):,}")
            st.metric("👤 Profile Visits", f"{int(selected_post['profile_visits']):,}")
            st.metric("🔗 Link Clicks", f"{int(selected_post['link_clicks']):,}")
            st.metric("📈 Impressions", f"{int(selected_post['impressions']):,}")
    
    with detail_col3:
        st.markdown("### 🎯 Performance Indicators")
        
        # Engagement Rate
        er_benchmark = 5.0
        er_delta = selected_post['engagement_rate'] - er_benchmark
        st.metric(
            "Engagement Rate",
            f"{selected_post['engagement_rate']:.2f}%",
            delta=f"{er_delta:+.2f}% vs 5% benchmark",
            delta_color="normal"
        )
        
        # Share of Voice
        st.metric(
            "Share of Voice",
            f"{selected_post['share_of_voice']:.2f}%",
            help="(Saves + Shares) / Impressions - measures virality"
        )
        
        # Profile Conversion
        st.metric(
            "Profile Conversion",
            f"{selected_post['profile_conversion']:.2f}%",
            help="Link Clicks / Profile Visits - traffic generation"
        )
        
        # Scores
        score_col1, score_col2 = st.columns(2)
        with score_col1:
            st.metric("🏆 Virality Score", f"{int(selected_post['virality_score']):,}")
        with score_col2:
            st.metric("🔗 Conversion Score", f"{int(selected_post['conversion_score']):,}")
        
        # Performance badges
        st.markdown("---")
        st.markdown("**🏅 Performance Badges:**")
        
        if selected_post['virality_score'] == df_filtered['virality_score'].max():
            st.success("🏆 Most Viral Post")
        if selected_post['conversion_score'] == df_filtered['conversion_score'].max():
            st.info("🔗 Highest Conversion")
        if selected_post['comments'] == df_filtered['comments'].max():
            st.warning("💬 Most Engaging")
        if selected_post['engagement_rate'] >= 5.0:
            st.success("✅ Above Benchmark ER")
    
    # Caption
    st.markdown("---")
    st.markdown("### 📝 Post Caption")
    st.write(selected_post['caption'])

else:
    st.info("👆 Click on any row in the table above to see detailed post information")

# ============================================
# FOOTER INFO
# ============================================

st.markdown("---")
st.markdown("""
<div class='info-box'>
<h4>💡 How to Use This Table:</h4>
<ul>
    <li><strong>Sort:</strong> Click on column headers to sort</li>
    <li><strong>Filter:</strong> Click the filter icon (☰) on the right sidebar to add filters per column</li>
    <li><strong>Search:</strong> Use the sidebar search to find specific posts</li>
    <li><strong>Multi-column Sort:</strong> Hold Shift and click multiple headers</li>
    <li><strong>Select:</strong> Click any row to see detailed post information below</li>
    <li><strong>Resize:</strong> Drag column borders to adjust width</li>
</ul>
</div>
""", unsafe_allow_html=True)

# Export functionality
st.markdown("---")
if st.button("📥 Export Current View to CSV", type="primary"):
    csv = df_filtered.to_csv(index=False)
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name=f"content_library_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv"
    )