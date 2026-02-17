import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import random

# ============================================================
# 2. DUMMY DATA GENERATORS
# ============================================================

def generate_traffic_data(days=30):
    """
    Generate daily website traffic data simulating Shopify + GA4 + Cloudflare.
    
    Includes:
    - Total sessions (raw, including bots)
    - Bot sessions (filtered out)
    - Human sessions ("True Traffic")
    - Breakdown by device (Mobile, Desktop, Tablet)
    - Breakdown by source (Google Ads, Meta Ads, TikTok Ads, Organic, Direct, Email, Social)
    """
    np.random.seed(42)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    dates = pd.date_range(start=start_date, end=end_date, freq='D')

    all_data = []

    for date in dates:
        # Base traffic with day-of-week patterns
        weekday = date.weekday()
        is_weekend = weekday >= 5

        # Total raw sessions (including bots)
        base_sessions = np.random.randint(3500, 6500)
        if is_weekend:
            base_sessions = int(base_sessions * 1.25)  # Weekend boost

        # Bot traffic: 15-30% of total (realistic for e-commerce)
        bot_pct = np.random.uniform(0.15, 0.30)
        bot_sessions = int(base_sessions * bot_pct)
        human_sessions = base_sessions - bot_sessions

        # Bot breakdown
        bot_sub_1s = int(bot_sessions * np.random.uniform(0.40, 0.60))  # Sessions < 1 second
        bot_known_ips = int(bot_sessions * np.random.uniform(0.20, 0.35))  # Known bot IPs
        bot_no_js = bot_sessions - bot_sub_1s - bot_known_ips  # No JavaScript execution

        # Device breakdown (human sessions only)
        mobile_pct = np.random.uniform(0.62, 0.72)  # Mobile dominant (Shopify typical)
        desktop_pct = np.random.uniform(0.22, 0.30)
        tablet_pct = 1.0 - mobile_pct - desktop_pct

        mobile_sessions = int(human_sessions * mobile_pct)
        desktop_sessions = int(human_sessions * desktop_pct)
        tablet_sessions = human_sessions - mobile_sessions - desktop_sessions

        # Source breakdown (human sessions only)
        source_pcts = {
            "Google Ads": np.random.uniform(0.20, 0.28),
            "Meta Ads": np.random.uniform(0.18, 0.25),
            "TikTok Ads": np.random.uniform(0.08, 0.15),
            "Organic Search": np.random.uniform(0.12, 0.18),
            "Direct": np.random.uniform(0.10, 0.15),
            "Email": np.random.uniform(0.05, 0.10),
        }
        # Normalize + remainder = Social Organic
        total_pct = sum(source_pcts.values())
        source_pcts = {k: v / total_pct * 0.92 for k, v in source_pcts.items()}
        source_pcts["Social Organic"] = 1.0 - sum(source_pcts.values())

        source_sessions = {}
        remaining = human_sessions
        for src, pct in list(source_pcts.items())[:-1]:
            s = int(human_sessions * pct)
            source_sessions[src] = s
            remaining -= s
        source_sessions["Social Organic"] = remaining

        # Page load time (LCP) — Mobile slower than Desktop
        lcp_mobile = round(np.random.uniform(2.0, 4.5), 1)
        lcp_desktop = round(np.random.uniform(1.2, 2.8), 1)

        # Occasional speed spikes (simulates issues)
        if np.random.random() < 0.08:
            lcp_mobile = round(np.random.uniform(4.0, 6.5), 1)

        all_data.append({
            "date": date,
            "total_sessions": base_sessions,
            "bot_sessions": bot_sessions,
            "human_sessions": human_sessions,
            "bot_sub_1s": bot_sub_1s,
            "bot_known_ips": bot_known_ips,
            "bot_no_js": bot_no_js,
            "bot_pct": round(bot_pct * 100, 1),
            "mobile_sessions": mobile_sessions,
            "desktop_sessions": desktop_sessions,
            "tablet_sessions": tablet_sessions,
            "lcp_mobile": lcp_mobile,
            "lcp_desktop": lcp_desktop,
            **{f"src_{k.lower().replace(' ', '_')}": v for k, v in source_sessions.items()},
        })

    return pd.DataFrame(all_data)


def generate_funnel_data(days=30):
    """
    Generate Shopify conversion funnel data (daily).
    
    Funnel steps:
    1. Landing Page (= human sessions)
    2. Product Page View
    3. Add to Cart
    4. Initiate Checkout
    5. Purchase (completed order)
    
    Also generates per-device and per-source funnel breakdowns.
    """
    np.random.seed(42)
    traffic_df = generate_traffic_data(days=days)

    all_data = []

    for _, row in traffic_df.iterrows():
        date = row["date"]
        human_sessions = row["human_sessions"]

        # --- Overall Funnel (realistic Shopify drop-offs) ---
        landing_page = human_sessions
        product_page = int(landing_page * np.random.uniform(0.55, 0.70))
        add_to_cart = int(product_page * np.random.uniform(0.25, 0.40))
        checkout = int(add_to_cart * np.random.uniform(0.50, 0.70))
        purchase = int(checkout * np.random.uniform(0.45, 0.65))

        # Bounce rate
        single_page_sessions = landing_page - product_page
        bounce_rate = single_page_sessions / max(landing_page, 1) * 100

        # Cart abandonment
        cart_abandonment = (add_to_cart - purchase) / max(add_to_cart, 1) * 100

        # True CVR
        true_cvr = purchase / max(human_sessions, 1) * 100

        # AOV (Average Order Value)
        aov = round(np.random.uniform(45, 95), 2)
        revenue = round(purchase * aov, 2)

        all_data.append({
            "date": date,
            "landing_page": landing_page,
            "product_page": product_page,
            "add_to_cart": add_to_cart,
            "checkout": checkout,
            "purchase": purchase,
            "bounce_rate": round(bounce_rate, 1),
            "cart_abandonment": round(cart_abandonment, 1),
            "true_cvr": round(true_cvr, 2),
            "aov": aov,
            "revenue": revenue,
            "lcp_mobile": row["lcp_mobile"],
            "lcp_desktop": row["lcp_desktop"],
            "human_sessions": human_sessions,
        })

    return pd.DataFrame(all_data)


def generate_funnel_by_device(days=30):
    """
    Generate funnel breakdown per device type (Mobile, Desktop, Tablet).
    Mobile typically has worse CVR but more traffic.
    """
    np.random.seed(43)
    traffic_df = generate_traffic_data(days=days)

    device_configs = {
        "Mobile": {
            "session_key": "mobile_sessions",
            "product_rate": (0.45, 0.60),      # Lower browse rate on mobile
            "cart_rate": (0.20, 0.32),          # Lower add-to-cart
            "checkout_rate": (0.45, 0.60),      # Lower checkout completion
            "purchase_rate": (0.35, 0.55),      # Lower purchase rate (friction)
            "bounce_range": (38, 52),
        },
        "Desktop": {
            "session_key": "desktop_sessions",
            "product_rate": (0.60, 0.78),       # Higher browse rate
            "cart_rate": (0.30, 0.45),          # Higher add-to-cart
            "checkout_rate": (0.55, 0.72),      # Higher checkout
            "purchase_rate": (0.50, 0.70),      # Higher purchase (easier form filling)
            "bounce_range": (25, 38),
        },
        "Tablet": {
            "session_key": "tablet_sessions",
            "product_rate": (0.50, 0.68),
            "cart_rate": (0.25, 0.38),
            "checkout_rate": (0.48, 0.65),
            "purchase_rate": (0.42, 0.60),
            "bounce_range": (30, 42),
        },
    }

    all_data = []

    for _, row in traffic_df.iterrows():
        date = row["date"]
        for device, config in device_configs.items():
            sessions = row[config["session_key"]]
            if sessions <= 0:
                continue

            landing = sessions
            product = int(landing * np.random.uniform(*config["product_rate"]))
            cart = int(product * np.random.uniform(*config["cart_rate"]))
            checkout = int(cart * np.random.uniform(*config["checkout_rate"]))
            purchase = int(checkout * np.random.uniform(*config["purchase_rate"]))

            bounce = round(np.random.uniform(*config["bounce_range"]), 1)
            cart_abandon = round((cart - purchase) / max(cart, 1) * 100, 1)
            cvr = round(purchase / max(sessions, 1) * 100, 2)

            all_data.append({
                "date": date,
                "device": device,
                "sessions": sessions,
                "landing_page": landing,
                "product_page": product,
                "add_to_cart": cart,
                "checkout": checkout,
                "purchase": purchase,
                "bounce_rate": bounce,
                "cart_abandonment": cart_abandon,
                "cvr": cvr,
            })

    return pd.DataFrame(all_data)


def generate_funnel_by_source(days=30):
    """
    Generate funnel breakdown per traffic source.
    Paid traffic has higher volume but sometimes lower CVR.
    Organic/Direct tends to have higher CVR (intent-driven).
    """
    np.random.seed(44)
    traffic_df = generate_traffic_data(days=days)

    source_configs = {
        "Google Ads": {
            "session_key": "src_google_ads",
            "product_rate": (0.50, 0.65),
            "cart_rate": (0.25, 0.38),
            "checkout_rate": (0.50, 0.65),
            "purchase_rate": (0.45, 0.62),
        },
        "Meta Ads": {
            "session_key": "src_meta_ads",
            "product_rate": (0.40, 0.55),       # Lower — impulse clicks
            "cart_rate": (0.22, 0.35),
            "checkout_rate": (0.45, 0.60),
            "purchase_rate": (0.40, 0.58),
        },
        "TikTok Ads": {
            "session_key": "src_tiktok_ads",
            "product_rate": (0.35, 0.50),       # Lowest — curiosity clicks
            "cart_rate": (0.18, 0.30),
            "checkout_rate": (0.40, 0.58),
            "purchase_rate": (0.35, 0.55),
        },
        "Organic Search": {
            "session_key": "src_organic_search",
            "product_rate": (0.65, 0.80),       # Highest — high intent
            "cart_rate": (0.35, 0.48),
            "checkout_rate": (0.58, 0.72),
            "purchase_rate": (0.55, 0.70),
        },
        "Direct": {
            "session_key": "src_direct",
            "product_rate": (0.60, 0.75),       # High — returning customers
            "cart_rate": (0.32, 0.45),
            "checkout_rate": (0.55, 0.70),
            "purchase_rate": (0.50, 0.68),
        },
        "Email": {
            "session_key": "src_email",
            "product_rate": (0.55, 0.72),
            "cart_rate": (0.30, 0.42),
            "checkout_rate": (0.52, 0.68),
            "purchase_rate": (0.48, 0.65),
        },
        "Social Organic": {
            "session_key": "src_social_organic",
            "product_rate": (0.38, 0.55),
            "cart_rate": (0.20, 0.32),
            "checkout_rate": (0.42, 0.60),
            "purchase_rate": (0.38, 0.55),
        },
    }

    all_data = []

    for _, row in traffic_df.iterrows():
        date = row["date"]
        for source, config in source_configs.items():
            sessions = row.get(config["session_key"], 0)
            if sessions <= 0:
                continue

            landing = sessions
            product = int(landing * np.random.uniform(*config["product_rate"]))
            cart = int(product * np.random.uniform(*config["cart_rate"]))
            checkout = int(cart * np.random.uniform(*config["checkout_rate"]))
            purchase = int(checkout * np.random.uniform(*config["purchase_rate"]))

            cart_abandon = round((cart - purchase) / max(cart, 1) * 100, 1)
            cvr = round(purchase / max(sessions, 1) * 100, 2)

            all_data.append({
                "date": date,
                "source": source,
                "sessions": sessions,
                "landing_page": landing,
                "product_page": product,
                "add_to_cart": cart,
                "checkout": checkout,
                "purchase": purchase,
                "cart_abandonment": cart_abandon,
                "cvr": cvr,
            })

    return pd.DataFrame(all_data)


def generate_page_speed_data(days=30):
    """
    Generate page speed / Core Web Vitals data.
    Simulates Shopify storefront performance:
    - LCP (Largest Contentful Paint) — main metric
    - FID (First Input Delay)
    - CLS (Cumulative Layout Shift)
    """
    np.random.seed(45)
    end_date = datetime.now()
    dates = pd.date_range(start=end_date - timedelta(days=days), end=end_date, freq='D')

    all_data = []

    for date in dates:
        # Mobile — typically slower
        lcp_mobile = round(np.random.uniform(2.2, 4.2), 1)
        fid_mobile = round(np.random.uniform(80, 250), 0)
        cls_mobile = round(np.random.uniform(0.05, 0.25), 2)

        # Desktop — faster
        lcp_desktop = round(np.random.uniform(1.0, 2.5), 1)
        fid_desktop = round(np.random.uniform(30, 120), 0)
        cls_desktop = round(np.random.uniform(0.02, 0.12), 2)

        # Occasional spikes (app installs, theme changes, etc.)
        if np.random.random() < 0.07:
            lcp_mobile = round(np.random.uniform(4.5, 7.0), 1)
            fid_mobile = round(np.random.uniform(300, 500), 0)

        all_data.append({
            "date": date,
            "lcp_mobile": lcp_mobile,
            "lcp_desktop": lcp_desktop,
            "fid_mobile": fid_mobile,
            "fid_desktop": fid_desktop,
            "cls_mobile": cls_mobile,
            "cls_desktop": cls_desktop,
        })

    return pd.DataFrame(all_data)

# # Run this cell to generate and save the data (only needs to be done once)
# if __name__ == "__main__":
#     traffic_df = generate_traffic_data()
#     funnel_df = generate_funnel_data()
#     funnel_device_df = generate_funnel_by_device()
#     funnel_source_df = generate_funnel_by_source()
#     speed_df = generate_page_speed_data()

#     # Save to CSV for loading in the dashboard
#     path = "../data/module3/"
#     traffic_df.to_csv(path + "traffic_data.csv", index=False)
#     funnel_df.to_csv(path + "funnel_data.csv", index=False)
#     funnel_device_df.to_csv(path + "funnel_by_device.csv", index=False)
#     funnel_source_df.to_csv(path + "funnel_by_source.csv", index=False)
#     speed_df.to_csv(path + "page_speed_data.csv", index=False)
