import streamlit as st
import pandas as pd
import random
import time
from datetime import datetime
import numpy as np
import plotly.graph_objects as go


# Page configuration
st.set_page_config(
    page_title="⚡ Battery Cell Testing Dashboard",
    page_icon="🔋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
    }
    
    .metric-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
        box-shadow: 0 8px 20px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
    }
    
    .cell-status {
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: bold;
        margin: 0.2rem;
        display: inline-block;
    }
    
    .status-good { background: #4CAF50; color: white; }
    .status-warning { background: #FF9800; color: white; }
    .status-critical { background: #F44336; color: white; }
    
    .sidebar-section {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid #667eea;
    }
    
    .stSelectbox > div > div {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'cells_data' not in st.session_state:
    st.session_state.cells_data = {}
if 'bench_configured' not in st.session_state:
    st.session_state.bench_configured = False
if 'live_monitoring' not in st.session_state:
    st.session_state.live_monitoring = False

# Header
st.markdown("""
<div class="main-header">
    <h1>⚡ Battery Cell Testing Dashboard</h1>
    <p>Advanced Battery Management System for Cell Testing & Monitoring</p>
</div>
""", unsafe_allow_html=True)

# Sidebar configuration
with st.sidebar:
    st.markdown("### 🔧 Bench Configuration")
    
    with st.container():
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        bench_name = st.text_input("🏭 Bench Name", value="Test Bench Alpha", key="bench_name")
        
        type_cell = st.selectbox(
            "🔋 Default Cell Type",
            options=["nmc", "lfp"],
            format_func=lambda x: f"{'NMC (Nickel Manganese Cobalt)' if x == 'nmc' else 'LFP (Lithium Iron Phosphate)'}"
        )
        
        group_number = st.number_input("👥 Group Number", min_value=1, max_value=100, value=1)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Cell type specifications
    if type_cell == "lfp":
        nominal, min_voltage, max_voltage = 3.2, 2.8, 3.6
        cell_color = "#FF6B6B"
    else:  # nmc
        nominal, min_voltage, max_voltage = 3.6, 3.4, 4.8
        cell_color = "#4ECDC4"
    
    st.markdown("### ⚙️ Cell Configuration")
    with st.container():
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        num_cells = st.slider("Number of Cells", 1, 16, 8)
        
        if st.button("🚀 Configure Test Bench", type="primary"):
            st.session_state.bench_configured = True
            st.session_state.cells_data = {}
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# Main dashboard
if st.session_state.bench_configured:
    
    # Cell configuration section
    if not st.session_state.cells_data:
        st.markdown("## 🔋 Cell Setup")
        
        with st.form("cell_configuration"):
            cols = st.columns(4)
            cell_configs = []
            
            for i in range(num_cells):
                col_idx = i % 4
                with cols[col_idx]:
                    st.markdown(f"**Cell {i+1}**")
                    cell_type = st.selectbox(
                        f"Type",
                        options=["lfp", "nmc"],
                        key=f"cell_type_{i}",
                        index=0 if type_cell == "lfp" else 1
                    )
                    current = st.number_input(
                        f"Current (A)",
                        min_value=0.1,
                        max_value=50.0,
                        value=2.5,
                        step=0.1,
                        key=f"current_{i}"
                    )
                    cell_configs.append((cell_type, current))
            
            if st.form_submit_button("⚡ Initialize Cells", type="primary"):
                cells_data = {}
                for idx, (cell_type, current) in enumerate(cell_configs, start=1):
                    cell_key = f"cell_{idx}_{cell_type}"
                    
                    if cell_type == "lfp":
                        voltage = 3.2
                        min_v, max_v = 2.8, 3.6
                    else:  # nmc
                        voltage = 3.6
                        min_v, max_v = 3.4, 4.8
                    
                    temp = round(random.uniform(25, 40), 1)
                    capacity = round(voltage * current, 2)
                    
                    cells_data[cell_key] = {
                        "voltage": voltage,
                        "current": current,
                        "temp": temp,
                        "capacity": capacity,
                        "max_voltage": max_v,
                        "min_voltage": min_v,
                        "status": "Normal",
                        "timestamp": datetime.now(),
                        "cycle_count": 0,
                        "health": random.uniform(85, 100)
                    }
                
                st.session_state.cells_data = cells_data
                st.rerun()
    
    else:
        # Dashboard with live data
        col1, col2, col3, col4 = st.columns(4)
        
        # Calculate summary metrics
        total_cells = len(st.session_state.cells_data)
        avg_voltage = np.mean([cell['voltage'] for cell in st.session_state.cells_data.values()])
        total_capacity = sum([cell['capacity'] for cell in st.session_state.cells_data.values()])
        avg_temp = np.mean([cell['temp'] for cell in st.session_state.cells_data.values()])
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <h3>🔋 Total Cells</h3>
                <h1>{total_cells}</h1>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <h3>⚡ Avg Voltage</h3>
                <h1>{avg_voltage:.2f}V</h1>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <h3>🔥 Total Capacity</h3>
                <h1>{total_capacity:.1f}Wh</h1>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <h3>🌡️ Avg Temperature</h3>
                <h1>{avg_temp:.1f}°C</h1>
            </div>
            """, unsafe_allow_html=True)
        
        # Live monitoring toggle
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("## 📊 Real-Time Cell Monitoring")
        with col2:
            if st.button("🔄 Toggle Live Monitoring"):
                st.session_state.live_monitoring = not st.session_state.live_monitoring
        
        # Create visualizations
        col1, col2 = st.columns(2)
        
        with col1:
            # Voltage comparison chart
            fig_voltage = go.Figure()
            
            cell_names = list(st.session_state.cells_data.keys())
            voltages = [st.session_state.cells_data[cell]['voltage'] for cell in cell_names]
            colors = ['#FF6B6B' if 'lfp' in cell else '#4ECDC4' for cell in cell_names]
            
            fig_voltage.add_trace(go.Bar(
                x=cell_names,
                y=voltages,
                marker_color=colors,
                text=[f"{v:.2f}V" for v in voltages],
                textposition='auto',
                hovertemplate="<b>%{x}</b><br>Voltage: %{y:.2f}V<extra></extra>"
            ))
            
            fig_voltage.update_layout(
                title="Cell Voltage Comparison",
                xaxis_title="Cell ID",
                yaxis_title="Voltage (V)",
                showlegend=False,
                height=400,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            
            st.plotly_chart(fig_voltage, use_container_width=True)
        
        with col2:
            # Temperature and capacity scatter plot
            temps = [st.session_state.cells_data[cell]['temp'] for cell in cell_names]
            capacities = [st.session_state.cells_data[cell]['capacity'] for cell in cell_names]
            
            fig_scatter = go.Figure()
            
            fig_scatter.add_trace(go.Scatter(
                x=temps,
                y=capacities,
                mode='markers+text',
                marker=dict(
                    size=15,
                    color=colors,
                    line=dict(width=2, color='white')
                ),
                text=[cell.split('_')[1] for cell in cell_names],
                textposition="middle center",
                hovertemplate="<b>%{text}</b><br>Temperature: %{x:.1f}°C<br>Capacity: %{y:.2f}Wh<extra></extra>"
            ))
            
            fig_scatter.update_layout(
                title="Temperature vs Capacity",
                xaxis_title="Temperature (°C)",
                yaxis_title="Capacity (Wh)",
                height=400,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            
            st.plotly_chart(fig_scatter, use_container_width=True)
        
        # Cell status table
        st.markdown("## 📋 Detailed Cell Status")
        
        # Create DataFrame for display
        df_data = []
        for cell_id, data in st.session_state.cells_data.items():
            status = "Normal"
            if data['voltage'] >= data['max_voltage'] * 0.95:
                status = "High Voltage"
            elif data['voltage'] <= data['min_voltage'] * 1.05:
                status = "Low Voltage"
            elif data['temp'] > 35:
                status = "High Temperature"
            
            df_data.append({
                "Cell ID": cell_id,
                "Type": cell_id.split('_')[2].upper(),
                "Voltage (V)": f"{data['voltage']:.2f}",
                "Current (A)": f"{data['current']:.2f}",
                "Temperature (°C)": f"{data['temp']:.1f}",
                "Capacity (Wh)": f"{data['capacity']:.2f}",
                "Health (%)": f"{data['health']:.1f}",
                "Status": status
            })
        
        df = pd.DataFrame(df_data)
        
        # Color-code the dataframe
        def color_status(val):
            if val == "Normal":
                return 'background-color: #d4edda'
            elif val in ["High Voltage", "High Temperature"]:
                return 'background-color: #fff3cd'
            else:
                return 'background-color: #f8d7da'
        
        styled_df = df.style.applymap(color_status, subset=['Status'])
        st.dataframe(styled_df, use_container_width=True, hide_index=True)
        
        # Control buttons
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🔄 Refresh Data", type="secondary"):
                # Simulate data updates
                for cell_id in st.session_state.cells_data:
                    st.session_state.cells_data[cell_id]['temp'] = round(random.uniform(25, 40), 1)
                    st.session_state.cells_data[cell_id]['voltage'] += random.uniform(-0.1, 0.1)
                    st.session_state.cells_data[cell_id]['health'] += random.uniform(-1, 0.5)
                st.rerun()
        
        with col2:
            if st.button("📊 Export Data", type="secondary"):
                csv = df.to_csv(index=False)
                st.download_button(
                    label="📁 Download CSV",
                    data=csv,
                    file_name=f"battery_test_{bench_name}_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                    mime="text/csv"
                )
        
        with col3:
            if st.button("🚨 Emergency Stop", type="secondary"):
                st.error("⚠️ Emergency stop activated! All cell testing halted.")
                st.balloons()
        
        # Live monitoring section
        if st.session_state.live_monitoring:
            st.markdown("## 🔴 Live Monitoring Active")
            with st.empty():
                for i in range(10):
                    # Simulate real-time updates
                    live_data = []
                    for cell_id, data in st.session_state.cells_data.items():
                        voltage = data['voltage'] + random.uniform(-0.05, 0.05)
                        temp = data['temp'] + random.uniform(-1, 1)
                        live_data.append({
                            'Cell': cell_id.split('_')[1],
                            'Voltage': voltage,
                            'Temperature': temp,
                            'Time': datetime.now().strftime('%H:%M:%S')
                        })
                    
                    live_df = pd.DataFrame(live_data)
                    st.dataframe(live_df, use_container_width=True)
                    time.sleep(1)

else:
    # Welcome screen
    st.markdown("""
    ## 🎯 Welcome to the Battery Testing System
    
    Configure your test bench using the sidebar to get started:
    
    1. **Enter bench details** - Name and group information
    2. **Select cell type** - Choose between NMC or LFP chemistry
    3. **Set number of cells** - Configure your test setup
    4. **Click 'Configure Test Bench'** - Initialize the system
    
    ### 🔋 Supported Cell Types:
    - **NMC (Nickel Manganese Cobalt)**: 3.6V nominal, 3.4-4.8V range
    - **LFP (Lithium Iron Phosphate)**: 3.2V nominal, 2.8-3.6V range
    
    ### 📊 Features:
    - Real-time monitoring dashboard
    - Interactive data visualization
    - Cell health tracking
    - Data export capabilities
    - Emergency safety controls
    """)

# Footer
st.markdown("---")
st.markdown("⚡ **Battery Cell Testing Dashboard** | Built with Streamlit & Plotly | 🔋 Advanced Battery Management System")
