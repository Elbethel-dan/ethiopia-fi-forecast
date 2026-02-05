import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime
import warnings
import os
from pathlib import Path
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Ethiopia Financial Inclusion Dashboard",
    page_icon="🇪🇹",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #3B82F6;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }
    .ethiopia-flag {
        background: linear-gradient(90deg, #078930 33%, #FEDE00 33%, #FEDE00 66%, #DA121A 66%);
        height: 5px;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #F8FAFC;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #078930;
        margin-bottom: 1rem;
    }
    .stButton>button {
        background-color: #078930;
        color: white;
    }
    .dataframe {
        font-size: 14px;
    }
</style>
""", unsafe_allow_html=True)

class EthiopiaDataLoader:
    """Load Ethiopia-specific financial inclusion data from CSV files"""
    
    def __init__(self):
        # Update this to your actual directory structure
        self.base_path = Path("/Users/elbethelzewdie/Downloads/ethiopia-fi-forecast/ethiopia-fi-forecast/data")
        self.raw_path = self.base_path / "raw"
        self.processed_path = self.base_path / "processed"
        
        # Create directories if they don't exist
        self.raw_path.mkdir(parents=True, exist_ok=True)
        self.processed_path.mkdir(parents=True, exist_ok=True)
    
    def load_unified_data(self):
        """Load the main unified dataset"""
        # Try multiple possible file locations
        possible_paths = [
            self.raw_path / "ethiopia_fi_unified_new.csv",
            self.base_path / "ethiopia_fi_unified_new.csv",
            Path("data/raw/ethiopia_fi_unified_new.csv"),
            Path("ethiopia_fi_unified_new.csv")
        ]
        
        for file_path in possible_paths:
            if file_path.exists():
                try:
                    df = pd.read_csv(file_path)
                    st.sidebar.success(f"✅ Loaded unified data from: {file_path}")
                    return df
                except Exception as e:
                    st.sidebar.error(f"❌ Error reading {file_path}: {e}")
        
        st.sidebar.error("❌ Could not find ethiopia_fi_unified_new.csv")
        return None
    
    def load_impact_data(self):
        """Load impact sheet data"""
        possible_paths = [
            self.raw_path / "impact_sheet_new.csv",
            self.base_path / "impact_sheet_new.csv",
            Path("data/raw/impact_sheet_new.csv"),
            Path("impact_sheet_new.csv")
        ]
        
        for file_path in possible_paths:
            if file_path.exists():
                try:
                    df = pd.read_csv(file_path)
                    st.sidebar.success(f"✅ Loaded impact data from: {file_path}")
                    return df
                except Exception as e:
                    st.sidebar.warning(f"⚠️ Error reading impact data: {e}")
        
        st.sidebar.warning("⚠️ Impact data not found, using sample data")
        return None
    
    def load_usage_forecast(self):
        """Load usage forecast data"""
        # First try to load from file
        forecast_path = self.processed_path / "usage_forecast.csv"
        if forecast_path.exists():
            try:
                df = pd.read_csv(forecast_path)
                return df
            except:
                pass
        
        # Fallback to sample data
        data = {
            'Year': [2012, 2014, 2024, 2025, 2026, 2027],
            'Type': ['Historical', 'Historical', 'Historical', 'Forecast', 'Forecast', 'Forecast'],
            'Actual': [9914800.0, 1500.0, 563481793.3, None, None, None],
            'Base': [None, None, None, 56.9, 59.5, 62.2],
            'Optimistic': [None, None, None, 64.6, 67.9, 71.3],
            'Pessimistic': [None, None, None, 49.2, 51.1, 53.1]
        }
        return pd.DataFrame(data)
    
    def load_access_forecast(self):
        """Load access forecast data"""
        forecast_path = self.processed_path / "access_forecast.csv"
        if forecast_path.exists():
            try:
                df = pd.read_csv(forecast_path)
                return df
            except:
                pass
        
        data = {
            'Year': [2014, 2017, 2021, 2024, 2025, 2026, 2027],
            'Type': ['Historical', 'Historical', 'Historical', 'Historical', 'Forecast', 'Forecast', 'Forecast'],
            'Actual': [2200.0, 3500.0, 4600.0, 4900.0, None, None, None],
            'Base': [None, None, None, None, 58.7, 60.7, 62.9],
            'Optimistic': [None, None, None, None, 63.9, 66.4, 69.1],
            'Pessimistic': [None, None, None, None, 53.5, 55.0, 56.7]
        }
        return pd.DataFrame(data)
    
    def load_forecast_summary(self):
        """Load forecast summary data"""
        summary_path = self.processed_path / "forecast_summary.csv"
        if summary_path.exists():
            try:
                df = pd.read_csv(summary_path)
                return df
            except:
                pass
        
        data = {
            'Indicator': ['Account Ownership', 'Account Ownership', 'Account Ownership', 
                         'Digital Payment Usage', 'Digital Payment Usage', 'Digital Payment Usage'],
            'Year': [2025, 2026, 2027, 2025, 2026, 2027],
            'Trend_Only': [54.2, 56.9, 59.7, 51.1, 54.6, 58.0],
            'Event_Impact': ['+4.5%', '+3.8%', '+3.2%', '+5.8%', '+4.9%', '+4.2%'],
            'Total_Forecast': [58.7, 60.7, 62.9, 56.9, 59.5, 62.2]
        }
        return pd.DataFrame(data)
    
    def process_historical_data(self, df):
        """Process historical data to extract time series"""
        if df is not None:
            try:
                # Try to extract year from date column
                if 'date' in df.columns:
                    df['Year'] = pd.to_datetime(df['date']).dt.year
                elif 'year' in df.columns:
                    df['Year'] = df['year']
                elif 'Year' in df.columns:
                    df['Year'] = df['Year']
                
                # Group by year and calculate averages
                yearly_data = df.groupby('Year').mean().reset_index()
                
                # Ensure we have data for 2012-2024
                all_years = pd.DataFrame({'Year': range(2012, 2025)})
                yearly_data = pd.merge(all_years, yearly_data, on='Year', how='left')
                
                # Fill missing columns with sample data
                required_columns = ['Account_Ownership', 'Digital_Payments', 
                                   'ATM_Penetration', 'Agent_Banking', 'Mobile_Money']
                
                for col in required_columns:
                    if col not in yearly_data.columns:
                        if col == 'Account_Ownership':
                            yearly_data[col] = np.linspace(20, 49, len(yearly_data)) + np.random.normal(0, 2, len(yearly_data))
                        elif col == 'Digital_Payments':
                            yearly_data[col] = np.linspace(15, 45, len(yearly_data)) + np.random.normal(0, 2, len(yearly_data))
                        elif col == 'ATM_Penetration':
                            yearly_data[col] = np.linspace(5, 25, len(yearly_data)) + np.random.normal(0, 1, len(yearly_data))
                        elif col == 'Agent_Banking':
                            yearly_data[col] = np.linspace(1, 15, len(yearly_data)) + np.random.normal(0, 0.5, len(yearly_data))
                        elif col == 'Mobile_Money':
                            yearly_data[col] = np.linspace(0, 30, len(yearly_data)) + np.random.normal(0, 1.5, len(yearly_data))
                
                return yearly_data
            except Exception as e:
                st.sidebar.warning(f"⚠️ Could not process CSV: {e}")
        
        # Fallback to sample data
        years = list(range(2012, 2025))
        return pd.DataFrame({
            'Year': years,
            'Account_Ownership': np.linspace(20, 49, len(years)) + np.random.normal(0, 2, len(years)),
            'Digital_Payments': np.linspace(15, 45, len(years)) + np.random.normal(0, 2, len(years)),
            'ATM_Penetration': np.linspace(5, 25, len(years)) + np.random.normal(0, 1, len(years)),
            'Agent_Banking': np.linspace(1, 15, len(years)) + np.random.normal(0, 0.5, len(years)),
            'Mobile_Money': np.linspace(0, 30, len(years)) + np.random.normal(0, 1.5, len(years))
        })

class EthiopiaDashboard:
    def __init__(self):
        self.data_loader = EthiopiaDataLoader()
        self.load_all_data()
    
    def load_all_data(self):
        """Load all datasets"""
        # Load raw data
        self.unified_data = self.data_loader.load_unified_data()
        self.impact_data = self.data_loader.load_impact_data()
        
        # Process historical data
        self.historical_data = self.data_loader.process_historical_data(self.unified_data)
        
        # Load forecasts
        self.usage_forecast = self.data_loader.load_usage_forecast()
        self.access_forecast = self.data_loader.load_access_forecast()
        self.forecast_summary = self.data_loader.load_forecast_summary()
    
    def overview_page(self):
        """Render overview page"""
        st.markdown('<div class="ethiopia-flag"></div>', unsafe_allow_html=True)
        st.markdown('<h1 class="main-header">🇪🇹 Ethiopia Financial Inclusion Dashboard</h1>', unsafe_allow_html=True)
        
        # Key metrics from historical data (2024)
        latest_year = 2024
        latest_data = self.historical_data[self.historical_data['Year'] == latest_year]
        
        if not latest_data.empty:
            latest_row = latest_data.iloc[0]
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                st.metric(
                    label="Account Ownership (2024)",
                    value=f"{latest_row['Account_Ownership']:.1f}%",
                    delta=f"From 20% in 2012"
                )
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                st.metric(
                    label="Digital Payment Usage",
                    value=f"{latest_row['Digital_Payments']:.1f}%",
                    delta=f"+{latest_row['Digital_Payments'] - 15:.1f}% since 2012"
                )
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col3:
                st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                st.metric(
                    label="Mobile Money Penetration",
                    value=f"{latest_row['Mobile_Money']:.1f}%",
                    delta="Rapid growth"
                )
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col4:
                # Get forecast for 2025
                usage_2025 = self.usage_forecast[
                    (self.usage_forecast['Year'] == 2025) & 
                    (self.usage_forecast['Type'] == 'Forecast')
                ]['Base'].values[0]
                
                st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                st.metric(
                    label="2025 Forecast (Base)",
                    value=f"{usage_2025:.1f}%",
                    delta="Digital Payments"
                )
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Historical Trend 2012-2024
            st.markdown('<h3 class="sub-header">📊 Historical Trends (2012-2024)</h3>', unsafe_allow_html=True)
            
            fig = go.Figure()
            
            metrics = ['Account_Ownership', 'Digital_Payments', 'Mobile_Money']
            colors = ['#078930', '#3B82F6', '#F59E0B']
            
            for metric, color in zip(metrics, colors):
                fig.add_trace(go.Scatter(
                    x=self.historical_data['Year'],
                    y=self.historical_data[metric],
                    name=metric.replace('_', ' '),
                    line=dict(color=color, width=3),
                    mode='lines+markers'
                ))
            
            fig.update_layout(
                title="Financial Inclusion Metrics (2012-2024)",
                xaxis_title="Year",
                yaxis_title="Percentage (%)",
                hovermode="x unified",
                height=400
            )
            
            st.plotly_chart(fig, width='stretch')
        
        # Forecast Summary
        st.markdown('<h3 class="sub-header">📈 Forecast Summary (2025-2027)</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Digital Payment Usage Forecast:**")
            usage_display = self.usage_forecast[self.usage_forecast['Type'] == 'Forecast'][['Year', 'Base', 'Optimistic', 'Pessimistic']]
            st.dataframe(
                usage_display.style.format({
                    'Base': '{:.1f}%',
                    'Optimistic': '{:.1f}%',
                    'Pessimistic': '{:.1f}%'
                }), 
                width='stretch'
            )
        
        with col2:
            st.markdown("**Account Access Forecast:**")
            access_display = self.access_forecast[self.access_forecast['Type'] == 'Forecast'][['Year', 'Base', 'Optimistic', 'Pessimistic']]
            st.dataframe(
                access_display.style.format({
                    'Base': '{:.1f}%',
                    'Optimistic': '{:.1f}%',
                    'Pessimistic': '{:.1f}%'
                }), 
                width='stretch'
            )
        
        # Detailed Forecast Summary
        st.markdown('<h3 class="sub-header">📋 Detailed Forecast Components</h3>', unsafe_allow_html=True)
        st.dataframe(self.forecast_summary, width='stretch')
    
    def trends_page(self):
        """Render trends analysis page"""
        st.markdown('<div class="ethiopia-flag"></div>', unsafe_allow_html=True)
        st.markdown('<h1 class="main-header">📈 Ethiopia FI Trends Analysis</h1>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([3, 1])
        
        with col2:
            # Year range selector
            min_year = int(self.historical_data['Year'].min())
            max_year = int(self.historical_data['Year'].max())
            
            year_range = st.slider(
                "Select Year Range:",
                min_value=min_year,
                max_value=max_year,
                value=(min_year, max_year)
            )
            
            # Metric selection
            metrics = st.multiselect(
                "Select Metrics:",
                options=['Account_Ownership', 'Digital_Payments', 'ATM_Penetration', 
                        'Agent_Banking', 'Mobile_Money'],
                default=['Account_Ownership', 'Digital_Payments']
            )
            
            # View type
            view_type = st.radio(
                "View Type:",
                options=["Line Chart", "Bar Chart", "Area Chart"]
            )
        
        # Filter data
        filtered_data = self.historical_data[
            (self.historical_data['Year'] >= year_range[0]) & 
            (self.historical_data['Year'] <= year_range[1])
        ]
        
        with col1:
            # Create visualization
            fig = go.Figure()
            
            colors = px.colors.qualitative.Set3
            
            if view_type == "Line Chart":
                for i, metric in enumerate(metrics):
                    fig.add_trace(go.Scatter(
                        x=filtered_data['Year'],
                        y=filtered_data[metric],
                        name=metric.replace('_', ' '),
                        line=dict(color=colors[i % len(colors)], width=3),
                        mode='lines+markers'
                    ))
            
            elif view_type == "Bar Chart":
                for metric in metrics:
                    fig.add_trace(go.Bar(
                        x=filtered_data['Year'],
                        y=filtered_data[metric],
                        name=metric.replace('_', ' '),
                        marker_color=colors[metrics.index(metric) % len(colors)]
                    ))
                fig.update_layout(barmode='group')
            
            else:  # Area Chart
                for metric in metrics:
                    fig.add_trace(go.Scatter(
                        x=filtered_data['Year'],
                        y=filtered_data[metric],
                        name=metric.replace('_', ' '),
                        fill='tozeroy',
                        mode='lines'
                    ))
            
            fig.update_layout(
                title=f"Financial Inclusion Trends ({year_range[0]}-{year_range[1]})",
                xaxis_title="Year",
                yaxis_title="Percentage (%)",
                hovermode="x unified",
                height=500
            )
            
            st.plotly_chart(fig, width='stretch')
        
        # Data table
        st.markdown('<h3 class="sub-header">📊 Historical Data</h3>', unsafe_allow_html=True)
        st.dataframe(filtered_data, width='stretch', height=300)
        
        # Download button
        st.download_button(
            label="📥 Download Historical Data",
            data=filtered_data.to_csv(index=False),
            file_name=f"ethiopia_fi_trends_{year_range[0]}_{year_range[1]}.csv",
            mime="text/csv"
        )
    
    def forecasts_page(self):
        """Render forecasts page"""
        st.markdown('<div class="ethiopia-flag"></div>', unsafe_allow_html=True)
        st.markdown('<h1 class="main-header">🔮 Ethiopia FI Forecasts (2025-2027)</h1>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([3, 1])
        
        with col2:
            # Forecast type selection
            forecast_type = st.radio(
                "Forecast Type:",
                options=["Digital Payment Usage", "Account Access", "Comparison"]
            )
            
            # Scenario selection
            scenarios = st.multiselect(
                "Select Scenarios:",
                options=["Base", "Optimistic", "Pessimistic"],
                default=["Base", "Optimistic"]
            )
            
            # Show confidence intervals
            show_ci = st.checkbox("Show Uncertainty Range", value=True)
        
        with col1:
            # Create forecast visualization
            fig = go.Figure()
            
            # Colors for scenarios
            color_map = {"Base": "#078930", "Optimistic": "#10B981", "Pessimistic": "#EF4444"}
            
            # Historical data (2012-2024)
            if forecast_type != "Comparison":
                historical_metric = "Digital_Payments" if forecast_type == "Digital Payment Usage" else "Account_Ownership"
                fig.add_trace(go.Scatter(
                    x=self.historical_data['Year'],
                    y=self.historical_data[historical_metric],
                    name=f"Historical {forecast_type}",
                    line=dict(color='#6B7280', width=2, dash='dot'),
                    mode='lines'
                ))
            
            # Add forecasts
            forecast_years = [2025, 2026, 2027]
            
            if forecast_type == "Digital Payment Usage":
                forecast_df = self.usage_forecast[self.usage_forecast['Type'] == 'Forecast']
                for scenario in scenarios:
                    values = forecast_df[scenario].values
                    fig.add_trace(go.Scatter(
                        x=forecast_years,
                        y=values,
                        name=f"Digital - {scenario}",
                        line=dict(color=color_map[scenario], width=3),
                        mode='lines+markers'
                    ))
            
            elif forecast_type == "Account Access":
                forecast_df = self.access_forecast[self.access_forecast['Type'] == 'Forecast']
                for scenario in scenarios:
                    values = forecast_df[scenario].values
                    fig.add_trace(go.Scatter(
                        x=forecast_years,
                        y=values,
                        name=f"Access - {scenario}",
                        line=dict(color=color_map[scenario], width=3),
                        mode='lines+markers'
                    ))
            
            else:  # Comparison
                # Digital payments
                usage_df = self.usage_forecast[self.usage_forecast['Type'] == 'Forecast']
                for scenario in scenarios:
                    values = usage_df[scenario].values
                    fig.add_trace(go.Scatter(
                        x=forecast_years,
                        y=values,
                        name=f"Digital - {scenario}",
                        line=dict(color=color_map[scenario], width=3, dash='solid'),
                        mode='lines+markers'
                    ))
                
                # Account access
                access_df = self.access_forecast[self.access_forecast['Type'] == 'Forecast']
                for scenario in scenarios:
                    values = access_df[scenario].values
                    fig.add_trace(go.Scatter(
                        x=forecast_years,
                        y=values,
                        name=f"Access - {scenario}",
                        line=dict(color=color_map[scenario], width=3, dash='dash'),
                        mode='lines+markers'
                    ))
            
            # Add target lines
            fig.add_hline(y=60, line_dash="dash", line_color="#F59E0B",
                         annotation_text="60% Target")
            fig.add_hline(y=65, line_dash="dot", line_color="#8B5CF6",
                         annotation_text="65% Target")
            
            fig.update_layout(
                title=f"Ethiopia Financial Inclusion Forecasts",
                xaxis_title="Year",
                yaxis_title="Percentage (%)",
                hovermode="x unified",
                height=500
            )
            
            st.plotly_chart(fig, width='stretch')
        
        # Forecast details table
        st.markdown('<h3 class="sub-header">📋 Forecast Details</h3>', unsafe_allow_html=True)
        
        if forecast_type == "Digital Payment Usage":
            forecast_df = self.usage_forecast[self.usage_forecast['Type'] == 'Forecast']
        elif forecast_type == "Account Access":
            forecast_df = self.access_forecast[self.access_forecast['Type'] == 'Forecast']
        else:
            # Show both
            usage_df = self.usage_forecast[self.usage_forecast['Type'] == 'Forecast'].copy()
            access_df = self.access_forecast[self.access_forecast['Type'] == 'Forecast'].copy()
            usage_df['Type'] = 'Digital Payments'
            access_df['Type'] = 'Account Access'
            forecast_df = pd.concat([usage_df, access_df])
        
        st.dataframe(forecast_df, width='stretch')
        
        # Download forecast data
        st.download_button(
            label="📥 Download Forecast Data",
            data=forecast_df.to_csv(index=False),
            file_name="ethiopia_fi_forecasts.csv",
            mime="text/csv"
        )
    
    def projections_page(self):
        """Render projections page"""
        st.markdown('<div class="ethiopia-flag"></div>', unsafe_allow_html=True)
        st.markdown('<h1 class="main-header">🎯 Ethiopia FI Projections & Scenarios</h1>', unsafe_allow_html=True)
        
        # Scenario configuration
        col1, col2, col3 = st.columns(3)
        
        with col1:
            base_growth = st.slider(
                "Base Annual Growth Rate (%):",
                min_value=1.0,
                max_value=10.0,
                value=3.5,
                step=0.1
            )
        
        with col2:
            opt_boost = st.slider(
                "Optimistic Boost (% points):",
                min_value=0.5,
                max_value=5.0,
                value=1.8,
                step=0.1
            )
        
        with col3:
            pess_drag = st.slider(
                "Pessimistic Drag (% points):",
                min_value=0.5,
                max_value=5.0,
                value=2.2,
                step=0.1
            )
        
        # Get current values from forecasts
        current_digital = 45.0  # Default
        current_access = 49.0   # Default
        
        # Try to get actual 2024 values
        if 2024 in self.historical_data['Year'].values:
            current_digital = self.historical_data[self.historical_data['Year'] == 2024]['Digital_Payments'].values[0]
            current_access = self.historical_data[self.historical_data['Year'] == 2024]['Account_Ownership'].values[0]
        
        # Generate projections to 2030
        years = list(range(2024, 2031))
        
        # Create projections
        digital_scenarios = {}
        access_scenarios = {}
        
        for scenario_name, modifier in [('Base', 0), ('Optimistic', opt_boost), ('Pessimistic', -pess_drag)]:
            # Digital payments projection
            digital_rates = [current_digital]
            for i in range(1, len(years)):
                growth = (base_growth + modifier) / 100
                new_rate = digital_rates[-1] * (1 + growth)
                digital_rates.append(min(new_rate, 100))
            digital_scenarios[scenario_name] = digital_rates
            
            # Account access projection
            access_rates = [current_access]
            for i in range(1, len(years)):
                growth = (base_growth + modifier) / 100
                new_rate = access_rates[-1] * (1 + growth)
                access_rates.append(min(new_rate, 100))
            access_scenarios[scenario_name] = access_rates
        
        # Create visualizations
        tab1, tab2 = st.tabs(["Digital Payment Usage", "Account Access"])
        
        with tab1:
            fig1 = go.Figure()
            colors = {'Base': '#078930', 'Optimistic': '#10B981', 'Pessimistic': '#EF4444'}
            
            for scenario, rates in digital_scenarios.items():
                fig1.add_trace(go.Scatter(
                    x=years,
                    y=rates,
                    name=scenario,
                    line=dict(color=colors[scenario], width=3),
                    mode='lines+markers'
                ))
            
            # Add target lines
            fig1.add_hline(y=60, line_dash="dash", line_color="#F59E0B",
                          annotation_text="60% Target")
            fig1.add_hline(y=70, line_dash="dot", line_color="#8B5CF6",
                          annotation_text="70% Target")
            
            fig1.update_layout(
                title="Digital Payment Usage Projections (2024-2030)",
                xaxis_title="Year",
                yaxis_title="Percentage (%)",
                height=450
            )
            
            st.plotly_chart(fig1, width='stretch')
        
        with tab2:
            fig2 = go.Figure()
            
            for scenario, rates in access_scenarios.items():
                fig2.add_trace(go.Scatter(
                    x=years,
                    y=rates,
                    name=scenario,
                    line=dict(color=colors[scenario], width=3),
                    mode='lines+markers'
                ))
            
            # Add target lines
            fig2.add_hline(y=65, line_dash="dash", line_color="#F59E0B",
                          annotation_text="65% Target")
            fig2.add_hline(y=75, line_dash="dot", line_color="#8B5CF6",
                          annotation_text="75% Target")
            
            fig2.update_layout(
                title="Account Access Projections (2024-2030)",
                xaxis_title="Year",
                yaxis_title="Percentage (%)",
                height=450
            )
            
            st.plotly_chart(fig2, width='stretch')
        
        # Target analysis
        st.markdown('<h3 class="sub-header">🎯 Target Achievement Analysis</h3>', unsafe_allow_html=True)
        
        col4, col5 = st.columns(2)
        
        with col4:
            st.markdown("**Digital Payments (60% Target):**")
            for scenario, rates in digital_scenarios.items():
                achieved = False
                for i, year in enumerate(years):
                    if rates[i] >= 60:
                        st.success(f"✅ **{scenario}**: {year} ({rates[i]:.1f}%)")
                        achieved = True
                        break
                if not achieved:
                    st.warning(f"⚠️ **{scenario}**: {rates[-1]:.1f}% in 2030")
        
        with col5:
            st.markdown("**Account Access (65% Target):**")
            for scenario, rates in access_scenarios.items():
                achieved = False
                for i, year in enumerate(years):
                    if rates[i] >= 65:
                        st.success(f"✅ **{scenario}**: {year} ({rates[i]:.1f}%)")
                        achieved = True
                        break
                if not achieved:
                    st.warning(f"⚠️ **{scenario}**: {rates[-1]:.1f}% in 2030")
        
        # Create downloadable projections
        projection_data = []
        for i, year in enumerate(years):
            row = {'Year': year}
            for scenario in ['Base', 'Optimistic', 'Pessimistic']:
                row[f'Digital_{scenario}'] = digital_scenarios[scenario][i]
                row[f'Access_{scenario}'] = access_scenarios[scenario][i]
            projection_data.append(row)
        
        projection_df = pd.DataFrame(projection_data)
        
        # Download button
        st.download_button(
            label="📥 Download Projection Scenarios",
            data=projection_df.to_csv(index=False),
            file_name="ethiopia_fi_projections_2024_2030.csv",
            mime="text/csv"
        )

def main():
    """Main application function"""
    dashboard = EthiopiaDashboard()
    
    # Sidebar navigation
    st.sidebar.markdown('<div class="ethiopia-flag"></div>', unsafe_allow_html=True)
    st.sidebar.title("🇪🇹 Navigation")
    
    page = st.sidebar.radio(
        "Select Page:",
        ["📊 Overview", "📈 Trends", "🔮 Forecasts", "🎯 Projections"]
    )
    
    # Page routing
    if page == "📊 Overview":
        dashboard.overview_page()
    elif page == "📈 Trends":
        dashboard.trends_page()
    elif page == "🔮 Forecasts":
        dashboard.forecasts_page()
    elif page == "🎯 Projections":
        dashboard.projections_page()
    
    # Sidebar information
    st.sidebar.markdown("---")
    st.sidebar.info("""
    **Data Coverage:**
    - Historical: 2012-2024
    - Forecasts: 2025-2027
    - Projections: 2024-2030
    
    **Dashboard Features:**
    - Interactive visualizations
    - Scenario analysis
    - Data export
    - Target tracking
    """)
    
    # File uploader for data
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📁 Upload Data")
    
    uploaded_file = st.sidebar.file_uploader(
        "Upload your CSV data",
        type=["csv"],
        help="Upload ethiopia_fi_unified_new.csv or other data files"
    )
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.sidebar.success(f"Uploaded: {uploaded_file.name}")
            st.sidebar.dataframe(df.head(3), width='stretch')
        except Exception as e:
            st.sidebar.error(f"Error: {e}")

if __name__ == "__main__":
    main()