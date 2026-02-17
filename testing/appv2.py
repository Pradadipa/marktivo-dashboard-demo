import streamlit as st
import pandas as pd

# ============================================
# PAGE CONFIG
# ============================================
st.set_page_config(
    page_title="Content Library - With Thumbnails",
    page_icon="📚",
    layout="wide"
)

# ============================================
# CUSTOM CSS
# ============================================
st.markdown("""
<style>
    /* Dark mode styling */
    .stApp {
        background-color: #0e1117;
    }
    
    h1, h2, h3 {
        color: #667eea !important;
    }
    
    /* Make dataframe rows taller for thumbnails */
    .stDataFrame {
        font-size: 13px;
    }
</style>
""", unsafe_allow_html=True)

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
        
        'thumbnail': ['https://picsum.photos/seed/1/400/400',
                     'https://picsum.photos/seed/2/400/400',
                     'https://picsum.photos/seed/3/400/400',
                     'https://picsum.photos/seed/4/400/400',
                     'https://picsum.photos/seed/5/400/400',
                     'https://picsum.photos/seed/6/400/400',
                     'https://picsum.photos/seed/7/400/400',
                     'https://picsum.photos/seed/8/400/400',
                     'https://picsum.photos/seed/9/400/400',
                     'https://picsum.photos/seed/10/400/400']
    }
    
    return pd.DataFrame(data)

# ============================================
# MAIN APP
# ============================================

st.title("📚 Content Library with Thumbnails")
st.markdown("*Visual content library with inline thumbnail previews*")
st.markdown("---")

# Load data
df = load_data()

st.success(f"✅ Loaded {len(df)} posts")

# ============================================
# SIMPLE FILTERS
# ============================================

col1, col2, col3 = st.columns(3)

with col1:
    platforms = st.multiselect(
        "Platform",
        options=sorted(df['platform'].unique()),
        default=df['platform'].unique()
    )

with col2:
    sort_by = st.selectbox(
        "Sort by",
        ["Virality Score", "Engagement Rate", "Views", "Link Clicks", "Recent First"]
    )

with col3:
    show_cols = st.multiselect(
        "Show Columns",
        options=["All", "Engagement Only", "Traffic Only"],
        default=["All"]
    )

# Apply filters
if not platforms:
    platforms = df['platform'].unique()

df_filtered = df[df['platform'].isin(platforms)].copy()

# Apply sorting
sort_map = {
    "Virality Score": ('virality_score', False),
    "Engagement Rate": ('engagement_rate', False),
    "Views": ('views', False),
    "Link Clicks": ('link_clicks', False),
    "Recent First": ('date', False)
}
sort_col, sort_asc = sort_map[sort_by]
df_filtered = df_filtered.sort_values(sort_col, ascending=sort_asc)

st.info(f"📊 Showing {len(df_filtered)} posts • Sorted by **{sort_by}**")

st.markdown("---")

# ============================================
# TABLE WITH THUMBNAILS
# ============================================

st.subheader("📋 Content Performance Table")

# Determine which columns to show
if "Engagement Only" in show_cols:
    display_columns = ['thumbnail', 'post_id', 'platform', 'post_type', 'date', 
                      'views', 'likes', 'comments', 'shares', 'engagement_rate', 'virality_score']
elif "Traffic Only" in show_cols:
    display_columns = ['thumbnail', 'post_id', 'platform', 'post_type', 'date',
                      'views', 'link_clicks', 'conversion_score']
else:  # All
    display_columns = ['thumbnail', 'post_id', 'platform', 'post_type', 'date',
                      'views', 'likes', 'comments', 'shares', 'link_clicks',
                      'engagement_rate', 'virality_score', 'conversion_score']

display_df = df_filtered[display_columns].copy()
display_df = display_df.reset_index(drop=True)

# Display interactive dataframe with thumbnails
event = st.dataframe(
    display_df,
    use_container_width=True,
    height=600,
    on_select="rerun",
    selection_mode="single-row",
    column_config={
        "thumbnail": st.column_config.ImageColumn(
            "📸 Preview",
            width="medium",
            help="Post thumbnail image"
        ),
        "post_id": st.column_config.TextColumn(
            "Post ID",
            width="small"
        ),
        "platform": st.column_config.TextColumn(
            "Platform",
            width="small"
        ),
        "post_type": st.column_config.TextColumn(
            "Type",
            width="small"
        ),
        "date": st.column_config.DateColumn(
            "Published",
            width="medium",
            format="YYYY-MM-DD"
        ),
        "views": st.column_config.NumberColumn(
            "👁️ Views",
            width="small",
            format="%d"
        ),
        "likes": st.column_config.NumberColumn(
            "❤️ Likes",
            width="small",
            format="%d"
        ),
        "comments": st.column_config.NumberColumn(
            "💬 Comments",
            width="small",
            format="%d"
        ),
        "shares": st.column_config.NumberColumn(
            "🔄 Shares",
            width="small",
            format="%d"
        ),
        "link_clicks": st.column_config.NumberColumn(
            "🔗 Clicks",
            width="small",
            format="%d"
        ),
        "engagement_rate": st.column_config.NumberColumn(
            "📊 ER (%)",
            width="small",
            format="%.1f"
        ),
        "virality_score": st.column_config.NumberColumn(
            "🏆 Virality",
            width="medium",
            format="%d"
        ),
        "conversion_score": st.column_config.NumberColumn(
            "🎯 Conversion",
            width="medium",
            format="%d"
        ),
    },
    hide_index=True
)

st.markdown("---")

# ============================================
# SELECTED POST DETAILS
# ============================================

if event.selection.rows:
    selected_idx = event.selection.rows[0]
    selected = df_filtered.iloc[selected_idx]
    
    st.markdown(f"""
    <div style='background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); 
                color: white; padding: 15px; border-radius: 8px; margin-bottom: 20px;'>
        <h3 style='margin: 0; color: white !important;'>
            🔍 Selected: {selected['post_id']} - {selected['platform']} {selected['post_type']}
        </h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([2, 3, 3])
    
    with col1:
        st.markdown("### 📸 Full Preview")
        st.image(selected['thumbnail'], use_container_width=True)
        
        platform_emoji = {
            'Instagram': '📷',
            'TikTok': '🎵',
            'YouTube': '▶️',
            'LinkedIn': '💼'
        }
        emoji = platform_emoji.get(selected['platform'], '📱')
        
        st.markdown(f"**{emoji} {selected['platform']}**")
        st.caption(f"{selected['post_type']} • {selected['date']}")
        st.caption(f"Post ID: `{selected['post_id']}`")
    
    with col2:
        st.markdown("### 📊 Engagement Metrics")
        
        m1, m2 = st.columns(2)
        with m1:
            st.metric("👁️ Views", f"{int(selected['views']):,}")
            st.metric("❤️ Likes", f"{int(selected['likes']):,}")
        with m2:
            st.metric("💬 Comments", f"{int(selected['comments']):,}")
            st.metric("🔄 Shares", f"{int(selected['shares']):,}")
    
    with col3:
        st.markdown("### 🎯 Performance")
        
        st.metric(
            "📊 Engagement Rate",
            f"{selected['engagement_rate']:.1f}%",
            delta=f"{selected['engagement_rate'] - 5:.1f}% vs 5% benchmark",
            delta_color="normal"
        )
        
        st.metric("🔗 Link Clicks", f"{int(selected['link_clicks']):,}")
        
        p1, p2 = st.columns(2)
        with p1:
            st.metric("🏆 Virality", f"{int(selected['virality_score']):,}")
        with p2:
            st.metric("🎯 Conversion", f"{int(selected['conversion_score']):,}")
        
        st.markdown("---")
        
        # Performance badges
        badges = []
        if selected['virality_score'] == df_filtered['virality_score'].max():
            badges.append("🏆 Most Viral")
        if selected['engagement_rate'] >= 5:
            badges.append("✅ Above Benchmark")
        if selected['link_clicks'] == df_filtered['link_clicks'].max():
            badges.append("🔗 Best Traffic")
        
        if badges:
            for badge in badges:
                st.success(badge)

else:
    st.info("👆 **Click any row in the table above** to see detailed post analysis with full-size preview")

st.markdown("---")

# ============================================
# SUMMARY STATISTICS
# ============================================

st.subheader("📈 Summary Statistics")

s1, s2, s3, s4, s5 = st.columns(5)

with s1:
    st.metric("Total Posts", len(df_filtered))

with s2:
    st.metric("Avg Views", f"{df_filtered['views'].mean():,.0f}")

with s3:
    st.metric("Avg ER", f"{df_filtered['engagement_rate'].mean():.1f}%")

with s4:
    st.metric("Total Clicks", f"{df_filtered['link_clicks'].sum():,}")

with s5:
    best_post = df_filtered.loc[df_filtered['virality_score'].idxmax()]
    st.metric("Top Performer", best_post['post_id'])

# ============================================
# PLATFORM BREAKDOWN
# ============================================

st.markdown("---")
st.subheader("🌐 Performance by Platform")

platform_stats = df_filtered.groupby('platform').agg({
    'views': 'sum',
    'engagement_rate': 'mean',
    'link_clicks': 'sum',
    'virality_score': 'mean',
    'post_id': 'count'
}).round(2)

platform_stats.columns = ['Total Views', 'Avg ER (%)', 'Total Clicks', 'Avg Virality', 'Posts']
platform_stats = platform_stats.sort_values('Total Views', ascending=False)

st.dataframe(
    platform_stats,
    use_container_width=True,
    column_config={
        "Total Views": st.column_config.NumberColumn("👁️ Total Views", format="%d"),
        "Avg ER (%)": st.column_config.NumberColumn("📊 Avg ER", format="%.1f%%"),
        "Total Clicks": st.column_config.NumberColumn("🔗 Total Clicks", format="%d"),
        "Avg Virality": st.column_config.NumberColumn("🏆 Avg Virality", format="%d"),
        "Posts": st.column_config.NumberColumn("📝 Posts", format="%d")
    }
)

# ============================================
# EXPORT
# ============================================

st.markdown("---")

export_col1, export_col2 = st.columns(2)

with export_col1:
    if st.button("📥 Export Data to CSV", type="primary", use_container_width=True):
        csv = df_filtered.drop('thumbnail', axis=1).to_csv(index=False)
        st.download_button(
            "⬇️ Download CSV File",
            csv,
            f"content_library_{sort_by.replace(' ', '_').lower()}.csv",
            "text/csv",
            use_container_width=True
        )

with export_col2:
    if st.button("📊 Export Platform Stats", use_container_width=True):
        csv_stats = platform_stats.to_csv()
        st.download_button(
            "⬇️ Download Stats CSV",
            csv_stats,
            "platform_statistics.csv",
            "text/csv",
            use_container_width=True
        )

# ============================================
# FOOTER
# ============================================

st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 20px;'>
    <p style='color: #667eea; font-weight: 600;'>💡 Pro Tips:</p>
    <p style='color: #888; font-size: 13px;'>
        • Click column headers to sort • Click rows to see full details • 
        Use filters to narrow down results • Export data for further analysis
    </p>
</div>
""", unsafe_allow_html=True)
# ============================================
# END OF FILE
