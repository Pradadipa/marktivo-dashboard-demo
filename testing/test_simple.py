import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# ============================================
# PAGE CONFIG
# ============================================
st.set_page_config(
    page_title="Content Library - Simple Test",
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
    
    for i in range(50):
        platform = random.choice(platforms)
        post_type = random.choice(post_types)
        
        views = random.randint(1000, 500000)
        likes = int(views * random.uniform(0.02, 0.15))
        comments = int(likes * random.uniform(0.05, 0.2))
        shares = int(likes * random.uniform(0.1, 0.3))
        saves = int(likes * random.uniform(0.15, 0.4))
        impressions = int(views * random.uniform(1.2, 2.5))
        profile_visits = int(views * random.uniform(0.01, 0.05))
        link_clicks = int(profile_visits * random.uniform(0.1, 0.4))
        
        engagement_rate = round(((likes + comments + shares) / impressions) * 100, 2)
        share_of_voice = round(((saves + shares) / impressions) * 100, 2)
        profile_conversion = round((link_clicks / profile_visits) * 100, 2) if profile_visits > 0 else 0
        
        virality_score = int(views * 0.6 + shares * 100 + saves * 80)
        conversion_score = int(link_clicks * 500 + profile_visits * 50)
        
        posts_data.append({
            'post_id': f'POST_{i+1:03d}',
            'platform': platform,
            'post_type': post_type,
            'published_date': (datetime.now() - timedelta(days=random.randint(1, 30))).strftime('%Y-%m-%d'),
            'thumbnail_url': f'https://picsum.photos/seed/{i}/300/300',
            'views': views,
            'likes': likes,
            'comments': comments,
            'shares': shares,
            'link_clicks': link_clicks,
            'engagement_rate': engagement_rate,
            'virality_score': virality_score,
            'conversion_score': conversion_score
        })
    
    return pd.DataFrame(posts_data)

# ============================================
# MAIN APP
# ============================================

st.title("📚 Content Library - Streamlit Native Table")
st.markdown("---")

# Generate data
st.write("🔄 Loading data...")
df_posts = generate_sample_posts()
st.success(f"✅ Data loaded: {len(df_posts)} posts")

# ============================================
# FILTERS
# ============================================

st.subheader("🎛️ Filters")

col1, col2 = st.columns(2)

with col1:
    all_platforms = list(df_posts['platform'].unique())
    platform_filter = st.multiselect(
        "Filter by Platform",
        options=all_platforms,
        default=all_platforms
    )

with col2:
    sort_by = st.selectbox(
        "Sort by",
        ["Virality Score", "Engagement Rate", "Views", "Link Clicks"]
    )

# Apply filters
if not platform_filter:
    st.warning("No platform selected")
    platform_filter = all_platforms

df_filtered = df_posts[df_posts['platform'].isin(platform_filter)].copy()

# Apply sorting
if sort_by == "Virality Score":
    df_filtered = df_filtered.sort_values('virality_score', ascending=False)
elif sort_by == "Engagement Rate":
    df_filtered = df_filtered.sort_values('engagement_rate', ascending=False)
elif sort_by == "Views":
    df_filtered = df_filtered.sort_values('views', ascending=False)
else:
    df_filtered = df_filtered.sort_values('link_clicks', ascending=False)

st.info(f"📊 Showing {len(df_filtered)} posts")

# ============================================
# DISPLAY TABLE - STREAMLIT NATIVE
# ============================================

st.subheader("📋 Posts Table")

# Format for display
display_df = df_filtered[[
    'post_id',
    'platform',
    'post_type',
    'published_date',
    'views',
    'likes',
    'comments',
    'shares',
    'link_clicks',
    'engagement_rate',
    'virality_score',
    'conversion_score'
]].head(20).copy()

# Show dataframe
st.dataframe(
    display_df,
    use_container_width=True,
    height=400,
    column_config={
        "post_id": st.column_config.TextColumn("Post ID", width="small"),
        "platform": st.column_config.TextColumn("Platform", width="small"),
        "post_type": st.column_config.TextColumn("Type", width="small"),
        "published_date": st.column_config.DateColumn("Date", width="small"),
        "views": st.column_config.NumberColumn("Views", format="%d"),
        "likes": st.column_config.NumberColumn("Likes", format="%d"),
        "comments": st.column_config.NumberColumn("Comments", format="%d"),
        "shares": st.column_config.NumberColumn("Shares", format="%d"),
        "link_clicks": st.column_config.NumberColumn("Clicks", format="%d"),
        "engagement_rate": st.column_config.NumberColumn("ER %", format="%.2f"),
        "virality_score": st.column_config.NumberColumn("Virality", format="%d"),
        "conversion_score": st.column_config.NumberColumn("Conversion", format="%d"),
    }
)

# ============================================
# SUMMARY STATS
# ============================================

st.markdown("---")
st.subheader("📊 Summary Statistics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Posts", len(df_filtered))
    
with col2:
    st.metric("Avg Views", f"{df_filtered['views'].mean():,.0f}")
    
with col3:
    st.metric("Avg ER", f"{df_filtered['engagement_rate'].mean():.2f}%")
    
with col4:
    st.metric("Total Clicks", f"{df_filtered['link_clicks'].sum():,}")

st.success("✅ If you see data above, Streamlit is working correctly!")