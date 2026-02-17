import streamlit as st
import sys
from pathlib import Path
import pandas as pd

# Add project root to sys.path for module imports
sys.path.append(str(Path(__file__).parent))

from config.settings import *

# Page configuration
st.set_page_config(
    page_title="Marktivo Growth OS",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# load custom CSS
def load_css():
    css_path = Path(__file__).parent / 'assets' / 'styles.css'
    with open(css_path) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Main app 
def main():
    # Load custom CSS
    load_css()

    # Sidebar navigation
    st.sidebar.title("🎯 MARKTIVO GROWTH OS")
    st.sidebar.markdown("---")

    page = st.sidebar.radio(
        "Navigation",
        ["🏠 Dashboard Overview", 
        "💰 Revenue Engineering", 
        "📱 Organic Architecture", 
        "🎯 CRO Terminal", 
        "🤖 RevOps Automation"]
    )

    # Page routing
    if page == "🏠 Dashboard Overview":
        show_overview()
    elif page == "💰 Revenue Engineering":
        show_revenue_engineering()
    elif page == "📱 Organic Architecture":
        show_organic_architecture()
    elif page == "🎯 CRO Terminal":
        show_cro_terminal()
    elif page == "🤖 RevOps Automation":
        st.title("🤖 RevOps Automation")
        st.info("Module 4 - Coming soon...")

def show_overview():
    """Dashboard Overview - North Star Metrics"""

    st.title("🎯 MARKTIVO GROWTH OS")
    st.markdown("### **The Glass Box** - Radical Transparency Dashboard")
    st.markdown("---")

    # Load data
    from utils.data_loader import DataLoader
    loader = DataLoader()

    revenue_df = loader.load_revenue_data()

    if not revenue_df.empty:
        # Calculate key metrics
        last_7_days = revenue_df[revenue_df['date'] >= revenue_df['date'].max() - pd.Timedelta(days=7)]

        total_revenue = last_7_days['revenue'].sum()
        total_spend = last_7_days['spend'].sum()
        mer = total_revenue / total_spend if total_spend > 0 else 0
        contribution = total_revenue - total_spend

        # North Star Metrics
        st.markdown('#### 📊 **NORTH STAR METRICS** (Last 7 Days)')

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                label="MER (7-Day Rolling)",
                value=f"{mer:,.2f}x",
                delta="+3%",
                help="Marketing Efficiency Ratio: Revenue / Spend"
            )
        with col2:
            st.metric(
                label="Contribution Margin",
                value=f"${contribution:,.0f}",
                delta="+12%",
                help="Total Revenue - Total Ad Spend"
            )
        
        with col3:
            st.metric(
                label="Projected LTV:CAC",
                value="3.2",
                delta="+0.4",
                help="60-Day LTV divided by CPA (Target > 3.0)"
            )
        
        with col4:
            st.metric(
                label="Real Revenue",
                value=f"${total_revenue:,.0f}",
                delta="+8%",
                help="Backend confirmed orders (Source of Truth)"
            )
        
        st.markdown("---")

        # Data Preview
        with st.expander("📋 **Data Preview** (Last 10 Days)"):
            st.dataframe(
                revenue_df.tail(40)[['date', 'funnel_stage', 'spend', 'revenue', 'roas', 'orders']],
                use_container_width=True
            )
    else:
        st.warning("⚠️ No data available.")
    
    # Rest of the function
    st.markdown("---")

    # Module Status
    st.markdown("#### 🔧 **MODULE STATUS**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.success("✅ **Module 1:** Revenue Engineering - In Progress")
        st.success("✅ **Module 2:** Organic Architecture - In Progress")
    
    with col2:
        st.success("✅ **Module 3:** CRO Terminal - In Progress")
        st.info("🚧 **Module 4:** RevOps Automation - Pending")
    
    st.markdown("---")
    
    # Quick Info
    st.info("""
    **🎯 Dashboard Philosophy:**  
    *"The Glass Box"* - Radical transparency. You sit in the cockpit; 
    the dashboard provides the flight data. Context is King. 
    Enforce operational discipline and prevent knee-jerk decisions.
    """)

def show_revenue_engineering():
    """Module 1: Revenue Engineering"""
    from modules.revenue_engineering import show_revenue_engineering as revenue_module
    revenue_module()

def show_organic_architecture():
    """Module 2: Organic Architecture"""
    from modules.organic_architecture import show_organic_architecture as organic_module
    organic_module()

def show_cro_terminal():
    """Module 3: CRO Terminal"""
    from modules.cro_terminal import show_cro_terminal as cro_module
    cro_module()


if __name__ == "__main__":
    main()