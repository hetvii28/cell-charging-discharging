import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import random
import time
import numpy as np
from datetime import datetime, timedelta
import json

# Page configuration
st.set_page_config(
    page_title="⚡ Battery Management System",
    page_icon="🔋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .main {
        font-family: 'Inter', sans-serif;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Header styling */
    .header-container {
        background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);
        padding: 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    .header-title {
        font-size: 3rem;
        font-weight: 700;
        color: white;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
        margin: 0;
    }
    
    .header-subtitle {
        font-size: 1.2rem;
        color: rgba(255,255,255,0.9);
        margin-top: 0.5rem;
    }
    
    /* Card styling */
    .metric-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
        margin: 1rem 0;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.2);
        background: rgba(255, 255, 255, 0.15);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: white;
        margin: 0.5rem 0;
    }
    
    .metric-label {
        font-size: 1rem;
        color: rgba(255, 255, 255, 0.8);
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #2c3e50 0%, #3498db 100%);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(45deg, #ff6b6b, #ee5a24);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 25px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        width: 100%;
        box-shadow: 0 4px 15px rgba(238, 90, 36, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(238, 90, 36, 0.4);
        background: linear-gradient(45deg, #ee5a24, #ff6b6b);
    }
    
    /* Status indicators */
    .status-indicator {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
    }
    
    .status-normal { background: #2ecc71; color: white; }
    .status-warning { background: #f39c12; color: white; }
    .status-critical { background: #e74c3c; color: white; }
    
    /* Animation */
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    .pulse { animation: pulse 2s infinite; }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 0.5rem 1rem;
        color: white;
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(45deg, #4facfe, #00f2fe);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
def init_session_state():
    if 'cells_data' not in st.session_state:
        st.session_state.cells_data = {}
    if 'tasks_data' not in st.session_state:
        st.session_state.tasks_data = {}
    if 'simulation_data' not in st.session_state:
        st.session_state.simulation_data = []
    if 'is_simulating' not in st.session_state:
        st.session_state.is_simulating = False

init_session_state()

# Header
st.markdown("""
<div class="header-container">
    <h1 class="header-title">⚡ Battery Management System</h1>
    <p class="header-subtitle">Advanced Cell Monitoring & Task Management Platform</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 🔧 System Configuration")
    
    # Cell Configuration Section
    with st.expander("🔋 Cell Configuration", expanded=True):
        num_cells = st.slider("Number of Cells", 1, 10, 3)
        
        cell_configs = []
        for i in range(num_cells):
            col1, col2 = st.columns([2, 1])
            with col1:
                cell_type = st.selectbox(f"Cell {i+1}", ["lfp", "nmc"], key=f"cell_{i}")
            with col2:
                if st.button("🔄", key=f"refresh_{i}", help="Refresh cell data"):
                    st.rerun()
            cell_configs.append(cell_type)
        
        if st.button("🚀 Generate Battery Pack"):
            st.session_state.cells_data = {}
            for idx, cell_type in enumerate(cell_configs, start=1):
                cell_key = f"cell_{idx}_{cell_type}"
                voltage = 3.2 if cell_type == "lfp" else 3.6
                min_voltage = 2.8 if cell_type == "lfp" else 3.2
                max_voltage = 3.6 if cell_type == "lfp" else 4.0
                current = round(random.uniform(0.1, 5.0), 2)
                temp = round(random.uniform(25, 40), 1)
                capacity = round(voltage * current, 2)
                
                st.session_state.cells_data[cell_key] = {
                    "voltage": voltage,
                    "current": current,
                    "temp": temp,
                    "capacity": capacity,
                    "min_voltage": min_voltage,
                    "max_voltage": max_voltage,
                    "type": cell_type,
                    "timestamp": datetime.now()
                }
            st.success("✅ Battery pack generated successfully!")
            st.balloons()
    
    # Quick Stats
    if st.session_state.cells_data:
        st.markdown("### 📊 Quick Stats")
        total_cells = len(st.session_state.cells_data)
        avg_voltage = np.mean([cell['voltage'] for cell in st.session_state.cells_data.values()])
        total_capacity = sum([cell['capacity'] for cell in st.session_state.cells_data.values()])
        
        st.metric("Total Cells", total_cells)
        st.metric("Average Voltage", f"{avg_voltage:.2f}V")
        st.metric("Total Capacity", f"{total_capacity:.2f}Wh")

# Main content
if st.session_state.cells_data:
    # Create tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "🔋 Cell Monitor", "⚡ Task Manager", "📈 Analytics"])
    
    with tab1:
        # Key metrics row
        col1, col2, col3, col4 = st.columns(4)
        
        total_cells = len(st.session_state.cells_data)
        avg_voltage = np.mean([cell['voltage'] for cell in st.session_state.cells_data.values()])
        avg_temp = np.mean([cell['temp'] for cell in st.session_state.cells_data.values()])
        total_capacity = sum([cell['capacity'] for cell in st.session_state.cells_data.values()])
        
        metrics = [
            ("Total Cells", total_cells, "🔋"),
            ("Avg Voltage", f"{avg_voltage:.2f}V", "⚡"),
            ("Avg Temperature", f"{avg_temp:.1f}°C", "🌡️"),
            ("Total Capacity", f"{total_capacity:.2f}Wh", "💡")
        ]
        
        for col, (label, value, icon) in zip([col1, col2, col3, col4], metrics):
            with col:
                st.markdown(f"""
                <div class="metric-card">
                    <div style="text-align: center;">
                        <div style="font-size: 2rem; margin-bottom: 0.5rem;">{icon}</div>
                        <div class="metric-label">{label}</div>
                        <div class="metric-value">{value}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Charts section
        col1, col2 = st.columns(2)
        
        with col1:
            # Voltage distribution
            cell_names = list(st.session_state.cells_data.keys())
            voltages = [st.session_state.cells_data[cell]['voltage'] for cell in cell_names]
            cell_types = [st.session_state.cells_data[cell]['type'] for cell in cell_names]
            
            fig1 = px.bar(
                x=cell_names,
                y=voltages,
                color=cell_types,
                title="🔋 Cell Voltage Distribution",
                color_discrete_map={'lfp': '#2ecc71', 'nmc': '#3498db'},
                template='plotly_dark'
            )
            fig1.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='white',
                title_font_size=18,
                title_x=0.5
            )
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            # Temperature vs Current scatter
            temps = [st.session_state.cells_data[cell]['temp'] for cell in cell_names]
            currents = [st.session_state.cells_data[cell]['current'] for cell in cell_names]
            
            fig2 = px.scatter(
                x=temps,
                y=currents,
                color=cell_types,
                size=[20]*len(cell_names),
                title="🌡️ Temperature vs Current Analysis",
                labels={'x': 'Temperature (°C)', 'y': 'Current (A)'},
                color_discrete_map={'lfp': '#2ecc71', 'nmc': '#3498db'},
                template='plotly_dark'
            )
            fig2.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='white',
                title_font_size=18,
                title_x=0.5
            )
            st.plotly_chart(fig2, use_container_width=True)
        
        # System health overview
        st.markdown("### 🏥 System Health Overview")
        health_col1, health_col2, health_col3 = st.columns(3)
        
        # Calculate health metrics
        voltage_health = sum(1 for cell in st.session_state.cells_data.values() 
                           if cell['min_voltage'] <= cell['voltage'] <= cell['max_voltage'])
        temp_health = sum(1 for cell in st.session_state.cells_data.values() 
                         if cell['temp'] <= 35)
        
        with health_col1:
            voltage_percentage = (voltage_health / total_cells) * 100
            st.markdown(f"""
            <div class="metric-card">
                <h4 style="color: white; text-align: center;">⚡ Voltage Health</h4>
                <div style="text-align: center;">
                    <div style="font-size: 2rem; color: {'#2ecc71' if voltage_percentage > 80 else '#f39c12' if voltage_percentage > 60 else '#e74c3c'};">
                        {voltage_percentage:.0f}%
                    </div>
                    <p style="color: rgba(255,255,255,0.7);">{voltage_health}/{total_cells} cells normal</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with health_col2:
            temp_percentage = (temp_health / total_cells) * 100
            st.markdown(f"""
            <div class="metric-card">
                <h4 style="color: white; text-align: center;">🌡️ Thermal Health</h4>
                <div style="text-align: center;">
                    <div style="font-size: 2rem; color: {'#2ecc71' if temp_percentage > 80 else '#f39c12' if temp_percentage > 60 else '#e74c3c'};">
                        {temp_percentage:.0f}%
                    </div>
                    <p style="color: rgba(255,255,255,0.7);">{temp_health}/{total_cells} cells optimal</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with health_col3:
            overall_health = (voltage_percentage + temp_percentage) / 2
            st.markdown(f"""
            <div class="metric-card">
                <h4 style="color: white; text-align: center;">💚 Overall Health</h4>
                <div style="text-align: center;">
                    <div style="font-size: 2rem; color: {'#2ecc71' if overall_health > 80 else '#f39c12' if overall_health > 60 else '#e74c3c'};">
                        {overall_health:.0f}%
                    </div>
                    <p style="color: rgba(255,255,255,0.7);">System Status</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown("### 🔋 Individual Cell Monitoring")
        
        # Cell selector
        selected_cell = st.selectbox("Select Cell for Detailed View", list(st.session_state.cells_data.keys()))
        
        if selected_cell:
            cell_data = st.session_state.cells_data[selected_cell]
            
            # Cell info header
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"""
                <div class="metric-card">
                    <h4 style="color: #3498db; text-align: center;">Cell Type</h4>
                    <div style="text-align: center; font-size: 1.5rem; color: white; font-weight: bold;">
                        {cell_data['type'].upper()}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                status = "Normal" if cell_data['min_voltage'] <= cell_data['voltage'] <= cell_data['max_voltage'] else "Warning"
                status_color = "#2ecc71" if status == "Normal" else "#f39c12"
                st.markdown(f"""
                <div class="metric-card">
                    <h4 style="color: #e74c3c; text-align: center;">Status</h4>
                    <div style="text-align: center; font-size: 1.5rem; color: {status_color}; font-weight: bold;">
                        {status}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class="metric-card">
                    <h4 style="color: #9b59b6; text-align: center;">Current</h4>
                    <div style="text-align: center; font-size: 1.5rem; color: white; font-weight: bold;">
                        {cell_data['current']} A
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                st.markdown(f"""
                <div class="metric-card">
                    <h4 style="color: #f39c12; text-align: center;">Capacity</h4>
                    <div style="text-align: center; font-size: 1.5rem; color: white; font-weight: bold;">
                        {cell_data['capacity']} Wh
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            # Gauges
            col1, col2 = st.columns(2)
            
            with col1:
                # Voltage gauge
                fig_voltage = go.Figure(go.Indicator(
                    mode = "gauge+number+delta",
                    value = cell_data['voltage'],
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    title = {'text': "Voltage (V)", 'font': {'color': 'white', 'size': 20}},
                    delta = {'reference': (cell_data['min_voltage'] + cell_data['max_voltage'])/2},
                    gauge = {
                        'axis': {'range': [None, cell_data['max_voltage'] + 0.5], 'tickcolor': 'white'},
                        'bar': {'color': "#3498db"},
                        'steps': [
                            {'range': [0, cell_data['min_voltage']], 'color': "#e74c3c"},
                            {'range': [cell_data['min_voltage'], cell_data['max_voltage']], 'color': "#2ecc71"}
                        ],
                        'threshold': {
                            'line': {'color': "white", 'width': 4},
                            'thickness': 0.75,
                            'value': cell_data['max_voltage']
                        }
                    },
                    number = {'font': {'color': 'white', 'size': 30}}
                ))
                fig_voltage.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font_color='white',
                    height=350
                )
                st.plotly_chart(fig_voltage, use_container_width=True)
            
            with col2:
                # Temperature gauge
                fig_temp = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = cell_data['temp'],
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    title = {'text': "Temperature (°C)", 'font': {'color': 'white', 'size': 20}},
                    gauge = {
                        'axis': {'range': [None, 60], 'tickcolor': 'white'},
                        'bar': {'color': "#f39c12"},
                        'steps': [
                            {'range': [0, 30], 'color': "#2ecc71"},
                            {'range': [30, 45], 'color': "#f39c12"},
                            {'range': [45, 60], 'color': "#e74c3c"}
                        ]
                    },
                    number = {'font': {'color': 'white', 'size': 30}}
                ))
                fig_temp.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font_color='white',
                    height=350
                )
                st.plotly_chart(fig_temp, use_container_width=True)
        
        # All cells overview table
        st.markdown("### 📋 All Cells Overview")
        df_cells = pd.DataFrame.from_dict(st.session_state.cells_data, orient='index')
        df_cells['status'] = df_cells.apply(
            lambda row: '🟢 Normal' if row['min_voltage'] <= row['voltage'] <= row['max_voltage'] else '🟡 Warning',
            axis=1
        )
        
        # Format the dataframe for display
        display_df = df_cells[['type', 'voltage', 'current', 'temp', 'capacity', 'status']].copy()
        display_df.columns = ['Type', 'Voltage (V)', 'Current (A)', 'Temperature (°C)', 'Capacity (Wh)', 'Status']
        
        st.dataframe(
            display_df,
            use_container_width=True,
            height=400
        )
    
    with tab3:
        st.markdown("### ⚡ Task Management System")
        
        # Task creation form
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("#### ➕ Create New Task")
            
            with st.form("task_form"):
                task_type = st.selectbox("Task Type", ["CC_CV", "IDLE", "CC_CD"])
                
                if task_type == "CC_CV":
                    st.markdown("**CC_CV Parameters:**")
                    cc_input = st.text_input("CC Value", value="5A", help="Enter value with unit (e.g., '5A' or '10W')")
                    cv_voltage = st.number_input("CV Voltage (V)", value=3.6, step=0.1)
                    current = st.number_input("Current (A)", value=2.5, step=0.1)
                    capacity = st.number_input("Capacity", value=10.0, step=0.1)
                    time_seconds = st.number_input("Time (seconds)", value=3600, step=1)
                    
                    task_data = {
                        "task_type": "CC_CV",
                        "cc_cp": cc_input,
                        "cv_voltage": cv_voltage,
                        "current": current,
                        "capacity": capacity,
                        "time_seconds": time_seconds,
                        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                
                elif task_type == "IDLE":
                    st.markdown("**IDLE Parameters:**")
                    time_seconds = st.number_input("Time (seconds)", value=1800, step=1)
                    
                    task_data = {
                        "task_type": "IDLE",
                        "time_seconds": time_seconds,
                        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                
                elif task_type == "CC_CD":
                    st.markdown("**CC_CD Parameters:**")
                    cc_input = st.text_input("CC Value", value="5A", help="Enter value with unit (e.g., '5A' or '10W')")
                    voltage = st.number_input("Voltage (V)", value=3.2, step=0.1)
                    capacity = st.number_input("Capacity", value=10.0, step=0.1)
                    time_seconds = st.number_input("Time (seconds)", value=3600, step=1)
                    
                    task_data = {
                        "task_type": "CC_CD",
                        "cc_cp": cc_input,
                        "voltage": voltage,
                        "capacity": capacity,
                        "time_seconds": time_seconds,
                        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                
                if st.form_submit_button("🚀 Add Task", use_container_width=True):
                    task_key = f"task_{len(st.session_state.tasks_data) + 1}"
                    st.session_state.tasks_data[task_key] = task_data
                    st.success(f"✅ Task {task_key} added successfully!")
                    st.balloons()
        
        with col2:
            st.markdown("#### 📋 Task Queue")
            
            if st.session_state.tasks_data:
                # Task overview metrics
                task_types = [task['task_type'] for task in st.session_state.tasks_data.values()]
                task_counts = pd.Series(task_types).value_counts()
                
                # Task distribution pie chart
                fig_tasks = px.pie(
                    values=task_counts.values,
                    names=task_counts.index,
                    title="📊 Task Distribution",
                    color_discrete_sequence=['#3498db', '#2ecc71', '#f39c12'],
                    template='plotly_dark'
                )
                fig_tasks.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='white',
                    title_x=0.5
                )
                st.plotly_chart(fig_tasks, use_container_width=True)
                
                # Clear all tasks button
                if st.button("🗑️ Clear All Tasks"):
                    st.session_state.tasks_data = {}
                    st.success("All tasks cleared!")
                    st.rerun()
            else:
                st.info("No tasks in queue. Create your first task!")
        
        # Tasks table
        if st.session_state.tasks_data:
            st.markdown("#### 📝 Task Details")
            df_tasks = pd.DataFrame.from_dict(st.session_state.tasks_data, orient='index')
            st.dataframe(df_tasks, use_container_width=True, height=300)
    
    with tab4:
        st.markdown("### 📈 Advanced Analytics")
        
        # Simulation controls
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            if st.button("▶️ Start Simulation", use_container_width=True):
                st.session_state.is_simulating = True
        
        with col2:
            if st.button("⏹️ Stop Simulation", use_container_width=True):
                st.session_state.is_simulating = False
        
        with col3:
            simulation_speed = st.slider("Simulation Speed", 0.1, 2.0, 1.0, 0.1)
        
        # Real-time charts placeholder
        if st.session_state.is_simulating:
            chart_placeholder = st.empty()
            metrics_placeholder = st.empty()
            
            # Simulate real-time data
            for i in range(100):
                if not st.session_state.is_simulating:
                    break
                
                # Generate time series data
                current_time = datetime.now() + timedelta(seconds=i)
                data_point = {
                    'time': current_time,
                    'timestamp': i
                }
                
                for cell_key, cell_data in st.session_state.cells_data.items():
                    # Simulate voltage fluctuation
                    base_voltage = cell_data['voltage']
                    voltage_noise = random.uniform(-0.05, 0.05)
                    data_point[f'{cell_key}_voltage'] = base_voltage + voltage_noise
                    
                    # Simulate temperature fluctuation
                    base_temp = cell_data['temp']
                    temp_noise = random.uniform(-1, 1)
                    data_point[f'{cell_key}_temp'] = base_temp + temp_noise
                
                st.session_state.simulation_data.append(data_point)
                
                # Keep only last 50 points
                if len(st.session_state.simulation_data) > 50:
                    st.session_state.simulation_data.pop(0)
                
                # Create real-time chart
                if len(st.session_state.simulation_data) > 1:
                    df_sim = pd.DataFrame(st.session_state.simulation_data)
                    
                    fig_realtime = go.Figure()
                    
                    colors = ['#3498db', '#2ecc71', '#f39c12', '#e74c3c', '#9b59b6']
                    for idx, cell_key in enumerate(st.session_state.cells_data.keys()):
                        voltage_col = f'{cell_key}_voltage'
                        if voltage_col in df_sim.columns:
                            fig_realtime.add_trace(go.Scatter(
                                x=df_sim['timestamp'],
                                y=df_sim[voltage_col],
                                mode='lines',
                                name=cell_key,
                                line=dict(color=colors[idx % len(colors)], width=3)
                            ))
                    
                    fig_
