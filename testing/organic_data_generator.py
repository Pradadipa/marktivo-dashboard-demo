# organic_data_generator.py
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def generate_sample_organic_data():
    """
    Simulate data yang biasanya didapat dari API platform
    Untuk production: replace dengan actual API calls
    """
    
    platforms = ['Instagram', 'TikTok', 'YouTube', 'LinkedIn']
    
    # 1. FOLLOWER GROWTH DATA (untuk Ticker Tape)
    follower_data = []
    for platform in platforms:
        growth = random.randint(-50, 2000) if platform != 'LinkedIn' else random.randint(-10, 100)
        follower_data.append({
            'platform': platform,
            'current_followers': random.randint(10000, 500000),
            'growth_7d': growth,
            'growth_percentage': round((growth / random.randint(50000, 200000)) * 100, 2)
        })
    
    df_followers = pd.DataFrame(follower_data)
    
    # 2. CONTENT POSTS DATA (untuk Content Library)
    posts_data = []
    post_types = ['Reel', 'Story', 'Feed', 'Video', 'Short', 'Carousel']
    
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
        
        # Virality & Conversion Scores
        virality_score = views * 0.6 + shares * 100 + saves * 80
        conversion_score = link_clicks * 500 + profile_visits * 50
        
        posts_data.append({
            'post_id': f'POST_{i+1:03d}',
            'platform': platform,
            'post_type': post_type,
            'published_date': (datetime.now() - timedelta(days=random.randint(1, 30))).strftime('%Y-%m-%d'),
            'thumbnail_url': f'https://picsum.photos/400/400?random={i}',  # Demo thumbnail
            'caption': f'Sample post content {i+1}...',
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
            'virality_score': int(virality_score),
            'conversion_score': int(conversion_score)
        })
    
    df_posts = pd.DataFrame(posts_data)
    
    return df_followers, df_posts

if __name__ == "__main__":
    followers_df, posts_df = generate_sample_organic_data()
    # Save to CSV for testing purposes
    followers_df.to_csv('sample_followers_data.csv', index=False)
    posts_df.to_csv('sample_posts_data.csv', index=False)
    print("Sample organic data generated and saved to CSV files.")