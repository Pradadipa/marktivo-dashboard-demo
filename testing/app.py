import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder

# ============================================
# PAGE CONFIG
# ============================================
st.set_page_config(
    page_title="Content Library - Simple",
    page_icon="📚",
    layout="wide"
)

# ============================================
# SIMPLE DATA - HANYA 10 POSTS
# ============================================
@st.cache_data
def load_data():
    """Simple data - only 10 posts for quick testing"""
    
    data = {
        'post_id': ['POST_001', 'POST_002', 'POST_003', 'POST_004', 'POST_005', 
                    'POST_006', 'POST_007', 'POST_008', 'POST_009', 'POST_010'],
        
        'platform': ['Instagram', 'TikTok', 'YouTube', 'LinkedIn', 'Instagram',
                     'TikTok', 'Instagram', 'YouTube', 'LinkedIn', 'TikTok'],
        
        'post_type': ['Reel', 'Video', 'Short', 'Post', 'Feed',
                      'Video', 'Reel', 'Video', 'Post', 'Video'],
        
        'date': ['2025-02-08', '2025-02-07', '2025-02-06', '2025-02-05', '2025-02-04',
                 '2025-02-03', '2025-02-02', '2025-02-01', '2025-01-31', '2025-01-30'],
        
        'views': [15000, 85000, 12000, 3500, 8000,
                  125000, 22000, 18000, 4200, 95000],
        
        'likes': [1200, 8500, 960, 280, 640,
                  12500, 1980, 1440, 336, 9500],
        
        'comments': [85, 420, 48, 15, 32,
                     625, 99, 72, 18, 475],
        
        'shares': [145, 850, 96, 28, 64,
                   1250, 198, 144, 34, 950],
        
        'link_clicks': [125, 680, 85, 42, 56,
                        890, 165, 120, 38, 720],
        
        'engagement_rate': [9.5, 11.2, 8.8, 4.2, 7.8,
                           10.5, 9.2, 8.5, 3.9, 10.8],
        
        'virality_score': [25000, 125000, 18000, 5500, 12000,
                          185000, 35000, 28000, 6800, 145000],
        
        'conversion_score': [15000, 82000, 10200, 5040, 6720,
                            106800, 19800, 14400, 4560, 86400],
        
        'thumbnail': ['https://picsum.photos/seed/1/300/300',
                     'https://picsum.photos/seed/2/300/300',
                     'https://picsum.photos/seed/3/300/300',
                     'https://picsum.photos/seed/4/300/300',
                     'https://picsum.photos/seed/5/300/300',
                     'https://picsum.photos/seed/6/300/300',
                     'https://picsum.photos/seed/7/300/300',
                     'https://picsum.photos/seed/8/300/300',
                     'https://picsum.photos/seed/9/300/300',
                     'https://picsum.photos/seed/10/300/300']
    }
    
    return pd.DataFrame(data)

# ============================================
# MAIN APP
# ============================================

st.title("📚 Content Library (Simple Version)")
st.markdown("---")

# Load data
df = load_data()

st.success(f"✅ Loaded {len(df)} posts")

# ============================================
# SIMPLE FILTERS
# ============================================

col1, col2 = st.columns(2)

with col1:
    platforms = st.multiselect(
        "Platform",
        options=df['platform'].unique(),
        default=df['platform'].unique()
    )

with col2:
    sort_by = st.selectbox(
        "Sort by",
        ["Virality Score", "Engagement Rate", "Views", "Link Clicks"]
    )

# Apply filters
if not platforms:
    platforms = df['platform'].unique()

df_filtered = df[df['platform'].isin(platforms)].copy()

# Apply sorting
sort_map = {
    "Virality Score": 'virality_score',
    "Engagement Rate": 'engagement_rate',
    "Views": 'views',
    "Link Clicks": 'link_clicks'
}
df_filtered = df_filtered.sort_values(sort_map[sort_by], ascending=False)

st.info(f"📊 Showing {len(df_filtered)} posts")

st.markdown("---")

# ============================================
# AG GRID TABLE
# ============================================

st.subheader("📋 Posts Table")

# Prepare display columns
display_df = df_filtered[[
    'post_id',
    'platform',
    'post_type',
    'date',
    'views',
    'likes',
    'comments',
    'shares',
    'link_clicks',
    'engagement_rate',
    'virality_score',
    'conversion_score',
    'thumbnail'
]].copy()

# Configure grid
gb = GridOptionsBuilder.from_dataframe(display_df)

gb.configure_default_column(
    resizable=True,
    filterable=True,
    sortable=True
)

gb.configure_pagination(paginationAutoPageSize=True)
gb.configure_selection('single')

# Column configs
gb.configure_column("post_id", width=110, pinned='left')
gb.configure_column("platform", width=110)
gb.configure_column("post_type", width=100)
gb.configure_column("date", width=120)
gb.configure_column("views", width=110)
gb.configure_column("likes", width=100)
gb.configure_column("comments", width=110)
gb.configure_column("shares", width=100)
gb.configure_column("link_clicks", width=120)
gb.configure_column("engagement_rate", width=140, header_name="ER (%)")
gb.configure_column("virality_score", width=130)
gb.configure_column("conversion_score", width=150)
gb.configure_column("thumbnail", hide=True)

grid_options = gb.build()

# Display grid
grid_response = AgGrid(
    display_df,
    gridOptions=grid_options,
    update_on=['selectionChanged'],
    theme='streamlit',
    height=400
)

st.markdown("---")

# ============================================
# SELECTED POST DETAILS
# ============================================

if grid_response['selected_rows'] is not None and len(grid_response['selected_rows']) > 0:
    selected = pd.DataFrame(grid_response['selected_rows']).iloc[0]
    
    st.subheader(f"🔍 Selected: {selected['post_id']}")
    
    col1, col2, col3 = st.columns([2, 3, 3])
    
    with col1:
        st.markdown("### 📸 Thumbnail")
        st.image(selected['thumbnail'], use_column_width=True)
        st.markdown(f"**{selected['platform']}**")
        st.caption(f"{selected['post_type']} • {selected['date']}")
    
    with col2:
        st.markdown("### 📊 Metrics")
        
        m1, m2 = st.columns(2)
        with m1:
            st.metric("Views", f"{int(selected['views']):,}")
            st.metric("Likes", f"{int(selected['likes']):,}")
        with m2:
            st.metric("Comments", f"{int(selected['comments']):,}")
            st.metric("Shares", f"{int(selected['shares']):,}")
    
    with col3:
        st.markdown("### 🎯 Performance")
        
        st.metric(
            "Engagement Rate",
            f"{selected['engagement_rate']:.1f}%",
            delta=f"{selected['engagement_rate'] - 5:.1f}% vs 5% benchmark"
        )
        
        st.metric("Link Clicks", f"{int(selected['link_clicks']):,}")
        
        p1, p2 = st.columns(2)
        with p1:
            st.metric("Virality", f"{int(selected['virality_score']):,}")
        with p2:
            st.metric("Conversion", f"{int(selected['conversion_score']):,}")
        
        # Badges
        if selected['virality_score'] == df_filtered['virality_score'].max():
            st.success("🏆 Most Viral")
        if selected['engagement_rate'] >= 5:
            st.success("✅ Above Benchmark")

else:
    st.info("👆 Click any row to see details")

st.markdown("---")

# ============================================
# SUMMARY
# ============================================

st.subheader("📈 Summary")

s1, s2, s3, s4 = st.columns(4)

with s1:
    st.metric("Total Posts", len(df_filtered))

with s2:
    st.metric("Avg Views", f"{df_filtered['views'].mean():,.0f}")

with s3:
    st.metric("Avg ER", f"{df_filtered['engagement_rate'].mean():.1f}%")

with s4:
    st.metric("Total Clicks", f"{df_filtered['link_clicks'].sum():,}")

# ============================================
# EXPORT
# ============================================

st.markdown("---")

if st.button("📥 Export to CSV"):
    csv = df_filtered.drop('thumbnail', axis=1).to_csv(index=False)
    st.download_button(
        "Download",
        csv,
        "content_library.csv",
        "text/csv"
    )