""" 
Data Loader Utility
Centralized data loading for all module
"""

import pandas as pd
import streamlit as st
from pathlib import Path

class DataLoader:
    def __init__(self):
        self.data_dir = Path('data/processed')
    
    @st.cache_data
    def load_revenue_data(_self):
        """Load processed revenue data"""
        try:
            df = pd.read_csv(_self.data_dir / 'revenue_data.csv')
            df['date'] = pd.to_datetime(df['date'])
            return df
        except FileNotFoundError:
            st.error("Revenue data file not found.")
            return pd.DataFrame()
    
    @st.cache_data
    def load_cohort_data(_self):
        """Load processed cohort analysis data"""
        try:
            df = pd.read_csv(_self.data_dir / 'cohort_data.csv')
            df['aquisition_date'] = pd.to_datetime(df['acquisition_date'])
            return df
        except FileNotFoundError:
            st.error("Cohort data file not found.")
            return pd.DataFrame()
    
    @st.cache_data
    def load_social_data(_self):
        """Load processed social media data"""
        try:
            df = pd.read_csv(_self.data_dir / 'social_data.csv')
            df['date'] = pd.to_datetime(df['date'])
            return df
        except FileNotFoundError:
            st.error("Social media data file not found.")
            return pd.DataFrame()
    
    @st.cache_data
    def load_funnel_data(_self):
        """Load processed funnel data"""
        try:
            df = pd.read_csv(_self.data_dir / 'funnel_data.csv')
            df['date'] = pd.to_datetime(df['date'])
            return df
        except FileNotFoundError:
            st.error("Funnel data file not found.")
            return pd.DataFrame()
    
    @st.cache_data
    def load_revops_data(_self):
        """Load processed RevOps automation data"""
        try:
            df = pd.read_csv(_self.data_dir / 'revops_data.csv')
            df['date'] = pd.to_datetime(df['date'])
            return df
        except FileNotFoundError:
            st.error("RevOps data file not found.")
            return pd.DataFrame()
    
    @st.cache_data
    def load_organic_data(_self):
        """Load processed organic architecture data"""
        try:
            df = pd.read_csv(_self.data_dir / 'organic_data.csv')
            df['date'] = pd.to_datetime(df['date'])
            return df
        except FileNotFoundError:
            st.error("Organic data file not found.")
            return pd.DataFrame()
    
    @st.cache_data
    def load_social_data(_self):
        """Load processed social media data"""
        try:
            df = pd.read_csv(_self.data_dir / 'social_data.csv')
            df['date'] = pd.to_datetime(df['date'])
            return df
        except FileNotFoundError:
            st.error("Social media data file not found.")
            return pd.DataFrame()
    
    @st.cache_data
    def load_content_library(_self):
        """Load processed content library data"""
        try:
            df = pd.read_csv(_self.data_dir / 'content_library.csv')
            df['date'] = pd.to_datetime(df['date'])
            return df
        except FileNotFoundError:
            st.error("Content library data file not found.")
            return pd.DataFrame()
    
    # Module 3 specific data loading functions
    @st.cache_data
    def load_funnel_module3_data(_self):
        """Load processed funnel data for CRO Terminal"""
        try:
            df = pd.read_csv(_self.data_dir / 'funnel_module3_data.csv')
            df['date'] = pd.to_datetime(df['date'])
            return df
        except FileNotFoundError:
            st.error("Funnel data for CRO Terminal not found.")
            return pd.DataFrame()

    @st.cache_data
    def load_funnel_by_device(_self):
        """Load funnel by device data for CRO Terminal"""
        try:
            df = pd.read_csv(_self.data_dir / 'funnel_by_device.csv')
            df['date'] = pd.to_datetime(df['date'])
            return df
        except FileNotFoundError:
            st.error("Funnel by device data for CRO Terminal not found.")
            return pd.DataFrame()
    
    @st.cache_data
    def load_funnel_by_source(_self):
        """Load funnel by source data for CRO Terminal"""
        try:
            df = pd.read_csv(_self.data_dir / 'funnel_by_source.csv')
            df['date'] = pd.to_datetime(df['date'])
            return df
        except FileNotFoundError:
            st.error("Funnel by source data for CRO Terminal not found.")
            return pd.DataFrame()
    
    @st.cache_data
    def load_page_speed_data(_self):
        """Load page speed data for CRO Terminal"""
        try:
            df = pd.read_csv(_self.data_dir / 'page_speed_data.csv')
            df['date'] = pd.to_datetime(df['date'])
            return df
        except FileNotFoundError:
            st.error("Page speed data for CRO Terminal not found.")
            return pd.DataFrame()

    @st.cache_data
    def load_traffic_data(_self):
        """Load traffic data for CRO Terminal"""
        try:
            df = pd.read_csv(_self.data_dir / 'traffic_data.csv')
            df['date'] = pd.to_datetime(df['date'])
            return df
        except FileNotFoundError:
            st.error("Traffic data for CRO Terminal not found.")
            return pd.DataFrame()

    
    # def load_all(_self):
    #     """Load all datasets"""
    #     return {
    #         'revenue_data': _self.load_revenue_data(),
    #         'cohort_data': _self.load_cohort_data(),
    #         'social_data': _self.load_social_data(),
    #         'funnel_data': _self.load_funnel_data(),
    #         'revops_data': _self.load_revops_data()
    #     }