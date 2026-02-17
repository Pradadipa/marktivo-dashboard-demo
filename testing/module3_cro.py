"""
MODULE 3: DATA STEERING (The CRO Terminal)
Mission: Identify and fix "Leaky Buckets" in the customer journey.
Core Philosophy: "Traffic is vanity; Conversion is sanity."

E-commerce Platform: Shopify
CSS: assets/module3_cro.css (to be created)
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import random

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

# Funnel Stage Colors
FUNNEL_COLORS = {
    "Landing Page": NEON_BLUE,
    "Product Page": NEON_PURPLE,
    "Add to Cart": NEON_ORANGE,
    "Checkout": NEON_YELLOW,
    "Purchase": NEON_GREEN,
}

# Device Colors
DEVICE_COLORS = {
    "Mobile": "#E1306C",
    "Desktop": "#00D4FF",
    "Tablet": "#A855F7",
}

# Source Colors
SOURCE_COLORS = {
    "Google Ads": "#4285F4",
    "Meta Ads": "#1877F2",
    "TikTok Ads": "#00F2EA",
    "Organic Search": "#00FF88",
    "Direct": "#FFD700",
    "Email": "#FF6B35",
    "Social Organic": "#A855F7",
}


def load_module3_css():
    """Load Module 3 CSS from external file in assets/ folder."""
    import os
    css_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'module3_cro.css')
    try:
        with open(css_path) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        try:
            with open('assets/module3_cro.css') as f:
                st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
        except FileNotFoundError:
            st.warning("⚠️ CSS file not found: assets/module3_cro.css")


def format_number(num):
    """Format large numbers: 1500 → 1.5K, 1500000 → 1.5M"""
    if num >= 1_000_000:
        return f"{num / 1_000_000:.1f}M"
    elif num >= 1_000:
        return f"{num / 1_000:.1f}K"
    return str(int(num))


# ============================================================
# 2. DUMMY DATA GENERATORS
# ============================================================

@st.cache_data
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


@st.cache_data
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


@st.cache_data
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


@st.cache_data
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


@st.cache_data
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


# ============================================================
# 3. COMPONENT RENDERERS
# ============================================================

def render_bot_filter_stats(traffic_df, is_filtered):
    """
    Section 1: Data Integrity Layer — "The Bouncer"
    Shows bot detection breakdown and True Traffic toggle effect.
    """
    st.markdown('<div style="font-size: 14px; color: #8892A0; text-transform: uppercase; letter-spacing: 2px; padding-bottom: 8px; border-bottom: 1px solid #2D3348; margin-bottom: 16px; margin-top: 24px;">🛡️ DATA INTEGRITY — THE BOUNCER</div>', unsafe_allow_html=True)

    total_bots = traffic_df["bot_sessions"].sum()
    total_raw = traffic_df["total_sessions"].sum()
    total_sub_1s = traffic_df["bot_sub_1s"].sum()
    total_known_ips = traffic_df["bot_known_ips"].sum()
    total_no_js = traffic_df["bot_no_js"].sum()
    bot_pct = total_bots / max(total_raw, 1) * 100

    # Toggle status indicator
    status_color = NEON_GREEN if is_filtered else NEON_YELLOW
    status_text = "ON — Showing True Human Traffic" if is_filtered else "OFF — Showing Raw Traffic (inc. Bots)"

    st.markdown(f"""<div style="display: flex; align-items: center; gap: 8px; padding: 10px 16px; background: linear-gradient(135deg, #1B1F2B 0%, #222838 100%); border: 1px solid #2D3348; border-radius: 8px; margin-bottom: 14px;">
<div style="width: 8px; height: 8px; border-radius: 50%; background: {status_color};"></div>
<span style="font-size: 11px; color: {status_color}; text-transform: uppercase; letter-spacing: 1px; font-weight: 600;">True Traffic Filter: {status_text}</span>
</div>""", unsafe_allow_html=True)

    # Bot breakdown cards
    bot_cols = st.columns(4)
    bot_items = [
        {"label": "Total Bot Sessions", "value": f"{total_bots:,.0f}", "sub": f"{bot_pct:.1f}% of all traffic", "color": NEON_RED, "icon": "🤖"},
        {"label": "Sessions < 1 second", "value": f"{total_sub_1s:,.0f}", "sub": "Automated scrapers", "color": NEON_ORANGE, "icon": "⚡"},
        {"label": "Known Bot IPs", "value": f"{total_known_ips:,.0f}", "sub": "Googlebot, Bingbot, etc.", "color": NEON_YELLOW, "icon": "🌐"},
        {"label": "No JS Execution", "value": f"{total_no_js:,.0f}", "sub": "Headless browsers", "color": NEON_PURPLE, "icon": "🚫"},
    ]

    for idx, item in enumerate(bot_items):
        with bot_cols[idx]:
            st.markdown(f"""<div style="background: linear-gradient(135deg, #1B1F2B 0%, #222838 100%); border: 1px solid #2D3348; border-left: 3px solid {item['color']}; border-radius: 8px; padding: 14px 16px;">
<div style="font-size: 9px; color: #8892A0; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 4px;">{item['icon']} {item['label']}</div>
<div style="font-size: 22px; font-weight: 700; color: {item['color']};">{item['value']}</div>
<div style="font-size: 9px; color: #5A6577; margin-top: 2px;">{item['sub']}</div>
</div>""", unsafe_allow_html=True)


def render_red_alert_funnel(funnel_df):
    """
    Section 2A: The "Red Alert" Funnel — Master Funnel Visualization
    Steps: Landing Page → Product Page → Add to Cart → Checkout → Purchase
    Dynamic Health States: Green/Yellow/Red based on drop-off benchmarks.
    """
    st.markdown('<div style="font-size: 14px; color: #8892A0; text-transform: uppercase; letter-spacing: 2px; padding-bottom: 8px; border-bottom: 1px solid #2D3348; margin-bottom: 16px; margin-top: 24px;">🚨 RED ALERT FUNNEL — MASTER CONVERSION PATH</div>', unsafe_allow_html=True)

    # Aggregate funnel data
    total_landing = funnel_df["landing_page"].sum()
    total_product = funnel_df["product_page"].sum()
    total_cart = funnel_df["add_to_cart"].sum()
    total_checkout = funnel_df["checkout"].sum()
    total_purchase = funnel_df["purchase"].sum()

    stages = [
        {"name": "Landing Page", "value": total_landing, "icon": "🏠"},
        {"name": "Product Page", "value": total_product, "icon": "📦"},
        {"name": "Add to Cart", "value": total_cart, "icon": "🛒"},
        {"name": "Initiate Checkout", "value": total_checkout, "icon": "💳"},
        {"name": "Purchase", "value": total_purchase, "icon": "✅"},
    ]

    # Calculate drop-off rates between stages
    # Benchmarks: what's a "healthy" pass-through rate per step
    benchmarks = {
        "Landing Page → Product Page": {"good": 55, "warning": 40},
        "Product Page → Add to Cart": {"good": 28, "warning": 18},
        "Add to Cart → Initiate Checkout": {"good": 55, "warning": 40},
        "Initiate Checkout → Purchase": {"good": 50, "warning": 35},
    }

    transitions = []
    for i in range(len(stages) - 1):
        from_stage = stages[i]
        to_stage = stages[i + 1]
        pass_rate = to_stage["value"] / max(from_stage["value"], 1) * 100
        drop_rate = 100 - pass_rate
        dropped = from_stage["value"] - to_stage["value"]

        bm_key = f"{from_stage['name']} → {to_stage['name']}"
        bm = benchmarks.get(bm_key, {"good": 50, "warning": 35})

        if pass_rate >= bm["good"]:
            health = "good"
            health_color = NEON_GREEN
            health_label = "HEALTHY"
        elif pass_rate >= bm["warning"]:
            health = "warning"
            health_color = NEON_YELLOW
            health_label = "ATTENTION"
        else:
            health = "bad"
            health_color = NEON_RED
            health_label = "CRITICAL"

        transitions.append({
            "from": from_stage["name"],
            "to": to_stage["name"],
            "pass_rate": pass_rate,
            "drop_rate": drop_rate,
            "dropped": dropped,
            "health": health,
            "health_color": health_color,
            "health_label": health_label,
        })

    # --- Plotly Funnel Chart ---
    col_funnel, col_detail = st.columns([3, 2])

    with col_funnel:
        # Determine colors based on health of INCOMING transition
        stage_colors = [NEON_BLUE]  # Landing page = neutral
        for t in transitions:
            stage_colors.append(t["health_color"])

        fig = go.Figure()

        fig.add_trace(go.Funnel(
            y=[f"{s['icon']} {s['name']}" for s in stages],
            x=[s["value"] for s in stages],
            textposition="auto",
            textinfo="value+percent initial",
            texttemplate="%{value:,.0f}<br><b>%{percentInitial:.1%}</b>",
            textfont=dict(color=TEXT_PRIMARY, size=12),
            marker=dict(
                color=stage_colors,
                line=dict(width=1, color="#2D3348"),
            ),
            connector=dict(
                line=dict(color="#2D3348", width=1),
                fillcolor="rgba(45, 51, 72, 0.2)",
            ),
        ))

        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color=TEXT_SECONDARY, size=12),
            height=380,
            margin=dict(l=10, r=10, t=10, b=10),
            showlegend=False,
        )

        st.plotly_chart(fig, use_container_width=True)

    with col_detail:
        # Drop-off detail cards
        st.markdown("""<div style="font-size: 10px; color: #5A6577; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 12px;">📉 Drop-Off Analysis</div>""", unsafe_allow_html=True)

        for t in transitions:
            st.markdown(f"""<div style="background: linear-gradient(135deg, #1B1F2B 0%, #222838 100%); border: 1px solid #2D3348; border-left: 3px solid {t['health_color']}; border-radius: 8px; padding: 12px 14px; margin-bottom: 8px;">
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
<div style="font-size: 10px; color: #8892A0;">{t['from']} → {t['to']}</div>
<div style="padding: 2px 8px; border-radius: 10px; background: {'rgba(0,255,136,0.12)' if t['health'] == 'good' else ('rgba(255,215,0,0.12)' if t['health'] == 'warning' else 'rgba(255,59,92,0.12)')}; font-size: 8px; font-weight: 700; color: {t['health_color']}; text-transform: uppercase; letter-spacing: 0.8px;">{t['health_label']}</div>
</div>
<div style="display: flex; justify-content: space-between; align-items: baseline;">
<div>
<span style="font-size: 20px; font-weight: 700; color: {t['health_color']};">{t['pass_rate']:.1f}%</span>
<span style="font-size: 10px; color: #5A6577; margin-left: 4px;">pass-through</span>
</div>
<div style="text-align: right;">
<span style="font-size: 12px; color: {NEON_RED};">-{format_number(t['dropped'])}</span>
<span style="font-size: 9px; color: #5A6577; margin-left: 2px;">dropped</span>
</div>
</div>
<div style="width: 100%; height: 3px; background: #2D3348; border-radius: 3px; margin-top: 6px; overflow: hidden;">
<div style="height: 100%; width: {t['pass_rate']:.0f}%; background: {t['health_color']}; border-radius: 3px;"></div>
</div>
</div>""", unsafe_allow_html=True)

    # --- Daily Funnel Trend Chart ---
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""<div style="font-size: 10px; color: #5A6577; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 12px;">📈 Daily Conversion Funnel Trend</div>""", unsafe_allow_html=True)

    fig2 = go.Figure()

    trend_stages = [
        {"col": "landing_page", "name": "Landing Page", "color": NEON_BLUE},
        {"col": "product_page", "name": "Product Page", "color": NEON_PURPLE},
        {"col": "add_to_cart", "name": "Add to Cart", "color": NEON_ORANGE},
        {"col": "checkout", "name": "Checkout", "color": NEON_YELLOW},
        {"col": "purchase", "name": "Purchase", "color": NEON_GREEN},
    ]

    sorted_df = funnel_df.sort_values("date")

    for stage in trend_stages:
        fig2.add_trace(go.Scatter(
            x=sorted_df["date"],
            y=sorted_df[stage["col"]],
            mode="lines",
            name=stage["name"],
            line=dict(color=stage["color"], width=2),
            fill="tozeroy",
            fillcolor=f"rgba({int(stage['color'][1:3], 16)}, {int(stage['color'][3:5], 16)}, {int(stage['color'][5:7], 16)}, 0.05)",
            hovertemplate=f"<b>{stage['name']}</b><br>Date: %{{x|%b %d}}<br>Count: %{{y:,.0f}}<extra></extra>",
        ))

    fig2.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color=TEXT_SECONDARY, size=11),
        legend=dict(
            orientation="h", yanchor="bottom", y=1.02,
            xanchor="center", x=0.5,
            font=dict(color=TEXT_PRIMARY, size=10),
        ),
        xaxis=dict(gridcolor="#1E2330", showgrid=True, tickformat="%b %d"),
        yaxis=dict(gridcolor="#1E2330", showgrid=True, tickformat=","),
        height=300,
        margin=dict(l=10, r=10, t=40, b=10),
        hovermode="x unified",
    )

    st.plotly_chart(fig2, use_container_width=True)

    # --- CVR Over Time ---
    st.markdown("""<div style="font-size: 10px; color: #5A6577; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 12px;">🎯 True CVR Over Time</div>""", unsafe_allow_html=True)

    fig3 = go.Figure()

    fig3.add_trace(go.Scatter(
        x=sorted_df["date"],
        y=sorted_df["true_cvr"],
        mode="lines+markers",
        name="True CVR",
        line=dict(color=NEON_GREEN, width=2.5),
        marker=dict(size=4, color=NEON_GREEN),
        fill="tozeroy",
        fillcolor="rgba(0, 255, 136, 0.06)",
        hovertemplate="Date: %{x|%b %d}<br>CVR: %{y:.2f}%<extra></extra>",
    ))

    # Benchmark line
    fig3.add_hline(
        y=2.5,
        line_dash="dash",
        line_color=NEON_YELLOW,
        line_width=1.5,
        annotation_text="Target: 2.5%",
        annotation_position="top right",
        annotation_font=dict(color=NEON_YELLOW, size=9),
    )

    fig3.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color=TEXT_SECONDARY, size=11),
        xaxis=dict(gridcolor="#1E2330", showgrid=True, tickformat="%b %d"),
        yaxis=dict(gridcolor="#1E2330", showgrid=True, title="CVR (%)", titlefont=dict(color=TEXT_MUTED, size=10)),
        height=250,
        margin=dict(l=10, r=10, t=10, b=10),
        showlegend=False,
    )

    st.plotly_chart(fig3, use_container_width=True)

def render_matrix_split(device_df, source_df):
    """
    Section 2B: The "Matrix Split" (Device & Source)
    Comparative breakdown of funnel performance by:
    - Tab 1: Device (Mobile vs Desktop vs Tablet)
    - Tab 2: Source (Google Ads vs Meta Ads vs TikTok Ads vs Organic etc.)
    """
    st.markdown('<div style="font-size: 14px; color: #8892A0; text-transform: uppercase; letter-spacing: 2px; padding-bottom: 8px; border-bottom: 1px solid #2D3348; margin-bottom: 16px; margin-top: 24px;">🔀 MATRIX SPLIT — DEVICE & SOURCE BREAKDOWN</div>', unsafe_allow_html=True)

    tab_device, tab_source = st.tabs(["📱 By Device", "🌐 By Source"])

    # ========================
    # TAB 1: DEVICE BREAKDOWN
    # ========================
    with tab_device:
        _render_device_split(device_df)

    # ========================
    # TAB 2: SOURCE BREAKDOWN
    # ========================
    with tab_source:
        _render_source_split(source_df)


def _render_device_split(device_df):
    """Render Device breakdown: summary cards + funnel comparison + table."""

    devices = device_df["device"].unique().tolist()

    # Aggregate per device
    device_agg = []
    for device in devices:
        ddf = device_df[device_df["device"] == device]
        sessions = ddf["sessions"].sum()
        purchases = ddf["purchase"].sum()
        cvr = purchases / max(sessions, 1) * 100
        bounce = ddf["bounce_rate"].mean()
        cart_ab = ddf["cart_abandonment"].mean()

        # Funnel totals
        landing = ddf["landing_page"].sum()
        product = ddf["product_page"].sum()
        cart = ddf["add_to_cart"].sum()
        checkout = ddf["checkout"].sum()

        device_agg.append({
            "device": device,
            "sessions": sessions,
            "landing": landing,
            "product": product,
            "cart": cart,
            "checkout": checkout,
            "purchase": purchases,
            "cvr": cvr,
            "bounce": bounce,
            "cart_abandon": cart_ab,
            "color": DEVICE_COLORS.get(device, "#444"),
        })

    # --- Summary Cards ---
    dev_cols = st.columns(len(device_agg))
    for idx, d in enumerate(device_agg):
        cvr_color = NEON_GREEN if d["cvr"] >= 2.5 else (NEON_YELLOW if d["cvr"] >= 1.5 else NEON_RED)
        bounce_color = NEON_GREEN if d["bounce"] < 40 else (NEON_YELLOW if d["bounce"] < 50 else NEON_RED)
        traffic_share = d["sessions"] / max(sum(x["sessions"] for x in device_agg), 1) * 100

        with dev_cols[idx]:
            st.markdown(f"""<div style="background: linear-gradient(135deg, #1B1F2B 0%, #222838 100%); border: 1px solid #2D3348; border-top: 3px solid {d['color']}; border-radius: 12px; padding: 16px;">
<div style="font-size: 13px; font-weight: 600; color: #FFFFFF; margin-bottom: 4px;">{"📱" if d["device"] == "Mobile" else ("🖥️" if d["device"] == "Desktop" else "📟")} {d['device']}</div>
<div style="font-size: 10px; color: #5A6577; margin-bottom: 12px;">{traffic_share:.0f}% of traffic · {format_number(d['sessions'])} sessions</div>
<div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
<div>
<div style="font-size: 9px; color: #8892A0; text-transform: uppercase;">CVR</div>
<div style="font-size: 20px; font-weight: 700; color: {cvr_color};">{d['cvr']:.2f}%</div>
</div>
<div>
<div style="font-size: 9px; color: #8892A0; text-transform: uppercase;">Bounce</div>
<div style="font-size: 20px; font-weight: 700; color: {bounce_color};">{d['bounce']:.1f}%</div>
</div>
<div>
<div style="font-size: 9px; color: #8892A0; text-transform: uppercase;">Cart Abn.</div>
<div style="font-size: 20px; font-weight: 700; color: {NEON_YELLOW};">{d['cart_abandon']:.1f}%</div>
</div>
</div>
<div style="font-size: 10px; color: #5A6577; border-top: 1px solid #2D3348; padding-top: 8px; margin-top: 4px;">
Orders: <span style="color: #FFFFFF; font-weight: 600;">{format_number(d['purchase'])}</span>
</div>
</div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- Funnel Comparison Chart (Grouped Bar) ---
    col_chart, col_table = st.columns([3, 2])

    with col_chart:
        st.markdown("""<div style="font-size: 10px; color: #5A6577; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 10px;">📊 Funnel Comparison by Device</div>""", unsafe_allow_html=True)

        fig = go.Figure()
        funnel_steps = ["landing", "product", "cart", "checkout", "purchase"]
        step_labels = ["Landing", "Product", "Cart", "Checkout", "Purchase"]

        for d in device_agg:
            # Normalize to percentage of landing page
            landing_val = max(d["landing"], 1)
            vals = [d[s] / landing_val * 100 for s in funnel_steps]

            fig.add_trace(go.Bar(
                name=d["device"],
                x=step_labels,
                y=vals,
                marker=dict(color=d["color"], cornerradius=4),
                text=[f"{v:.1f}%" for v in vals],
                textposition="auto",
                textfont=dict(color=TEXT_PRIMARY, size=10),
            ))

        fig.update_layout(
            barmode="group",
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color=TEXT_SECONDARY, size=11),
            legend=dict(
                orientation="h", yanchor="bottom", y=1.02,
                xanchor="center", x=0.5,
                font=dict(color=TEXT_PRIMARY, size=10),
            ),
            xaxis=dict(gridcolor="rgba(0,0,0,0)", showgrid=False),
            yaxis=dict(gridcolor="#1E2330", showgrid=True, title="% of Landing", titlefont=dict(size=10, color=TEXT_MUTED)),
            height=320,
            margin=dict(l=10, r=10, t=40, b=10),
        )

        st.plotly_chart(fig, use_container_width=True)

    with col_table:
        # --- Comparative Table ---
        st.markdown("""<div style="font-size: 10px; color: #5A6577; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 10px;">📋 Device Performance Matrix</div>""", unsafe_allow_html=True)

        # Table header
        st.markdown(f"""<div style="display: grid; grid-template-columns: 1.2fr repeat({len(device_agg)}, 1fr); gap: 2px; margin-bottom: 2px;">
<div style="background: #222838; padding: 8px 10px; border-radius: 4px 0 0 0; font-size: 9px; color: #5A6577; text-transform: uppercase;">Metric</div>
{"".join(f'<div style="background: #222838; padding: 8px 10px; text-align: center; font-size: 9px; color: {d["color"]}; font-weight: 600; text-transform: uppercase;">{d["device"]}</div>' for d in device_agg)}
</div>""", unsafe_allow_html=True)

        # Table rows
        table_rows = [
            {"label": "Sessions", "key": "sessions", "fmt": "num"},
            {"label": "CVR", "key": "cvr", "fmt": "pct2"},
            {"label": "Bounce Rate", "key": "bounce", "fmt": "pct1"},
            {"label": "Cart Abandon.", "key": "cart_abandon", "fmt": "pct1"},
            {"label": "Landing → Product", "key": None, "calc": lambda d: d["product"] / max(d["landing"], 1) * 100, "fmt": "pct1"},
            {"label": "Product → Cart", "key": None, "calc": lambda d: d["cart"] / max(d["product"], 1) * 100, "fmt": "pct1"},
            {"label": "Cart → Checkout", "key": None, "calc": lambda d: d["checkout"] / max(d["cart"], 1) * 100, "fmt": "pct1"},
            {"label": "Checkout → Purchase", "key": None, "calc": lambda d: d["purchase"] / max(d["checkout"], 1) * 100, "fmt": "pct1"},
            {"label": "Orders", "key": "purchase", "fmt": "num"},
        ]

        for row_idx, row in enumerate(table_rows):
            cells = []
            values = []
            for d in device_agg:
                if row["key"]:
                    val = d[row["key"]]
                else:
                    val = row["calc"](d)
                values.append(val)

            # Find best/worst for coloring
            best_idx = values.index(max(values)) if row["fmt"] != "pct1" or row["label"] in ["Landing → Product", "Product → Cart", "Cart → Checkout", "Checkout → Purchase"] else values.index(min(values))
            # For bounce & cart abandon, lower is better
            if row["label"] in ["Bounce Rate", "Cart Abandon."]:
                best_idx = values.index(min(values))

            for v_idx, val in enumerate(values):
                if row["fmt"] == "num":
                    text = format_number(val)
                elif row["fmt"] == "pct2":
                    text = f"{val:.2f}%"
                else:
                    text = f"{val:.1f}%"

                is_best = v_idx == best_idx
                val_color = NEON_GREEN if is_best else TEXT_PRIMARY

                cells.append(f'<div style="background: #1B1F2B; padding: 8px 10px; text-align: center; font-size: 11px; color: {val_color}; font-weight: {"600" if is_best else "400"};">{text}</div>')

            bg = "#181C27" if row_idx % 2 == 0 else "#1B1F2B"
            st.markdown(f"""<div style="display: grid; grid-template-columns: 1.2fr repeat({len(device_agg)}, 1fr); gap: 2px; margin-bottom: 2px;">
<div style="background: {bg}; padding: 8px 10px; font-size: 10px; color: #8892A0;">{row['label']}</div>
{"".join(cells)}
</div>""", unsafe_allow_html=True)


def _render_source_split(source_df):
    """Render Source breakdown: summary cards + funnel comparison + table."""

    sources = source_df["source"].unique().tolist()

    # Aggregate per source
    source_agg = []
    for source in sources:
        sdf = source_df[source_df["source"] == source]
        sessions = sdf["sessions"].sum()
        purchases = sdf["purchase"].sum()
        cvr = purchases / max(sessions, 1) * 100
        cart_ab = sdf["cart_abandonment"].mean()

        landing = sdf["landing_page"].sum()
        product = sdf["product_page"].sum()
        cart = sdf["add_to_cart"].sum()
        checkout = sdf["checkout"].sum()

        source_agg.append({
            "source": source,
            "sessions": sessions,
            "landing": landing,
            "product": product,
            "cart": cart,
            "checkout": checkout,
            "purchase": purchases,
            "cvr": cvr,
            "cart_abandon": cart_ab,
            "color": SOURCE_COLORS.get(source, "#444"),
        })

    # Sort by sessions descending
    source_agg.sort(key=lambda x: x["sessions"], reverse=True)

    # --- Top 4 Source Summary Cards ---
    top_4 = source_agg[:4]
    src_cols = st.columns(4)

    for idx, s in enumerate(top_4):
        cvr_color = NEON_GREEN if s["cvr"] >= 2.5 else (NEON_YELLOW if s["cvr"] >= 1.5 else NEON_RED)
        traffic_share = s["sessions"] / max(sum(x["sessions"] for x in source_agg), 1) * 100

        with src_cols[idx]:
            st.markdown(f"""<div style="background: linear-gradient(135deg, #1B1F2B 0%, #222838 100%); border: 1px solid #2D3348; border-top: 3px solid {s['color']}; border-radius: 12px; padding: 16px;">
<div style="font-size: 12px; font-weight: 600; color: #FFFFFF; margin-bottom: 4px;">{s['source']}</div>
<div style="font-size: 10px; color: #5A6577; margin-bottom: 12px;">{traffic_share:.0f}% of traffic · {format_number(s['sessions'])} sessions</div>
<div style="display: flex; justify-content: space-between;">
<div>
<div style="font-size: 9px; color: #8892A0; text-transform: uppercase;">CVR</div>
<div style="font-size: 20px; font-weight: 700; color: {cvr_color};">{s['cvr']:.2f}%</div>
</div>
<div>
<div style="font-size: 9px; color: #8892A0; text-transform: uppercase;">Cart Abn.</div>
<div style="font-size: 20px; font-weight: 700; color: {NEON_YELLOW};">{s['cart_abandon']:.1f}%</div>
</div>
<div>
<div style="font-size: 9px; color: #8892A0; text-transform: uppercase;">Orders</div>
<div style="font-size: 20px; font-weight: 700; color: #FFFFFF;">{format_number(s['purchase'])}</div>
</div>
</div>
</div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- CVR Comparison Chart (Horizontal Bar) ---
    col_cvr, col_funnel = st.columns([2, 3])

    with col_cvr:
        st.markdown("""<div style="font-size: 10px; color: #5A6577; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 10px;">🎯 CVR by Source</div>""", unsafe_allow_html=True)

        sorted_agg = sorted(source_agg, key=lambda x: x["cvr"])
        fig_cvr = go.Figure()

        fig_cvr.add_trace(go.Bar(
            x=[s["cvr"] for s in sorted_agg],
            y=[s["source"] for s in sorted_agg],
            orientation="h",
            marker=dict(
                color=[s["color"] for s in sorted_agg],
                cornerradius=4,
            ),
            text=[f"{s['cvr']:.2f}%" for s in sorted_agg],
            textposition="auto",
            textfont=dict(color=TEXT_PRIMARY, size=10),
        ))

        fig_cvr.add_vline(
            x=2.5, line_dash="dash", line_color=NEON_YELLOW, line_width=1.5,
            annotation_text="Target: 2.5%",
            annotation_position="top",
            annotation_font=dict(color=NEON_YELLOW, size=9),
        )

        fig_cvr.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color=TEXT_SECONDARY, size=10),
            xaxis=dict(gridcolor="#1E2330", showgrid=True, zeroline=False),
            yaxis=dict(gridcolor="rgba(0,0,0,0)", showgrid=False),
            height=280,
            margin=dict(l=10, r=20, t=10, b=10),
            showlegend=False,
        )

        st.plotly_chart(fig_cvr, use_container_width=True)

    with col_funnel:
        # --- Funnel by Source (Normalized %) ---
        st.markdown("""<div style="font-size: 10px; color: #5A6577; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 10px;">📊 Funnel Drop-Off by Source</div>""", unsafe_allow_html=True)

        fig_funnel = go.Figure()
        funnel_steps = ["landing", "product", "cart", "checkout", "purchase"]
        step_labels = ["Landing", "Product", "Cart", "Checkout", "Purchase"]

        for s in source_agg[:5]:  # Top 5 sources
            landing_val = max(s["landing"], 1)
            vals = [s[step] / landing_val * 100 for step in funnel_steps]

            fig_funnel.add_trace(go.Scatter(
                x=step_labels,
                y=vals,
                mode="lines+markers",
                name=s["source"],
                line=dict(color=s["color"], width=2),
                marker=dict(size=6, color=s["color"]),
                hovertemplate=f"<b>{s['source']}</b><br>%{{x}}: %{{y:.1f}}%<extra></extra>",
            ))

        fig_funnel.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color=TEXT_SECONDARY, size=10),
            legend=dict(
                orientation="h", yanchor="bottom", y=1.02,
                xanchor="center", x=0.5,
                font=dict(color=TEXT_PRIMARY, size=9),
            ),
            xaxis=dict(gridcolor="#1E2330", showgrid=True),
            yaxis=dict(gridcolor="#1E2330", showgrid=True, title="% of Landing", titlefont=dict(size=10, color=TEXT_MUTED)),
            height=280,
            margin=dict(l=10, r=10, t=40, b=10),
        )

        st.plotly_chart(fig_funnel, use_container_width=True)

    # --- Full Source Performance Table ---
    st.markdown("""<div style="font-size: 10px; color: #5A6577; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 10px;">📋 Full Source Performance Matrix</div>""", unsafe_allow_html=True)

    # Header
    header_cells = ["Source", "Sessions", "CVR", "Cart Abn.", "L→P", "P→C", "C→CO", "CO→Pur", "Orders"]
    header_html = "".join(
        f'<div style="background: #222838; padding: 8px 6px; text-align: {"left" if i == 0 else "center"}; font-size: 9px; color: #5A6577; text-transform: uppercase; font-weight: 600;">{h}</div>'
        for i, h in enumerate(header_cells)
    )
    st.markdown(f"""<div style="display: grid; grid-template-columns: 1.5fr repeat(8, 1fr); gap: 2px; margin-bottom: 2px;">{header_html}</div>""", unsafe_allow_html=True)

    # Find best values for highlighting
    all_cvrs = [s["cvr"] for s in source_agg]
    all_cart_ab = [s["cart_abandon"] for s in source_agg]
    best_cvr = max(all_cvrs)
    best_cart_ab = min(all_cart_ab)

    for row_idx, s in enumerate(source_agg):
        bg = "#181C27" if row_idx % 2 == 0 else "#1B1F2B"

        lp = s["product"] / max(s["landing"], 1) * 100
        pc = s["cart"] / max(s["product"], 1) * 100
        cco = s["checkout"] / max(s["cart"], 1) * 100
        cop = s["purchase"] / max(s["checkout"], 1) * 100

        cvr_color = NEON_GREEN if s["cvr"] == best_cvr else (NEON_GREEN if s["cvr"] >= 2.5 else TEXT_PRIMARY)
        cart_color = NEON_GREEN if s["cart_abandon"] == best_cart_ab else TEXT_PRIMARY

        row_cells = [
            f'<div style="background: {bg}; padding: 8px 6px; font-size: 11px; color: #FFFFFF; display: flex; align-items: center; gap: 6px;"><div style="width: 8px; height: 8px; border-radius: 2px; background: {s["color"]}; flex-shrink: 0;"></div>{s["source"]}</div>',
            f'<div style="background: {bg}; padding: 8px 6px; text-align: center; font-size: 11px; color: {TEXT_PRIMARY};">{format_number(s["sessions"])}</div>',
            f'<div style="background: {bg}; padding: 8px 6px; text-align: center; font-size: 11px; color: {cvr_color}; font-weight: {"600" if s["cvr"] >= 2.5 else "400"};">{s["cvr"]:.2f}%</div>',
            f'<div style="background: {bg}; padding: 8px 6px; text-align: center; font-size: 11px; color: {cart_color};">{s["cart_abandon"]:.1f}%</div>',
            f'<div style="background: {bg}; padding: 8px 6px; text-align: center; font-size: 11px; color: {TEXT_PRIMARY};">{lp:.1f}%</div>',
            f'<div style="background: {bg}; padding: 8px 6px; text-align: center; font-size: 11px; color: {TEXT_PRIMARY};">{pc:.1f}%</div>',
            f'<div style="background: {bg}; padding: 8px 6px; text-align: center; font-size: 11px; color: {TEXT_PRIMARY};">{cco:.1f}%</div>',
            f'<div style="background: {bg}; padding: 8px 6px; text-align: center; font-size: 11px; color: {TEXT_PRIMARY};">{cop:.1f}%</div>',
            f'<div style="background: {bg}; padding: 8px 6px; text-align: center; font-size: 11px; color: #FFFFFF; font-weight: 600;">{format_number(s["purchase"])}</div>',
        ]

        st.markdown(f"""<div style="display: grid; grid-template-columns: 1.5fr repeat(8, 1fr); gap: 2px; margin-bottom: 2px;">{"".join(row_cells)}</div>""", unsafe_allow_html=True)


def render_metric_stack_cro(funnel_df, speed_df):
    """
    Section 3: The Metric Stack (CRO & Experience)
    4 core metrics with gauge, trend line, and context:
    - True CVR: Orders ÷ Human Sessions (>2.5%)
    - Bounce Rate: Single Page Sessions ÷ Total (<40%)
    - Cart Abandonment: (Carts - Purchases) ÷ Carts (<70%)
    - Load Time (LCP): Largest Contentful Paint (<2.5s)
    """
    st.markdown('<div style="font-size: 14px; color: #8892A0; text-transform: uppercase; letter-spacing: 2px; padding-bottom: 8px; border-bottom: 1px solid #2D3348; margin-bottom: 16px; margin-top: 24px;">📐 METRIC STACK — CRO & EXPERIENCE</div>', unsafe_allow_html=True)

    sorted_funnel = funnel_df.sort_values("date")
    sorted_speed = speed_df.sort_values("date")

    # Calculate aggregated metrics
    total_orders = funnel_df["purchase"].sum()
    total_human = funnel_df["human_sessions"].sum()
    total_carts = funnel_df["add_to_cart"].sum()
    avg_cvr = total_orders / max(total_human, 1) * 100
    avg_bounce = funnel_df["bounce_rate"].mean()
    avg_cart_ab = (total_carts - total_orders) / max(total_carts, 1) * 100
    avg_lcp = speed_df["lcp_mobile"].mean()

    # 7-day vs previous 7-day comparison for trend
    if len(sorted_funnel) >= 14:
        recent_7 = sorted_funnel.tail(7)
        prev_7 = sorted_funnel.iloc[-14:-7]

        r_cvr = recent_7["true_cvr"].mean()
        p_cvr = prev_7["true_cvr"].mean()
        cvr_delta = r_cvr - p_cvr

        r_bounce = recent_7["bounce_rate"].mean()
        p_bounce = prev_7["bounce_rate"].mean()
        bounce_delta = r_bounce - p_bounce

        r_cart = recent_7["cart_abandonment"].mean()
        p_cart = prev_7["cart_abandonment"].mean()
        cart_delta = r_cart - p_cart
    else:
        cvr_delta = 0
        bounce_delta = 0
        cart_delta = 0

    if len(sorted_speed) >= 14:
        r_lcp = sorted_speed.tail(7)["lcp_mobile"].mean()
        p_lcp = sorted_speed.iloc[-14:-7]["lcp_mobile"].mean()
        lcp_delta = r_lcp - p_lcp
    else:
        lcp_delta = 0

    metrics = [
        {
            "name": '"True" CVR',
            "value": f"{avg_cvr:.2f}%",
            "calculation": "Orders ÷ Human Sessions",
            "benchmark": "> 2.5%",
            "why": "The real conversion efficiency.",
            "current": avg_cvr,
            "target": 2.5,
            "higher_is_better": True,
            "delta": cvr_delta,
            "delta_fmt": f"{cvr_delta:+.2f}%",
            "trend_data": sorted_funnel["true_cvr"].tolist(),
            "trend_dates": sorted_funnel["date"].tolist(),
            "color": NEON_GREEN if avg_cvr >= 2.5 else NEON_RED,
            "gauge_max": 6.0,
        },
        {
            "name": "Bounce Rate",
            "value": f"{avg_bounce:.1f}%",
            "calculation": "Single Page Sessions ÷ Total",
            "benchmark": "< 40%",
            "why": "Is the Landing Page irrelevant?",
            "current": avg_bounce,
            "target": 40,
            "higher_is_better": False,
            "delta": bounce_delta,
            "delta_fmt": f"{bounce_delta:+.1f}%",
            "trend_data": sorted_funnel["bounce_rate"].tolist(),
            "trend_dates": sorted_funnel["date"].tolist(),
            "color": NEON_GREEN if avg_bounce < 40 else NEON_RED,
            "gauge_max": 80.0,
        },
        {
            "name": "Cart Abandonment",
            "value": f"{avg_cart_ab:.1f}%",
            "calculation": "(Carts - Purchases) ÷ Carts",
            "benchmark": "< 70%",
            "why": "Is the pricing/shipping too high?",
            "current": avg_cart_ab,
            "target": 70,
            "higher_is_better": False,
            "delta": cart_delta,
            "delta_fmt": f"{cart_delta:+.1f}%",
            "trend_data": sorted_funnel["cart_abandonment"].tolist(),
            "trend_dates": sorted_funnel["date"].tolist(),
            "color": NEON_GREEN if avg_cart_ab < 70 else NEON_RED,
            "gauge_max": 100.0,
        },
        {
            "name": "Load Time (LCP)",
            "value": f"{avg_lcp:.1f}s",
            "calculation": "Largest Contentful Paint (s)",
            "benchmark": "< 2.5s",
            "why": "Speed Kills. +1s = -20% CVR.",
            "current": avg_lcp,
            "target": 2.5,
            "higher_is_better": False,
            "delta": lcp_delta,
            "delta_fmt": f"{lcp_delta:+.1f}s",
            "trend_data": sorted_speed["lcp_mobile"].tolist(),
            "trend_dates": sorted_speed["date"].tolist(),
            "color": NEON_GREEN if avg_lcp < 2.5 else (NEON_YELLOW if avg_lcp < 4.0 else NEON_RED),
            "gauge_max": 8.0,
        },
    ]

    # --- 4 Metric Cards in 2x2 Grid ---
    for row_start in range(0, 4, 2):
        cols = st.columns(2)
        for col_idx in range(2):
            m = metrics[row_start + col_idx]
            with cols[col_idx]:
                _render_cro_metric_card(m)

    # --- Summary Table ---
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""<div style="font-size: 10px; color: #5A6577; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 10px;">📋 CRO Metrics Reference Table</div>""", unsafe_allow_html=True)

    # Table header
    st.markdown("""<div style="display: grid; grid-template-columns: 1.2fr 2fr 0.8fr 2fr; gap: 2px; margin-bottom: 2px;">
<div style="background: #222838; padding: 10px 12px; font-size: 9px; color: #5A6577; text-transform: uppercase; font-weight: 600; border-radius: 4px 0 0 0;">Metric</div>
<div style="background: #222838; padding: 10px 12px; font-size: 9px; color: #5A6577; text-transform: uppercase; font-weight: 600;">Calculation</div>
<div style="background: #222838; padding: 10px 12px; text-align: center; font-size: 9px; color: #5A6577; text-transform: uppercase; font-weight: 600;">Benchmark</div>
<div style="background: #222838; padding: 10px 12px; font-size: 9px; color: #5A6577; text-transform: uppercase; font-weight: 600; border-radius: 0 4px 0 0;">Why It Matters</div>
</div>""", unsafe_allow_html=True)

    for idx, m in enumerate(metrics):
        bg = "#181C27" if idx % 2 == 0 else "#1B1F2B"
        st.markdown(f"""<div style="display: grid; grid-template-columns: 1.2fr 2fr 0.8fr 2fr; gap: 2px; margin-bottom: 2px;">
<div style="background: {bg}; padding: 10px 12px; font-size: 11px; color: {m['color']}; font-weight: 600;">{m['name']}</div>
<div style="background: {bg}; padding: 10px 12px; font-size: 11px; color: {TEXT_PRIMARY};">{m['calculation']}</div>
<div style="background: {bg}; padding: 10px 12px; text-align: center; font-size: 11px; color: {NEON_YELLOW}; font-weight: 600;">{m['benchmark']}</div>
<div style="background: {bg}; padding: 10px 12px; font-size: 11px; color: #8892A0; font-style: italic;">{m['why']}</div>
</div>""", unsafe_allow_html=True)


def _render_cro_metric_card(m):
    """Render a single CRO metric card with gauge + trend sparkline."""

    # Determine delta arrow and color
    if m["higher_is_better"]:
        delta_good = m["delta"] > 0
    else:
        delta_good = m["delta"] < 0

    delta_color = NEON_GREEN if delta_good else NEON_RED
    delta_arrow = "▲" if m["delta"] > 0 else ("▼" if m["delta"] < 0 else "—")

    # Health status
    if m["higher_is_better"]:
        on_track = m["current"] >= m["target"]
    else:
        on_track = m["current"] <= m["target"]

    status_text = "ON TARGET" if on_track else "BELOW TARGET"
    status_color = NEON_GREEN if on_track else NEON_RED

    # Gauge fill percentage
    gauge_pct = min(m["current"] / max(m["gauge_max"], 1) * 100, 100)

    # Card Header + Value
    st.markdown(f"""<div style="background: linear-gradient(135deg, #1B1F2B 0%, #222838 100%); border: 1px solid #2D3348; border-radius: 12px 12px 0 0; padding: 16px 20px;">
<div style="display: flex; justify-content: space-between; align-items: flex-start;">
<div>
<div style="font-size: 10px; color: #8892A0; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 6px;">{m['name']}</div>
<div style="font-size: 32px; font-weight: 700; color: {m['color']};">{m['value']}</div>
</div>
<div style="text-align: right;">
<div style="padding: 3px 10px; border-radius: 20px; background: {'rgba(0,255,136,0.12)' if on_track else 'rgba(255,59,92,0.12)'}; font-size: 8px; font-weight: 700; color: {status_color}; text-transform: uppercase; letter-spacing: 0.8px; margin-bottom: 6px;">{status_text}</div>
<div style="font-size: 13px; font-weight: 600; color: {delta_color};">{delta_arrow} {m['delta_fmt']}</div>
<div style="font-size: 8px; color: #5A6577;">vs prev 7 days</div>
</div>
</div>
</div>""", unsafe_allow_html=True)

    # Gauge Bar
    st.markdown(f"""<div style="background: linear-gradient(135deg, #1B1F2B 0%, #222838 100%); border-left: 1px solid #2D3348; border-right: 1px solid #2D3348; padding: 0 20px 12px 20px;">
<div style="display: flex; justify-content: space-between; font-size: 9px; color: #5A6577; margin-bottom: 4px;">
<span>0</span>
<span>Target: {m['benchmark']}</span>
<span>{m['gauge_max']}</span>
</div>
<div style="position: relative; width: 100%; height: 8px; background: #2D3348; border-radius: 8px; overflow: hidden;">
<div style="height: 100%; width: {gauge_pct:.0f}%; background: linear-gradient(90deg, {m['color']}, {m['color']}88); border-radius: 8px;"></div>
</div>
<div style="font-size: 9px; color: #8892A0; margin-top: 6px;">{m['calculation']}</div>
</div>""", unsafe_allow_html=True)

    # Trend Sparkline (using Plotly)
    if m["trend_data"] and len(m["trend_data"]) > 1:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=m["trend_dates"],
            y=m["trend_data"],
            mode="lines",
            line=dict(color=m["color"], width=2),
            fill="tozeroy",
            fillcolor=f"rgba({int(m['color'][1:3], 16)}, {int(m['color'][3:5], 16)}, {int(m['color'][5:7], 16)}, 0.06)",
            hovertemplate="%{x|%b %d}: %{y:.2f}<extra></extra>",
        ))

        # Target line
        fig.add_hline(
            y=m["target"],
            line_dash="dash",
            line_color=NEON_YELLOW,
            line_width=1,
            annotation_text=f"Target: {m['benchmark']}",
            annotation_position="top right",
            annotation_font=dict(color=NEON_YELLOW, size=8),
        )

        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color=TEXT_MUTED, size=9),
            xaxis=dict(gridcolor="#1E2330", showgrid=False, tickformat="%b %d", showticklabels=True),
            yaxis=dict(gridcolor="#1E2330", showgrid=True, showticklabels=True),
            height=140,
            margin=dict(l=5, r=5, t=5, b=5),
            showlegend=False,
        )

        st.plotly_chart(fig, use_container_width=True, key=f"trend_{m['name']}")

    # Card footer — why it matters
    st.markdown(f"""<div style="background: linear-gradient(135deg, #1B1F2B 0%, #222838 100%); border: 1px solid #2D3348; border-top: none; border-radius: 0 0 12px 12px; padding: 10px 20px;">
<div style="font-size: 10px; color: #8892A0; font-style: italic;">💡 {m['why']}</div>
</div>""", unsafe_allow_html=True)

    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)


def render_ai_brain_cro(funnel_df, speed_df, device_df):
    """
    Section 4: The AI Brain Logic (The CRO Expert)
    Placeholder — ready for OpenAI API integration.

    Logic A (Tech Check): Mobile CVR vs Load Time correlation
    Logic B (Offer Mismatch): Ad CTR vs Bounce Rate gap
    Logic C (Friction Monitor): Checkout abandonment detection
    """
    st.markdown('<div style="font-size: 14px; color: #8892A0; text-transform: uppercase; letter-spacing: 2px; padding-bottom: 8px; border-bottom: 1px solid #2D3348; margin-bottom: 16px; margin-top: 24px;">🧠 AI BRAIN — THE CRO EXPERT</div>', unsafe_allow_html=True)

    insights = _generate_cro_insights(funnel_df, speed_df, device_df)

    # Status Bar
    st.markdown(f"""<div style="display: flex; align-items: center; justify-content: space-between; padding: 10px 16px; background: linear-gradient(135deg, #1B1F2B 0%, #222838 100%); border: 1px solid #2D3348; border-radius: 8px; margin-bottom: 16px;">
<div style="display: flex; align-items: center; gap: 8px;">
<div style="width: 8px; height: 8px; border-radius: 50%; background: {NEON_GREEN};"></div>
<span style="font-size: 11px; color: #8892A0; text-transform: uppercase; letter-spacing: 1px;">AI Engine Status: Active</span>
</div>
<div style="font-size: 10px; color: #5A6577;">Last Analysis: Just now · Powered by OpenAI</div>
</div>""", unsafe_allow_html=True)

    for insight in insights:
        _render_cro_insight_card(insight)

    # Generate Button (Placeholder)
    st.markdown("<br>", unsafe_allow_html=True)
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    with col_btn2:
        if st.button("🧠 Generate Fresh CRO Insights", key="ai_cro_insights", use_container_width=True, type="primary"):
            st.info("🔌 OpenAI API integration pending. Insights above are placeholder data based on current metrics.")


def _generate_cro_insights(funnel_df, speed_df, device_df):
    """
    Generate placeholder CRO insights matching the brief's tone.
    Short, punchy, actionable — like a real CRO expert.
    """
    insights = []
    sorted_funnel = funnel_df.sort_values("date")
    sorted_speed = speed_df.sort_values("date")

    # --- Logic A: Tech Check ---
    # Compare recent mobile CVR vs LCP spike
    if len(sorted_funnel) >= 7 and len(sorted_speed) >= 7:
        recent_lcp = sorted_speed.tail(3)["lcp_mobile"].mean()
        prev_lcp = sorted_speed.iloc[-7:-3]["lcp_mobile"].mean()
        lcp_change = ((recent_lcp - prev_lcp) / max(prev_lcp, 1)) * 100

        # Mobile CVR from device data
        mobile_df = device_df[device_df["device"] == "Mobile"]
        if len(mobile_df) >= 7:
            mobile_sorted = mobile_df.sort_values("date")
            recent_mobile_cvr = mobile_sorted.tail(3)["cvr"].mean()
            prev_mobile_cvr = mobile_sorted.iloc[-7:-3]["cvr"].mean()
            cvr_change = ((recent_mobile_cvr - prev_mobile_cvr) / max(prev_mobile_cvr, 1)) * 100
        else:
            recent_mobile_cvr = mobile_df["cvr"].mean() if len(mobile_df) > 0 else 0
            cvr_change = 0

        severity = "critical" if recent_lcp > 4.0 else ("warning" if recent_lcp > 2.5 else "info")

        insights.append({
            "logic_id": "A",
            "logic_name": "Tech Check",
            "icon": "⚡",
            "severity": severity,
            "title": f"Mobile CVR dropped {abs(cvr_change):.0f}% overnight. Load time spiked to {recent_lcp:.1f}s.",
            "body": f"Mobile LCP increased from {prev_lcp:.1f}s to {recent_lcp:.1f}s ({lcp_change:+.0f}%) "
                    f"in the last 3 days. Mobile CVR is now {recent_mobile_cvr:.2f}%. "
                    f"Every +1 second of load time costs you approximately 20% in conversions.",
            "recommendation": "Check recent Shopify app installs or theme updates. "
                             "Audit third-party scripts in theme.liquid. "
                             "Run Google PageSpeed Insights and fix Critical issues first.",
            "accent_color": NEON_RED if severity == "critical" else NEON_YELLOW,
        })

    # --- Logic B: Offer Mismatch ---
    # High sessions but high bounce = landing page not matching ad promise
    avg_bounce = funnel_df["bounce_rate"].mean()
    avg_cvr = funnel_df["true_cvr"].mean()

    if avg_bounce > 38:
        severity = "critical" if avg_bounce > 50 else "warning"
        insights.append({
            "logic_id": "B",
            "logic_name": "Offer Mismatch",
            "icon": "🎯",
            "severity": severity,
            "title": f"High Bounce Rate ({avg_bounce:.0f}%) detected. Landing Page may not deliver on Ad promise.",
            "body": f"Bounce Rate is {avg_bounce:.1f}% with a CVR of only {avg_cvr:.2f}%. "
                    f"This pattern suggests visitors are arriving with expectations set by your ads, "
                    f"but the Landing Page content doesn't match what was promised.",
            "recommendation": "Match Landing Page headline to Ad copy exactly. "
                             "Ensure the product shown in ads is above-the-fold on the landing page. "
                             "A/B test a dedicated landing page vs. sending traffic to the homepage.",
            "accent_color": NEON_ORANGE,
        })
    else:
        insights.append({
            "logic_id": "B",
            "logic_name": "Offer Mismatch",
            "icon": "🎯",
            "severity": "success",
            "title": f"Landing Page alignment is healthy. Bounce Rate at {avg_bounce:.0f}%.",
            "body": f"Bounce Rate ({avg_bounce:.1f}%) is within the healthy range (<40%). "
                    f"Your ads and landing pages are well-aligned — visitors are staying and browsing.",
            "recommendation": "Maintain current ad-to-landing-page consistency. "
                             "Consider testing more aggressive offers to push CVR higher.",
            "accent_color": NEON_GREEN,
        })

    # --- Logic C: Friction Monitor ---
    # Checkout abandonment analysis
    total_carts = funnel_df["add_to_cart"].sum()
    total_purchases = funnel_df["purchase"].sum()
    checkout_abandon = (total_carts - total_purchases) / max(total_carts, 1) * 100

    # Check for recent spike
    if len(sorted_funnel) >= 7:
        recent_cart_ab = sorted_funnel.tail(3)["cart_abandonment"].mean()
        prev_cart_ab = sorted_funnel.iloc[-7:-3]["cart_abandonment"].mean()
        cart_ab_change = recent_cart_ab - prev_cart_ab
    else:
        recent_cart_ab = checkout_abandon
        cart_ab_change = 0

    if checkout_abandon > 65:
        severity = "critical" if checkout_abandon > 75 else "warning"
        insights.append({
            "logic_id": "C",
            "logic_name": "Friction Monitor",
            "icon": "🚧",
            "severity": severity,
            "title": f"Checkout Abandonment is abnormally high ({checkout_abandon:.0f}%). Check shipping settings or payment gateway.",
            "body": f"Cart-to-Purchase abandonment is {checkout_abandon:.1f}% (target: <70%). "
                    f"Recent trend shows {cart_ab_change:+.1f}% change vs previous period. "
                    f"This is costing you approximately {format_number(total_carts - total_purchases)} lost orders.",
            "recommendation": "Check if shipping costs are visible before checkout (surprise costs = #1 abandonment reason). "
                             "Verify payment gateway is processing correctly. "
                             "Consider adding express checkout (Shop Pay, Apple Pay) to reduce friction.",
            "accent_color": NEON_RED if severity == "critical" else NEON_ORANGE,
        })
    else:
        insights.append({
            "logic_id": "C",
            "logic_name": "Friction Monitor",
            "icon": "🚧",
            "severity": "success",
            "title": f"Checkout friction is within healthy range ({checkout_abandon:.0f}%).",
            "body": f"Cart-to-Purchase abandonment at {checkout_abandon:.1f}% is below the 70% threshold. "
                    f"Your checkout flow is performing well relative to e-commerce benchmarks.",
            "recommendation": "Maintain current checkout UX. Consider testing one-page checkout vs. multi-step. "
                             "Add trust badges and money-back guarantee near the payment button.",
            "accent_color": NEON_GREEN,
        })

    return insights


def _render_cro_insight_card(insight):
    """Render a single CRO AI insight card. Same pattern as Module 2."""

    severity_config = {
        "critical": {"bg": "rgba(255, 59, 92, 0.08)", "border": "rgba(255, 59, 92, 0.35)", "label_bg": "rgba(255, 59, 92, 0.2)", "label_color": NEON_RED, "label": "CRITICAL"},
        "warning": {"bg": "rgba(255, 215, 0, 0.06)", "border": "rgba(255, 215, 0, 0.3)", "label_bg": "rgba(255, 215, 0, 0.15)", "label_color": NEON_YELLOW, "label": "WARNING"},
        "success": {"bg": "rgba(0, 255, 136, 0.06)", "border": "rgba(0, 255, 136, 0.25)", "label_bg": "rgba(0, 255, 136, 0.15)", "label_color": NEON_GREEN, "label": "POSITIVE"},
        "info": {"bg": "rgba(0, 212, 255, 0.06)", "border": "rgba(0, 212, 255, 0.25)", "label_bg": "rgba(0, 212, 255, 0.15)", "label_color": NEON_BLUE, "label": "INFO"},
    }

    sev = severity_config.get(insight["severity"], severity_config["info"])
    accent = insight["accent_color"]

    # Card Header
    st.markdown(f"""<div style="background: {sev['bg']}; border: 1px solid {sev['border']}; border-radius: 12px 12px 0 0; padding: 14px 20px;">
<div style="display: flex; align-items: center; justify-content: space-between;">
<div style="display: flex; align-items: center; gap: 10px;">
<span style="font-size: 22px;">{insight['icon']}</span>
<div>
<div style="font-size: 13px; font-weight: 600; color: #FFFFFF;">{insight['title']}</div>
<div style="font-size: 10px; color: #5A6577; margin-top: 2px;">Logic {insight['logic_id']}: {insight['logic_name']}</div>
</div>
</div>
<div style="padding: 3px 10px; border-radius: 20px; background: {sev['label_bg']}; font-size: 9px; font-weight: 700; color: {sev['label_color']}; text-transform: uppercase; letter-spacing: 1px;">{sev['label']}</div>
</div>
</div>""", unsafe_allow_html=True)

    # Card Body
    st.markdown(f"""<div style="background: {sev['bg']}; border-left: 1px solid {sev['border']}; border-right: 1px solid {sev['border']}; padding: 0 20px 12px 20px;">
<div style="font-size: 12px; color: #C0C7D0; line-height: 1.7; padding: 10px 14px; background: rgba(0,0,0,0.15); border-radius: 8px;">
<span style="font-size: 9px; color: #5A6577; text-transform: uppercase; letter-spacing: 1px; display: block; margin-bottom: 6px;">📊 Analysis</span>
{insight['body']}
</div>
</div>""", unsafe_allow_html=True)

    # Card Footer
    st.markdown(f"""<div style="background: {sev['bg']}; border: 1px solid {sev['border']}; border-top: none; border-radius: 0 0 12px 12px; padding: 0 20px 14px 20px;">
<div style="font-size: 12px; color: #C0C7D0; line-height: 1.7; padding: 10px 14px; background: rgba(0,0,0,0.1); border-radius: 8px; border-left: 3px solid {accent};">
<span style="font-size: 9px; color: {accent}; text-transform: uppercase; letter-spacing: 1px; display: block; margin-bottom: 6px;">💡 Recommendation</span>
{insight['recommendation']}
</div>
</div>""", unsafe_allow_html=True)

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)


def show_cro_terminal():
    """
    Main entry point for Module 3: CRO Terminal.
    Called from app.py navigation.
    """
    load_module3_css()

    # --- Module Header ---
    st.markdown("""
    <div style="margin-bottom: 24px;">
        <div style="font-size: 32px; font-weight: 700; color: #FFFFFF; margin-bottom: 4px;">
            🎯 Data Steering</div>
        <div style="font-size: 14px; color: #8892A0; margin-bottom: 24px;">
            The CRO Terminal — Identify & Fix Leaky Buckets in the Customer Journey</div>
    </div>
    """, unsafe_allow_html=True)

    # --- Date Range & Filter ---
    col_f1, col_f2, col_f3 = st.columns([2, 2, 6])
    with col_f1:
        date_range = st.selectbox(
            "📅 Time Range",
            ["Last 7 Days", "Last 14 Days", "Last 30 Days"],
            index=2,
            key="cro_date_range"
        )
    with col_f2:
        traffic_view = st.selectbox(
            "👁️ Traffic View",
            ["True Human Traffic", "All Traffic (inc. Bots)"],
            index=0,
            key="cro_traffic_view"
        )

    # --- Generate Data ---
    days_map = {"Last 7 Days": 7, "Last 14 Days": 14, "Last 30 Days": 30}
    days = days_map.get(date_range, 30)

    traffic_df = generate_traffic_data(days=30)
    funnel_df = generate_funnel_data(days=30)
    device_df = generate_funnel_by_device(days=30)
    source_df = generate_funnel_by_source(days=30)
    speed_df = generate_page_speed_data(days=30)

    # Filter by date range
    cutoff_date = datetime.now() - timedelta(days=days)
    traffic_df = traffic_df[traffic_df["date"] >= cutoff_date]
    funnel_df = funnel_df[funnel_df["date"] >= cutoff_date]
    device_df = device_df[device_df["date"] >= cutoff_date]
    source_df = source_df[source_df["date"] >= cutoff_date]
    speed_df = speed_df[speed_df["date"] >= cutoff_date]

    # --- Data Summary for verification ---
    st.markdown('<div style="height: 1px; background: linear-gradient(to right, transparent, #2D3348, transparent); margin: 24px 0;"></div>', unsafe_allow_html=True)

    # Quick data verification
    total_raw = traffic_df["total_sessions"].sum()
    total_bots = traffic_df["bot_sessions"].sum()
    total_human = traffic_df["human_sessions"].sum()
    total_purchases = funnel_df["purchase"].sum()
    total_revenue = funnel_df["revenue"].sum()
    avg_cvr = funnel_df["true_cvr"].mean()
    avg_bounce = funnel_df["bounce_rate"].mean()
    avg_cart_abandon = funnel_df["cart_abandonment"].mean()
    avg_lcp_mobile = speed_df["lcp_mobile"].mean()
    avg_lcp_desktop = speed_df["lcp_desktop"].mean()

    # Show "The Bouncer" — Bot Filter Stats
    is_filtered = traffic_view == "True Human Traffic"

    # KPI Row
    kpi_cols = st.columns(5)
    kpi_items = [
        {
            "label": "True Sessions" if is_filtered else "Raw Sessions",
            "value": f"{total_human:,.0f}" if is_filtered else f"{total_raw:,.0f}",
            "sub": f"🤖 {total_bots:,.0f} bots filtered ({total_bots/max(total_raw,1)*100:.0f}%)" if is_filtered else f"⚠️ Includes {total_bots:,.0f} bot sessions",
            "color": NEON_BLUE,
        },
        {
            "label": "True CVR",
            "value": f"{avg_cvr:.2f}%",
            "sub": f"Benchmark: >2.5%",
            "color": NEON_GREEN if avg_cvr >= 2.5 else NEON_RED,
        },
        {
            "label": "Bounce Rate",
            "value": f"{avg_bounce:.1f}%",
            "sub": f"Benchmark: <40%",
            "color": NEON_GREEN if avg_bounce < 40 else NEON_RED,
        },
        {
            "label": "Cart Abandonment",
            "value": f"{avg_cart_abandon:.1f}%",
            "sub": f"Benchmark: <70%",
            "color": NEON_GREEN if avg_cart_abandon < 70 else NEON_RED,
        },
        {
            "label": "Avg LCP (Mobile)",
            "value": f"{avg_lcp_mobile:.1f}s",
            "sub": f"Benchmark: <2.5s",
            "color": NEON_GREEN if avg_lcp_mobile < 2.5 else (NEON_YELLOW if avg_lcp_mobile < 4.0 else NEON_RED),
        },
    ]

    for idx, kpi in enumerate(kpi_items):
        with kpi_cols[idx]:
            st.markdown(f"""<div style="background: linear-gradient(135deg, #1B1F2B 0%, #222838 100%); border: 1px solid #2D3348; border-top: 3px solid {kpi['color']}; border-radius: 12px; padding: 16px; text-align: center;">
<div style="font-size: 10px; color: #8892A0; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 6px;">{kpi['label']}</div>
<div style="font-size: 26px; font-weight: 700; color: {kpi['color']}; margin-bottom: 4px;">{kpi['value']}</div>
<div style="font-size: 10px; color: #5A6577;">{kpi['sub']}</div>
</div>""", unsafe_allow_html=True)

    # --- Section 1: Bot Filter Stats (The Bouncer) ---
    st.markdown('<div style="height: 1px; background: linear-gradient(to right, transparent, #2D3348, transparent); margin: 24px 0;"></div>', unsafe_allow_html=True)
    render_bot_filter_stats(traffic_df, is_filtered)

    # --- Section 2: Red Alert Funnel ---
    st.markdown('<div style="height: 1px; background: linear-gradient(to right, transparent, #2D3348, transparent); margin: 24px 0;"></div>', unsafe_allow_html=True)
    render_red_alert_funnel(funnel_df)

    # --- Section 3: Matrix Split (Device & Source) ---
    st.markdown('<div style="height: 1px; background: linear-gradient(to right, transparent, #2D3348, transparent); margin: 24px 0;"></div>', unsafe_allow_html=True)
    render_matrix_split(device_df, source_df)

    # --- Section 4: Metric Stack (CRO & Experience) ---
    st.markdown('<div style="height: 1px; background: linear-gradient(to right, transparent, #2D3348, transparent); margin: 24px 0;"></div>', unsafe_allow_html=True)
    render_metric_stack_cro(funnel_df, speed_df)

    # --- Section 5: AI Brain (CRO Expert) ---
    st.markdown('<div style="height: 1px; background: linear-gradient(to right, transparent, #2D3348, transparent); margin: 24px 0;"></div>', unsafe_allow_html=True)
    render_ai_brain_cro(funnel_df, speed_df, device_df)


# ============================================================
# 4. STANDALONE TEST MODE
# ============================================================

if __name__ == "__main__":
    st.set_page_config(
        page_title="Marktivo Growth OS — CRO Terminal",
        page_icon="🎯",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    show_cro_terminal()
