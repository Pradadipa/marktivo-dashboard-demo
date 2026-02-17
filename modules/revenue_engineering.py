"""
Module 1: Revenue Engineering - The Financial Terminal
Funnel Breakdown + North Star Ribbon + Data Integrity Layer
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go 
import plotly.express as px
from datetime import timedelta

from config.settings import COLORS, FUNNEL_STAGES, TARGETS
from utils.data_loader import DataLoader

def show_revenue_engineering():
    """Main function - Module 1"""

    st.title("💰 REVENUE ENGINEERING")
    st.markdown("### The Financial Terminal")
    st.markdown("---")

    # Load Data
    loader = DataLoader()
    df = loader.load_revenue_data()

    if df.empty:
        st.error("❌ No data.")
        return
    
    # Data filter
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input(
            "📅 Start Date",
            value=df['date'].max() - timedelta(days=30)
        )
    with col2:
        end_date = st.date_input(
            "📅 End Date",
            value=df['date'].max()
        )
    
    # Filter by date
    mask = (df['date'] >= pd.Timestamp(start_date)) & (df['date'] <= pd.Timestamp(end_date))
    filtered_df = df[mask].copy()

    # ========================================
    # SECTION 1: DATA INTEGRITY - THE ENFORCER
    # ========================================
    show_data_integrity(filtered_df)

    # ========================================
    # SECTION 2: NORTH STAR RIBBON
    # ========================================
    show_north_star(filtered_df)

    # ========================================
    # SECTION 3: MAIN TERMINAL - FUNNEL BREAKDOWN
    # ========================================
    show_main_terminal(filtered_df)

    # ========================================
    # SECTION 4: WELTH ENGINE - COHORT LTV
    # =======================================
    show_welth_engine(filtered_df)

    # ========================================
    # SECTION 5 : CONTEXT GRAPH - MER TIMELINE
    # =======================================
    show_context_graph(filtered_df)

    # ========================================
    # SECTION 6 : AI BRAIN LOGIC
    # =======================================
    show_ai_insights(filtered_df)

def show_data_integrity(df):
    """The Enforcer - Data Integrity Layer"""

    uncategorized = df[df['funnel_stage'] == 'UNCATEGORIZED']

    if not uncategorized.empty:
        # Red Alert box
        st.markdown(
            f"""
            <div style="
                background-color: rgba(255, 0, 85, 0.15);
                border: 2px solid #FF0055;
                border-radius: 10px;
                padding: 15px 20px;
                margin-bottom: 20px;
            ">
                <h4 style="color: #FF0055; margin: 0;">
                    ⚠️ UNCATEGORIZED SPEND — DATA INTEGRITY ALERT
                </h4>
                <p style="color: #FF0055; margin: 5px 0 0 0;">
                    {len(uncategorized)} campaigns missing funnel tags (|TOF|, |MOF|, |BOF|, |RET|).
                    Categorize these campaigns to validate data.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
        # Show uncategorized date
        with st.expander("📋 View Uncategorized Campaigns"):
            st.dataframe(
                uncategorized[['date', 'spend', 'revenue', 'impressions', 'clicks']],
                use_container_width=True
        )
    
    else:
        st.success("✅ **Data Integrity:** All campaigns are properly categorized.")

    st.markdown("---")

def show_north_star(df):
    """North Star Ribbon -  Top KPIs"""

    # Filter only valid stages
    valid_df = df[df['funnel_stage'] != 'UNCATEGORIZED']

    # Calculate metrics
    total_revenue = valid_df['revenue'].sum()
    total_spend = valid_df['spend'].sum()
    total_orders = valid_df['orders'].sum()
    mer = total_revenue / total_spend if total_spend > 0 else 0
    contribution = total_revenue - total_spend
    cpa = total_spend / total_orders if total_orders > 0 else 0
    ltv_cac = 3.2  # Simplified for demo

    # Platform Trust Index
    pixel_revenue = total_revenue * 1.2  # Pixel over-reports by ~20%
    trust_index = (total_revenue / pixel_revenue) * 100

    st.markdown("#### 📊 **NORTH STAR RIBBON**")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("MER (7-Day Rolling)", f"{mer:.2f}x",
            delta=f"+{mer - TARGETS['MER']:.2f}" if mer > TARGETS['MER'] else f"{mer - TARGETS['MER']:.2f}",
            help="Revenue ÷ Spend. Target: 3.0x")
    
    with col2:
        st.metric("Contribution Margin ($)", f"${contribution:,.0f}",
            delta="+12%",
            help="Total Revenue - Total Ad Spend")
    
    with col3:
        st.metric("Projected LTV:CAC", f"{ltv_cac:.1f}",
            delta="+0.4",
            help="60-Day LTV ÷ CPA. Target > 3.0")
    
    # Second row
    col4, col5, col6 = st.columns(3)

    with col4:
        st.metric("Real Revenue", f"${total_revenue:,.0f}",
            help="Backend confirmed orders (Source of Truth)")

    with col5:
        st.metric("Platform Trust Index", f"{trust_index:.0f}%",
            delta="-20%",
            help="Backend Sales vs Pixel Sales. 100% = perfect match")

    with col6:
        st.metric("Total CPA", f"${cpa:.2f}",
            help="Total Spend ÷ Total Orders")

    st.markdown("---")

def show_main_terminal(df):
    """Main Terminal - Funnel Breakdown Table"""

    st.markdown("#### 🎯 **MAIN TERMINAL — FUNNEL BREAKDOWN**")

    # Filter valid stages only
    valid_df = df[df['funnel_stage'] != 'UNCATEGORIZED']

    # Aggregate by funnel stage
    funnel_summary = valid_df.groupby('funnel_stage').agg({
        'spend': 'sum',
        'impressions': 'sum',
        'clicks': 'sum',
        'orders': 'sum',
        'revenue': 'sum',
        'contribution': 'sum'
    }).reset_index()

    # Calculate derived metrics
    funnel_summary['ctr'] = (funnel_summary['clicks'] / funnel_summary['impressions'] * 100).round(2)
    funnel_summary['cpm'] = (funnel_summary['spend'] / funnel_summary['impressions'] * 1000).round(2)
    funnel_summary['cpc'] = (funnel_summary['spend'] / funnel_summary['clicks']).round(2)
    funnel_summary['cpa'] = (funnel_summary['spend'] / funnel_summary['orders']).round(2)
    funnel_summary['roas'] = (funnel_summary['revenue'] / funnel_summary['spend']).round(2)
    funnel_summary['aov'] = (funnel_summary['revenue'] / funnel_summary['orders']).round(2)
    funnel_summary['conv_rate'] = (funnel_summary['orders'] / funnel_summary['clicks'] * 100).round(2)

    # Define display order
    stage_order = ['TOF', 'MOF', 'BOF', 'RET']
    stage_icons = {
        'TOF': '🔵 TOF - Top of Funnel',
        'MOF': '🟣 MOF - Mid of Funnel',
        'BOF': '🟠 BOF - Bottom of Funnel',
        'RET': '🟢 RET - Retention'
    }

    funnel_summary['funnel_stage'] = funnel_summary['funnel_stage'].map(stage_icons)
    funnel_summary = funnel_summary.set_index('funnel_stage').reindex(
        [stage_icons[s] for s in stage_order]
    ).reset_index()

    # Format display columns
    display_df = funnel_summary[
        ['funnel_stage', 'spend', 'contribution', 'impressions',
        'cpm', 'ctr', 'cpc', 'cpa', 'roas', 'aov', 'conv_rate']
    ].copy()

    display_df.columns = [
        'Funnel Stage',
        'Spend ($)', 'Contribution ($)', 'Impressions',
        'CPM ($)', 'CTR (%)', 'CPC ($)', 'CPA ($)',
        'ROAS', 'AOV ($)', 'Conv Rate (%)'
    ]

    # Format numbers
    display_df['Spend ($)'] = display_df['Spend ($)'].apply(lambda x: f"${x:,.0f}")
    display_df['Contribution ($)'] = display_df['Contribution ($)'].apply(lambda x: f"${x:,.0f}")
    display_df['Impressions'] = display_df['Impressions'].apply(lambda x: f"{x:,}")
    display_df['CPM ($)'] = display_df['CPM ($)'].apply(lambda x: f"${x:,.2f}")
    display_df['CPC ($)'] = display_df['CPC ($)'].apply(lambda x: f"${x:,.2f}")
    display_df['CPA ($)'] = display_df['CPA ($)'].apply(lambda x: f"${x:,.2f}")
    display_df['AOV ($)'] = display_df['AOV ($)'].apply(lambda x: f"${x:,.2f}")
    display_df['Conv Rate (%)'] = display_df['Conv Rate (%)'].apply(lambda x: f"{x:.2f}%")
    st.dataframe(display_df, use_container_width=True, hide_index=True)

    st.markdown("---")

    # ========================================
    # SPEND vs ROAS COMPARISON CHART
    # ========================================

    st.markdown("#### 📈 **SPEND vs ROAS — BY FUNNEL STAGE**")

    # Re-aggregate for chart (without icon labels)
    chart_df = valid_df.groupby('funnel_stage').agg({
        'spend': 'sum',
        'revenue': 'sum'
    }).reset_index()

    chart_df['roas'] = (chart_df['revenue'] / chart_df['spend']).round(2)

    # Map names
    chart_df['funnel_stage'] = chart_df['funnel_stage'].map({
        'TOF': 'TOF',
        'MOF': 'MOF',
        'BOF': 'BOF',
        'RET': 'RET'
    })

    stage_colors = ['#00D9FF', '#B026FF', '#FFB800', '#00FF88']

    fig = go.Figure()

    # Bar: Spend
    fig.add_trace(go.Bar(
        x=chart_df['funnel_stage'],
        y=chart_df['spend'],
        name='Spend ($)',
        marker_color=stage_colors,
        marker_line_color='#0E1117',
        marker_line_width=2
    ))

    # Line: ROAS
    fig.add_trace(go.Scatter(
        x=chart_df['funnel_stage'],
        y=chart_df['roas'],
        name='ROAS',
        mode='lines+markers',
        line=dict(color='#FFFFFF', width=3),
        marker=dict(size=12, color='#FFFFFF',
                    line=dict(color='#00D9FF', width=2))
    ))

    fig.update_layout(
        paper_bgcolor='#0E1117',
        plot_bgcolor='#1E1E1E',
        font=dict(color='#FAFAFA', family='monospace'),
        title_text="Spend Distribution & ROAS by Funnel Stage",
        title_font_color='#00D9FF',
        xaxis_title="Funnel Stage",
        yaxis_title="Spend ($)",
        yaxis2=dict(
            title='ROAS',
            overlaying='y',
            side='right',
            showgrid=False,
            titlefont=dict(color='#FFFFFF')
        ),
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=-0.3,
            xanchor='center',
            x=0.5
        ),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='#2D2D2D'),
        height=400
    )

    st.plotly_chart(fig, use_container_width=True)

def show_welth_engine(df):
    """Cohort LTV Analysis - The Triangel of Truth"""

    st.markdown("---")
    st.markdown("#### 💎 **WEALTH ENGINE — COHORT LTV ANALYSIS**")

    # Load cohort data
    loader = DataLoader()
    cohort_df = loader.load_cohort_data()

    if cohort_df.empty:
        st.warning("⚠️ Cohort data not available")
        return
    
    # Toogle view
    view_mode = st.radio(
        "**View Mode:**",
        ["💰 LTV Progression", "📊 Retention Metrics"],
        horizontal=True
    )

    if view_mode == "💰 LTV Progression":
        show_ltv_heatmap(cohort_df)
    else:
        show_retention_metrics(cohort_df)

def show_ltv_heatmap(cohort_df):
    """Ther Triangel of Truth - LTV Heatmap"""

    # Pivot for heatmap
    pivot_df = cohort_df.pivot_table(
        index='cohort',
        columns='day',
        values='ltv',
        aggfunc='mean'
    )

    fig = go.Figure(data=go.Heatmap(
        z=pivot_df.values,
        x=['Day 0', 'Day 30', 'Day 60', 'Day 90'],
        y=pivot_df.index,
        colorscale=[
            [0.5, "#FF0055"],
            [0.5, "#FFB800"],
            [1.0, "#00FF88"]
        ],
        text=pivot_df.values.round(2),
        texttemplate='$%{text}',
        textfont={"size":11, "color": "#0E1117"},
        colorbar=dict(
            title="LTV ($)",
            titleside="right",
            tickmode="linear",
            tick0=0,
            dtick=50,
            titlefont=dict(color='#FAFAFA'),
            tickfont=dict(color='#FAFAFA')
        ),
        hovertemplate='<b>%{y}</b><br>%{x}<br>LTV: $%{z:.2f}<extra></extra>'
    ))

    fig.update_layout(
        title="Cohort LTV Progression (The Triangel of Truth)",
        title_font_color='#00D9FF',
        xaxis_title="Days Since Acquisition",
        yaxis_title="Acquisition Cohort",
        paper_bgcolor='#0E1117',
        plot_bgcolor='#1E1E1E',
        font=dict(color='#FAFAFA', family='monospace'),
        height=500,
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False, autorange='reversed')
    )

    st.plotly_chart(fig, use_container_width=True)

    # Insight
    st.markdown("**💡 Heatmap Insights:**")

    col1, col2 = st.columns(2)

    with col1:
        # Best performing cohort
        day_60_ltv = cohort_df[cohort_df['day'] == 60].groupby('cohort')['ltv'].mean()
        best_cohort = day_60_ltv.idxmax()
        best_ltv = day_60_ltv.max()

        st.success(f"🏆 **Best Cohort:** {best_cohort} (Day 60 LTV: ${best_ltv:.2f})")
    with col2:
        # Average LTV
        avg_growth = cohort_df.groupby('day')['ltv'].mean()
        growth_rate = ((avg_growth[90] - avg_growth[0]) / avg_growth[0]) * 100

        st.info(f"📈 **Avg LTV Growth:** {growth_rate:.2f}% from Day 0 to Day 90")

def show_retention_metrics(cohort_df):
    """Retention Economics Metrics"""

    # Calculate metrics
    latest_cohort = cohort_df[cohort_df['cohort'] == cohort_df['cohort'].max()]

    day_60_ltv = latest_cohort[latest_cohort['day'] == 60]['ltv'].values[0]
    avg_cpa = 35 # Simplified

    cash_multiplier = day_60_ltv/ avg_cpa
    payback_period = 30
    second_order_rate = latest_cohort[latest_cohort['day'] == 30]['second_order_rate'].values[0] * 100

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "💰 Cash Multiplier (Day 60)",
            f"{cash_multiplier:.2f}x",
            help="LTV (Day 60) ÷ CPA. Shows scale potential."
        )
    
    with col2:
        st.metric(
            "⏱️ Payback Period",
            f"{payback_period} days",
            help="Days to break even on ad spend"
        )
    
    with col3:
        st.metric(
            "🔄 Second Order Rate",
            f"{second_order_rate:.1f}%",
            help="% of customers who buy again within 30 days"
        )
    
    st.markdown("---")

    # Retention curve
    retention_data = cohort_df.groupby('day')['retention_rate'].mean().reset_index()

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=['Day 0', 'Day 30', 'Day 60', 'Day 90'],
        y=retention_data['retention_rate'] * 100,
        mode='lines+markers',
        line=dict(color='#00FF88', width=3),
        marker=dict(size=12, color='#00FF88',
                    line=dict(color='#00D9FF', width=2)),
        fill='tozeroy',
        fillcolor='rgba(0, 255, 136, 0.2)',
        name='Retention Rate (%)'
    ))

    fig.update_layout(
        title="Customer Retention Curve",
        title_font_color='#00D9FF',
        xaxis_title="Days Since Acquisition",
        yaxis_title="Retention Rate (%)",
        paper_bgcolor='#0E1117',
        plot_bgcolor='#1E1E1E',
        font=dict(color='#FAFAFA', family='monospace'),
        height=350,
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='#2D2D2D', range=[0, 100]),
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True)

def show_context_graph(df):
    """MER Timeline - Context Graph"""

    st.markdown("---")
    st.markdown("#### 📈 **CONTEXT GRAPH — MER TIMELINE**")

    st.caption("Understanding 'Why' numbers moved")

    # Filter valid data
    valid_df = df[df['funnel_stage'] != 'UNCATEGORIZED']

    # Daily aggregation
    daily_df = valid_df.groupby('date').agg({
        'spend': 'sum',
        'revenue': 'sum'
    }).reset_index()

    daily_df['mer'] = daily_df.apply(lambda row: row['revenue'] / row['spend'] if row['spend'] > 0 else 0, axis=1)

    # Create dual axis chart
    fig = go.Figure()

    # Bar: Spend
    fig.add_trace(go.Bar(
        x=daily_df['date'],
        y=daily_df['spend'],
        name='Ad Spend ($)',
        marker_color='#00D9FF',
        marker_line_color='#0E1117',
        marker_line_width=1,
        yaxis='y',
        opacity=0.7
    ))

    # Line: MER
    fig.add_trace(go.Scatter(
        x=daily_df['date'],
        y=daily_df['mer'],
        name='MER',
        mode='lines+markers',
        line=dict(color='#00FF88', width=3),
        marker=dict(size=6, color='#00FF88'),
        yaxis='y2'
    ))

    # Add event annotations (placeholder)
    # Add event annotations (simulated) - SAFE VERSION
    events = []
    
    # Only add events if we have enough data
    if len(daily_df) > 15:
        events.append({'date': daily_df['date'].iloc[15], 'icon': '📧', 'text': 'Email Blast'})
    
    if len(daily_df) > 45:
        events.append({'date': daily_df['date'].iloc[45], 'icon': '🏷️', 'text': 'Sale Launch'})
    
    if len(daily_df) > 75:
        events.append({'date': daily_df['date'].iloc[75], 'icon': '⚠️', 'text': 'Tech Issue'})

    for event in events:
        fig.add_annotation(
            x=event['date'],
            y=daily_df[daily_df['date'] == event['date']]['mer'].values[0],
            text=f"{event['icon']}<br>{event['text']}",
            showarrow=True,
            arrowhead=2,
            arrowcolor="#FFB800",
            arrowsize=1,
            arrowwidth=2,
            ax=0,
            ay=-60,
            font=dict(size=10, color="#FFFFFF"),
            bgcolor='rgba(30, 30, 30, 0.8)',
            bordercolor='#FFB800',
            borderwidth=2
        )
    
    fig.update_layout(
        title="Daily Ad Spend vs MER (with Event Overlays)",
        title_font_color='#00D9FF',
        xaxis_title="Date",
        yaxis=dict(
            title="Ad Spend ($)",
            titlefont=dict(color='#00D9FF'),
            tickfont=dict(color='#00D9FF'),
            showgrid=True,
            gridcolor='#2D2D2D' 
        ),
        yaxis2=dict(
            title="MER (Marketing Efficiency Ratio)",
            titlefont=dict(color='#00FF88'),
            tickfont=dict(color='#00FF88'),
            overlaying='y',
            side='right',
            showgrid=False
        ),
        paper_bgcolor='#0E1117',
        plot_bgcolor='#1E1E1E',
        font=dict(color='#FAFAFA', family='monospace'),
        hovermode='x unified',
        height=450,
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=-0.3,
            xanchor='center',
            x=0.5
        )
    )

    st.plotly_chart(fig, use_container_width=True)
    st.info("""
    **📊 How to read this chart:**
    - **Blue bars** = Daily ad spend  
    - **Green line** = Marketing Efficiency Ratio (Revenue ÷ Spend)  
    - **Yellow icons** = External events that influenced performance
    """)

def show_ai_insights(df):
    """AI Bain Logic - Automated Insights"""
    st.markdown("---")
    st.markdown("#### 🤖 **AI BRAIN LOGIC — AUTOMATED INSIGHTS**")

    # Calculate key metrics
    valid_df = df[df['funnel_stage'] != 'UNCATEGORIZED']

    total_spend = valid_df['spend'].sum()
    total_revenue = valid_df['revenue'].sum()
    mer = total_revenue / total_spend if total_spend > 0 else 0

    # Last 7 days vs previous 7 days
    last_7 = valid_df[valid_df['date'] >= valid_df['date'].max() - pd.Timedelta(days=7)]
    prev_7 = valid_df[
        (valid_df['date'] >= valid_df['date'].max() - pd.Timedelta(days=14)) &
        (valid_df['date'] < valid_df['date'].max() - pd.Timedelta(days=7))
    ]

    last_7_mer = last_7['revenue'].sum() / last_7['spend'].sum() if last_7['spend'].sum() > 0 else 0
    prev_7_mer = prev_7['revenue'].sum() / prev_7['spend'].sum() if prev_7['spend'].sum() > 0 else 0

    mer_change = ((last_7_mer - prev_7_mer)/prev_7_mer * 100) if prev_7_mer > 0 else 0

    # Generate insights
    insights = []

    # Insight 1: MER Change
    if mer < TARGETS['MER']:
        ctr_avg = valid_df['ctr'].mean()
        conv_avg = valid_df['conv_rate'].mean()

        if conv_avg < 2.0:
            insights.append({
                'type': 'warning',
                'title': '⚠️ Profit Protector Alert',
                'message': f"Your MER is below target at {mer:.2f}x. Consider optimizing your bottom funnel strategies to boost conversions."
            })
    
    # insight 2: Scale Signal
    tof_data = valid_df[valid_df['funnel_stage'] == 'TOF']
    if not tof_data.empty:
        tof_cpa = tof_data['spend'].sum() / tof_data['orders'].sum() if tof_data['orders'].sum() > 0 else 0
        tof_spend = tof_data['spend'].sum()

        if tof_cpa < 30 and tof_spend < 200000:
            insights.append({
                'type': 'success',
                'title': '🚀 Scale Signal Detected',
                'message': f"Your TOF CPA is strong at ${tof_cpa:.2f}. Consider increasing your top funnel budget to capitalize on this efficiency."
            })
    
    # Insight 3: Cohort Performance
    ret_data = valid_df[valid_df['funnel_stage'] == 'RET']
    if not ret_data.empty:
        ret_roas = ret_data['revenue'].sum() / ret_data['spend'].sum() if ret_data['spend'].sum() > 0 else 0

        if ret_roas > 5.0:
            insights.append({
                'type': 'info',
                'title': '💎 Whale Watcher Alert',
                'message': f"Retention campaigns are delivering {ret_roas:.1f}x ROAS (exceptional!). Recent cohorts show high repeat purchase rates. **Recommendation:** Scale retention spend immediately."
            })
    
    # Insight 4: MER Trend
    if mer_change < -10:
        insights.append({
            'type': 'warning',
            'title': '📉 MER Downtrend Detected',
            'message': f"'MER declined {abs(mer_change):.1f}% week-over-week. Monitor CTR and conversion rates closely. Consider refreshing creative assets."
        })
    elif mer_change > 15:
        insights.append({
            'type': 'success',
            'title': '📈 Positive Momentum',
            'message': f'MER improved {mer_change:.1f}% week-over-week. Continue current strategy and consider gradual spend increases.'
        })

    # Display insights
    if insights:
        for insight in insights:
            if insight['type'] == 'warning':
                st.warning(f"**{insight['title']}**\n\n{insight['message']}")
            elif insight['type'] == 'success':
                st.success(f"**{insight['title']}**\n\n{insight['message']}")
            else:
                st.info(f"**{insight['title']}**\n\n{insight['message']}")
    else:
        st.info("✅ **All systems nominal.** No immediate action items detected.")