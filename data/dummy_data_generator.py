"""
Marktivo Growth OS - Dummy Data Generator
Generates realistic marketing data for all modules
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set seed for reproducibility
np.random.seed(42)
random.seed(42)

class MarketingDataGenerator:
    """Generate dummy marketing data for Marktivo Growth OS"""
    
    def __init__(self, days=90):
        """
        Initialize generator
        
        Args:
            days (int): Number of days of historical data to generate
        """
        self.days = days
        self.end_date = datetime.now()
        self.start_date = self.end_date - timedelta(days=days)
        
    def generate_date_range(self):
        """Generate date range"""
        return pd.date_range(
            start=self.start_date,
            end=self.end_date,
            freq='D'
        )
    
    # ========================================
    # MODULE 1: REVENUE ENGINEERING DATA
    # ========================================
    
    def generate_revenue_data(self):
        """Generate revenue engineering data (funnel campaigns)"""
        
        dates = self.generate_date_range()
        data = []
        
        funnel_stages = ['TOF', 'MOF', 'BOF', 'RET']
        
        for date in dates:
            # Add some trend and seasonality
            day_of_week = date.dayofweek
            trend_factor = 1 + (date - self.start_date).days / self.days * 0.3
            weekend_factor = 0.7 if day_of_week >= 5 else 1.0
            
            for stage in funnel_stages:
                # Base metrics vary by funnel stage
                if stage == 'TOF':
                    base_spend = 5000
                    base_impressions = 500000
                    base_ctr = 2.5
                    base_cpa = 25
                    base_orders = 150
                elif stage == 'MOF':
                    base_spend = 3000
                    base_impressions = 200000
                    base_ctr = 3.5
                    base_cpa = 20
                    base_orders = 120
                elif stage == 'BOF':
                    base_spend = 2000
                    base_impressions = 100000
                    base_ctr = 5.0
                    base_cpa = 15
                    base_orders = 100
                else:  # RET
                    base_spend = 1000
                    base_impressions = 50000
                    base_ctr = 6.0
                    base_cpa = 10
                    base_orders = 80
                
                # Apply variations
                spend = base_spend * trend_factor * weekend_factor * np.random.uniform(0.85, 1.15)
                impressions = base_impressions * trend_factor * weekend_factor * np.random.uniform(0.9, 1.1)
                clicks = impressions * (base_ctr / 100) * np.random.uniform(0.9, 1.1)
                orders = base_orders * trend_factor * weekend_factor * np.random.uniform(0.85, 1.15)
                
                # Calculate metrics
                ctr = (clicks / impressions) * 100 if impressions > 0 else 0
                cpm = (spend / impressions) * 1000 if impressions > 0 else 0
                cpc = spend / clicks if clicks > 0 else 0
                cpa = spend / orders if orders > 0 else 0
                
                # Revenue (AOV varies by stage)
                aov = np.random.uniform(80, 150) if stage != 'RET' else np.random.uniform(100, 200)
                revenue = orders * aov
                roas = revenue / spend if spend > 0 else 0
                contribution = revenue - spend
                conv_rate = (orders / clicks) * 100 if clicks > 0 else 0
                
                data.append({
                    'date': date.strftime('%Y-%m-%d'),
                    'funnel_stage': stage,
                    'spend': round(spend, 2),
                    'impressions': int(impressions),
                    'clicks': int(clicks),
                    'orders': int(orders),
                    'revenue': round(revenue, 2),
                    'ctr': round(ctr, 2),
                    'cpm': round(cpm, 2),
                    'cpc': round(cpc, 2),
                    'cpa': round(cpa, 2),
                    'roas': round(roas, 2),
                    'aov': round(aov, 2),
                    'contribution': round(contribution, 2),
                    'conv_rate': round(conv_rate, 2)
                })
        
        # Add some UNCATEGORIZED data (errors)
        uncategorized_dates = random.sample(list(dates), k=5)
        for date in uncategorized_dates:
            data.append({
                'date': date.strftime('%Y-%m-%d'),
                'funnel_stage': 'UNCATEGORIZED',
                'spend': round(np.random.uniform(500, 2000), 2),
                'impressions': int(np.random.uniform(10000, 50000)),
                'clicks': int(np.random.uniform(200, 1000)),
                'orders': int(np.random.uniform(10, 50)),
                'revenue': round(np.random.uniform(1000, 5000), 2),
                'ctr': 0,
                'cpm': 0,
                'cpc': 0,
                'cpa': 0,
                'roas': 0,
                'aov': 0,
                'contribution': 0,
                'conv_rate': 0
            })
        
        df = pd.DataFrame(data)
        return df.sort_values('date')
    
    def generate_cohort_data(self):
        """Generate cohort LTV data"""
        
        # Generate cohorts for last 6 months
        cohort_months = pd.date_range(
            start=self.end_date - timedelta(days=180),
            end=self.end_date,
            freq='MS'
        )
        
        data = []
        
        for cohort_date in cohort_months:
            cohort_name = cohort_date.strftime('%Y-%m')
            customers = int(np.random.uniform(800, 1500))
            
            # LTV progression (Day 0, 30, 60, 90)
            for day in [0, 30, 60, 90]:
                # LTV grows over time
                if day == 0:
                    ltv = np.random.uniform(80, 120)
                elif day == 30:
                    ltv = np.random.uniform(100, 180)
                elif day == 60:
                    ltv = np.random.uniform(130, 250)
                else:  # 90
                    ltv = np.random.uniform(150, 300)
                
                # Retention rate decreases
                retention = 1.0 if day == 0 else np.random.uniform(0.4, 0.7) * (1 - day/180)
                
                # Second order rate
                second_order_rate = 0 if day == 0 else np.random.uniform(0.15, 0.35)
                
                data.append({
                    'cohort': cohort_name,
                    'acquisition_date': cohort_date.strftime('%Y-%m-%d'),
                    'day': day,
                    'customers': customers,
                    'ltv': round(ltv, 2),
                    'retention_rate': round(retention, 3),
                    'second_order_rate': round(second_order_rate, 3)
                })
        
        return pd.DataFrame(data)
    
    # ========================================
    # MODULE 2: ORGANIC ARCHITECTURE DATA
    # ========================================
    
    def generate_social_data(self):
        """Generate social media metrics"""
        
        dates = self.generate_date_range()
        platforms = ['Instagram', 'TikTok', 'YouTube', 'LinkedIn']
        
        data = []
        
        for date in dates:
            for platform in platforms:
                # Platform-specific base metrics
                if platform == 'Instagram':
                    base_reach = 50000
                    base_engagement = 2500
                    base_followers = 125000
                elif platform == 'TikTok':
                    base_reach = 80000
                    base_engagement = 4000
                    base_followers = 95000
                elif platform == 'YouTube':
                    base_reach = 30000
                    base_engagement = 1500
                    base_followers = 45000
                else:  # LinkedIn
                    base_reach = 15000
                    base_engagement = 800
                    base_followers = 28000
                
                # Apply variations
                reach = int(base_reach * np.random.uniform(0.8, 1.3))
                likes = int(reach * np.random.uniform(0.03, 0.07))
                comments = int(reach * np.random.uniform(0.005, 0.015))
                shares = int(reach * np.random.uniform(0.01, 0.03))
                saves = int(reach * np.random.uniform(0.02, 0.05))
                
                engagement = likes + comments + shares + saves
                engagement_rate = (engagement / reach) * 100 if reach > 0 else 0
                
                profile_visits = int(reach * np.random.uniform(0.1, 0.2))
                link_clicks = int(profile_visits * np.random.uniform(0.15, 0.35))
                
                followers_change = int(np.random.uniform(-50, 200))
                
                data.append({
                    'date': date.strftime('%Y-%m-%d'),
                    'platform': platform,
                    'reach': reach,
                    'impressions': int(reach * np.random.uniform(1.5, 2.5)),
                    'likes': likes,
                    'comments': comments,
                    'shares': shares,
                    'saves': saves,
                    'engagement': engagement,
                    'engagement_rate': round(engagement_rate, 2),
                    'profile_visits': profile_visits,
                    'link_clicks': link_clicks,
                    'profile_cvr': round((link_clicks / profile_visits) * 100, 2) if profile_visits > 0 else 0,
                    'followers': base_followers + followers_change,
                    'followers_change': followers_change
                })
        
        return pd.DataFrame(data)
    
    # ========================================
    # MODULE 3: CRO TERMINAL DATA
    # ========================================
    
    def generate_funnel_data(self):
        """Generate conversion funnel data"""
        
        dates = self.generate_date_range()
        sources = ['TikTok Ads', 'Google Ads', 'Facebook Ads', 'Organic']
        devices = ['Mobile', 'Desktop']
        
        data = []
        
        for date in dates:
            for source in sources:
                for device in devices:
                    # Base funnel numbers
                    sessions = int(np.random.uniform(1000, 5000))
                    
                    # Remove bot traffic (5-15%)
                    bot_sessions = int(sessions * np.random.uniform(0.05, 0.15))
                    true_sessions = sessions - bot_sessions
                    
                    # Funnel drop-offs
                    product_views = int(true_sessions * np.random.uniform(0.4, 0.7))
                    add_to_cart = int(product_views * np.random.uniform(0.15, 0.35))
                    initiate_checkout = int(add_to_cart * np.random.uniform(0.6, 0.8))
                    purchases = int(initiate_checkout * np.random.uniform(0.4, 0.7))
                    
                    # Metrics
                    bounce_rate = np.random.uniform(0.25, 0.55)
                    avg_session_duration = np.random.uniform(120, 480)  # seconds
                    load_time = np.random.uniform(1.5, 4.0)  # seconds
                    
                    data.append({
                        'date': date.strftime('%Y-%m-%d'),
                        'source': source,
                        'device': device,
                        'total_sessions': sessions,
                        'bot_sessions': bot_sessions,
                        'true_sessions': true_sessions,
                        'product_views': product_views,
                        'add_to_cart': add_to_cart,
                        'initiate_checkout': initiate_checkout,
                        'purchases': purchases,
                        'bounce_rate': round(bounce_rate, 3),
                        'avg_session_duration': round(avg_session_duration, 1),
                        'load_time_lcp': round(load_time, 2),
                        'cvr': round((purchases / true_sessions) * 100, 2) if true_sessions > 0 else 0,
                        'cart_abandonment': round((1 - purchases/add_to_cart) * 100, 2) if add_to_cart > 0 else 0
                    })
        
        return pd.DataFrame(data)
    
    # ========================================
    # MODULE 4: REVOPS DATA
    # ========================================
    
    def generate_revops_data(self):
        """Generate RevOps/Sales pipeline data"""
        
        dates = self.generate_date_range()
        
        data = []
        
        for date in dates:
            # Lead generation
            leads_generated = int(np.random.uniform(50, 150))
            
            # AI qualification
            ai_qualified = int(leads_generated * np.random.uniform(0.6, 0.8))
            ai_response_time = np.random.uniform(10, 20)  # seconds
            
            # Human handling
            human_contacted = int(ai_qualified * np.random.uniform(0.5, 0.8))
            human_response_time = np.random.uniform(2, 8) * 3600  # hours to seconds
            
            # Deals
            deals_won = int(human_contacted * np.random.uniform(0.2, 0.4))
            avg_deal_size = np.random.uniform(1000, 5000)
            revenue = deals_won * avg_deal_size
            
            # Calculate fumbled leads
            fumbled_leads = ai_qualified - human_contacted
            fumble_rate = (fumbled_leads / ai_qualified) * 100 if ai_qualified > 0 else 0
            
            # Pipeline velocity
            avg_days_to_close = np.random.uniform(3, 14)
            
            data.append({
                'date': date.strftime('%Y-%m-%d'),
                'leads_generated': leads_generated,
                'ai_qualified': ai_qualified,
                'ai_response_time_sec': round(ai_response_time, 1),
                'human_contacted': human_contacted,
                'human_response_time_sec': round(human_response_time, 1),
                'fumbled_leads': fumbled_leads,
                'fumble_rate': round(fumble_rate, 2),
                'deals_won': deals_won,
                'avg_deal_size': round(avg_deal_size, 2),
                'revenue': round(revenue, 2),
                'pipeline_velocity_days': round(avg_days_to_close, 1)
            })
        
        return pd.DataFrame(data)
    
    # ========================================
    # GENERATE ALL DATA
    # ========================================
    
    def generate_all(self, save_to_csv=True):
        """Generate all datasets"""
        
        print("🔄 Generating dummy data...")
        
        datasets = {
            'revenue_data': self.generate_revenue_data(),
            'cohort_data': self.generate_cohort_data(),
            'social_data': self.generate_social_data(),
            'funnel_data': self.generate_funnel_data(),
            'revops_data': self.generate_revops_data()
        }
        
        if save_to_csv:
            print("\n💾 Saving to CSV files...")
            for name, df in datasets.items():
                filepath = f'data/processed/{name}.csv'
                df.to_csv(filepath, index=False)
                print(f"  ✅ Saved: {filepath} ({len(df)} rows)")
        
        print("\n✅ All data generated successfully!")
        
        return datasets

# ========================================
# RUN GENERATOR
# ========================================

if __name__ == "__main__":
    generator = MarketingDataGenerator(days=90)
    datasets = generator.generate_all(save_to_csv=True)
    
    # Print summaries
    print("\n📊 DATA SUMMARY:")
    print("="*50)
    for name, df in datasets.items():
        print(f"\n{name.upper()}:")
        print(f"  Rows: {len(df)}")
        print(f"  Columns: {len(df.columns)}")
        print(f"  Date range: {df['date'].min()} to {df['date'].max()}")