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
import io
import base64

# Page configuration
st.set_page_config(
    page_title="🔋 Advanced Battery Management System",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark theme and professional styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Main app styling */
    .main {
        font-family: 'Inter', sans-serif;
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f0f23 100%);
        color: #ffffff;
    }
    
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f0f23 100%);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #2a2a3e 0%, #1e1e2f 100%);
        border-right: 2px solid #3a3a5c;
    }
    
    /* Header styling */
    .header-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 15px 35px rgba(0,0,0,0.4);
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    .header-title {
        font-size: 3.5rem;
        font-weight: 700;
        color: white;
        text-shadow: 0 4px 8px rgba(0,0,0,0.3);
        margin: 0;
        background: linear-gradient(45deg, #ffffff, #e0e6ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .header-subtitle {
        font-size: 1.3rem;
        color: rgba(255,255,255,0.9);
        margin-top: 0.5rem;
        font-weight: 400;
    }
    
    /* Metric cards */
    .metric-card {
        background: linear-gradient(145deg, #2a2a3e, #1e1e2f);
        border: 1px solid #3a3a5c;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
        margin: 1rem 0;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #667eea, #764ba2);
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 40px rgba(102, 126, 234, 0.2);
        border-color: #667eea;
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #ffffff;
        margin: 0.5rem 0;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #b0b0c4;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 500;
    }
    
    .metric-icon {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
        opacity: 0.8;
    }
    
    /* Cell cards */
    .cell-card {
        background: linear-gradient(145deg, #2a2a3e, #1e1e2f);
        border: 1px solid #3a3a5c;
        padding: 1.2rem;
        border-radius: 12px;
        margin: 0.5rem 0;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
    }
    
    .cell-card:hover {
        border-color: #667eea;
        box-shadow: 0 12px 25px rgba(102, 126, 234, 0.15);
    }
    
    /* Task cards */
    .task-card {
        background: linear-gradient(145deg, #2a2a3e, #1e1e2f);
        border: 1px solid #3a3a5c;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #667eea;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 10px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        width: 100%;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    
    /* Input field styling */
    .stSelectbox > div > div, .stNumberInput > div > div > input, .stTextInput > div > div > input {
        background: #2a2a3e !important;
        border: 1px solid #3a3a5c !important;
        border-radius: 8px !important;
        color: #ffffff !important;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .stSelectbox > div > div:focus-within, 
    .stNumberInput > div > div:focus-within, 
    .stTextInput > div > div:focus-within {
        border-color: #667eea !important;
        box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2) !important;
    }
    
    /* Status indicators */
    .status-normal { 
        background: linear-gradient(135deg, #2ecc71, #27ae60);
        color: white; 
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .status-warning { 
        background: linear-gradient(135deg, #f39c12, #e67e22);
        color: white; 
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .status-critical { 
        background: linear-gradient(135deg, #e74c3c, #c0392b);
        color: white; 
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(42, 42, 62, 0.5);
        padding: 0.5rem;
        border-radius: 12px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 8px;
        padding: 0.8rem 1.5rem;
        color: #b0b0c4;
        font-weight: 500;
        border: 1px solid transparent;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        border-color: rgba(255,255,255,0.2);
    }
    
    /* Simulation status */
    .simulation-active {
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(102, 126, 234, 0.7); }
        70% { box-shadow: 0 0 0 15px rgba(102, 126, 234, 0); }
        100% { box-shadow: 0 0 0 0 rgba(102, 126, 234, 0); }
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #1a1a2e;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea, #764ba2);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #764ba2, #667eea);
    }
    
    /* Dataframe styling */
    .stDataFrame {
        background: #2a2a3e;
        border-radius: 10px;
        overflow: hidden;
        border: 1px solid #3a3a5c;
    }
    
    /* Form styling */
    .stForm {
        background: rgba(42, 42, 62, 0.3);
        border: 1px solid #3a3a5c;
        border-radius: 12px;
        padding: 1rem;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: rgba(42, 42, 62, 0.5) !important;
        border-radius: 8px !important;
        color: white !important;
    }
    
    /* Progress bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(135deg, #667eea, #764ba2);
    }
</style>
""", unsafe_allow_html=True)

# Cell type configurations
CELL_TYPES = {
    "lfp": {
        "name": "LiFePO4",
        "nominal_voltage": 3.2,
        "min_voltage": 2.8,
        "max_voltage": 3.6,
        "color": "#2ecc71"
    },
    "nmc": {
        "name": "Li-NMC",
        "nominal_voltage": 3.7,
        "min_voltage": 3.0,
        "max_voltage": 4.2,
        "color": "#3498db"
    },
    "liion": {
        "name": "Li-ion",
        "nominal_voltage": 3.6,
        "min_voltage": 3.2,
        "max_voltage": 4.0,
        "color": "#9b59b6"
    },
    "lto": {
        "name": "Li4Ti5O12",
        "nominal_voltage": 2.4,
        "min_voltage": 1.5,
        "max_voltage": 2.8,
        "color": "#f39c12"
    }
}

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
    if 'simulation_start_time' not in st.session_state:
        st.session_state.simulation_start_time = None
    if 'task_queue' not in st.session_state:
        st.session_state.task_queue = {}

init_session_state()

# Helper functions
def generate_cell_data(cell_type, custom_params=None):
    """Generate realistic cell data based on type"""
    config = CELL_TYPES[cell_type]
    
    if custom_params:
        voltage = custom_params.get('voltage', config['nominal_voltage'])
        current = custom_params.get('current', round(random.uniform(0.1, 5.0), 2))
        temp = custom_params.get('temp', round(random.uniform(25, 40), 1))
    else:
        voltage = config['nominal_voltage']
        current = round(random.uniform(0.1, 5.0), 2)
        temp = round(random.uniform(25, 40), 1)
    
    capacity = round(voltage * current, 2)
    
    return {
        "type": cell_type,
        "voltage": voltage,
        "current": current,
        "temp": temp,
        "capacity": capacity,
        "min_voltage": config['min_voltage'],
        "max_voltage": config['max_voltage'],
        "nominal_voltage": config['nominal_voltage'],
        "timestamp": datetime.now(),
        "status": "normal"
    }

def simulate_battery_behavior(cell_data, task_data, elapsed_time):
    """Simulate realistic battery behavior during tasks"""
    new_data = cell_data.copy()
    task_type = task_data['task_type']
    
    if task_type == "CC_CV":
        # Constant Current - Constant Voltage charging
        cv_voltage = task_data['cv_voltage']
        current = task_data['current']
        
        # CC phase: voltage rises
        if new_data['voltage'] < cv_voltage * 0.95:
            voltage_increase = 0.01 * (current / 2.0)
            new_data['voltage'] = min(new_data['voltage'] + voltage_increase, cv_voltage)
            new_data['current'] = current
        else:
            # CV phase: current tapers
            new_data['voltage'] = cv_voltage
            new_data['current'] = max(current * 0.95, 0.1)
        
        # Temperature rise during charging
        new_data['temp'] = min(new_data['temp'] + random.uniform(0.1, 0.3), 45)
        
    elif task_type == "CC_CD":
        # Constant Current discharge
        current = task_data.get('current', 2.0)
        voltage_drop = 0.008 * (current / 2.0)
        new_data['voltage'] = max(new_data['voltage'] - voltage_drop, new_data['min_voltage'])
        new_data['current'] = -current  # Negative for discharge
        
        # Temperature rise during discharge
        new_data['temp'] = min(new_data['temp'] + random.uniform(0.05, 0.2), 40)
        
    elif task_type == "IDLE":
        # Rest period - parameters stabilize
        new_data['current'] = 0.0
        # Temperature moves toward ambient (25°C)
        if new_data['temp'] > 25:
            new_data['temp'] = max(new_data['temp'] - 0.5, 25)
        
        # Voltage settles slightly
        target_voltage = new_data['nominal_voltage']
        if abs(new_data['voltage'] - target_voltage) > 0.01:
            diff = target_voltage - new_data['voltage']
            new_data['voltage'] += diff * 0.1
    
    # Update capacity
    new_data['capacity'] = round(abs(new_data['voltage'] * new_data['current']), 2)
    
    # Update status based on voltage
    if new_data['voltage'] < new_data['min_voltage'] * 1.1:
        new_data['status'] = "critical"
    elif new_data['voltage'] > new_data['max_voltage'] * 0.9:
        new_data['status'] = "warning"
    else:
        new_data['status'] = "normal"
    
    return new_data

def export_data(data, filename, format_type):
    """Export data in various formats"""
    if format_type == "CSV":
        df = pd.DataFrame(data)
        return df.to_csv(index=False)
    elif format_type == "JSON":
        return json.dumps(data, indent=2, default=str)
    elif format_type == "Excel":
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            if isinstance(data, list):
                df = pd.DataFrame(data)
                df.to_excel(writer, sheet_name='Data', index=False)
            else:
                for sheet_name, sheet_data in data.items():
                    df = pd.DataFrame(sheet_data)
                    df.to_excel(writer, sheet_name=sheet_name, index=False)
        return output.getvalue()

# Header
st.markdown("""
<div class="header-container">
    <h1 class="header-title">⚡ Advanced Battery Management System</h1>
    <p class="header-subtitle">Professional Battery Testing & Analysis Platform</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### ⚙️ System Configuration")
    
    # Cell Configuration
    with st.expander("🔋 Cell Configuration", expanded=True):
        st.markdown("#### Add New Cell")
        
        col1, col2 = st.columns(2)
        with col1:
            cell_type = st.selectbox(
                "Cell Type",
                list(CELL_TYPES.keys()),
                format_func=lambda x: f"{CELL_TYPES[x]['name']} ({x.upper()})"
            )
        
        with col2:
            cell_count = st.number_input("Quantity", 1, 10, 1)
        
        # Custom parameters
        st.markdown("#### Custom Parameters (Optional)")
        use_custom = st.checkbox("Use custom parameters")
        
        custom_params = {}
        if use_custom:
            col1, col2 = st.columns(2)
            with col1:
                custom_params['voltage'] = st.number_input(
                    "Voltage (V)", 
                    value=CELL_TYPES[cell_type]['nominal_voltage'],
                    step=0.1
                )
                custom_params['current'] = st.number_input("Current (A)", value=2.5, step=0.1)
            with col2:
                custom_params['temp'] = st.number_input("Temperature (°C)", value=25.0, step=0.1)
        
        if st.button("➕ Add Cells", use_container_width=True):
            for i in range(cell_count):
                cell_key = f"cell_{len(st.session_state.cells_data) + 1}_{cell_type}"
                st.session_state.cells_data[cell_key] = generate_cell_data(
                    cell_type, 
                    custom_params if use_custom else None
                )
            st.success(f"✅ Added {cell_count} {CELL_TYPES[cell_type]['name']} cell(s)!")
            st.rerun()
    
    # Quick actions
    if st.session_state.cells_data:
        st.markdown("#### 🎯 Quick Actions")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Update All", use_container_width=True):
                for key in st.session_state.cells_data:
                    cell_type = st.session_state.cells_data[key]['type']
                    st.session_state.cells_data[key].update(generate_cell_data(cell_type))
                st.success("All cells updated!")
                st.rerun()
        
        with col2:
            if st.button("🗑️ Clear All", use_container_width=True):
                st.session_state.cells_data = {}
                st.session_state.tasks_data = {}
                st.session_state.task_queue = {}
                st.success("All data cleared!")
                st.rerun()
    
    # System status
    if st.session_state.cells_data:
        st.markdown("#### 📊 System Status")
        total_cells = len(st.session_state.cells_data)
        active_tasks = len(st.session_state.tasks_data)
        
        st.metric("Total Cells", total_cells)
        st.metric("Active Tasks", active_tasks)
        
        if st.session_state.is_simulating:
            st.markdown('<div class="status-normal simulation-active">🔴 SIMULATION RUNNING</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="status-normal">⚪ SYSTEM IDLE</div>', unsafe_allow_html=True)

# Main content
if st.session_state.cells_data:
    # Create tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Dashboard", 
        "🔋 Cell Management", 
        "⚡ Task Management", 
        "🔬 Real-time Simulation", 
        "📈 Data Analysis"
    ])
    
    with tab1:
        # System overview metrics
        col1, col2, col3, col4 = st.columns(4)
        
        total_cells = len(st.session_state.cells_data)
        avg_voltage = np.mean([cell['voltage'] for cell in st.session_state.cells_data.values()])
        avg_temp = np.mean([cell['temp'] for cell in st.session_state.cells_data.values()])
        total_power = sum([abs(cell['voltage'] * cell['current']) for cell in st.session_state.cells_data.values()])
        
        metrics_data = [
            ("Total Cells", total_cells, "🔋", "#3498db"),
            ("Avg Voltage", f"{avg_voltage:.2f}V", "⚡", "#2ecc71"),
            ("Avg Temperature", f"{avg_temp:.1f}°C", "🌡️", "#f39c12"),
            ("Total Power", f"{total_power:.2f}W", "💡", "#9b59b6")
        ]
        
        for col, (label, value, icon, color) in zip([col1, col2, col3, col4], metrics_data):
            with col:
                st.markdown(f"""
                <div class="metric-card">
                    <div style="text-align: center;">
                        <div class="metric-icon" style="color: {color};">{icon}</div>
                        <div class="metric-label">{label}</div>
                        <div class="metric-value">{value}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        # System health overview
        st.markdown("### 🏥 System Health Analysis")
        
        health_col1, health_col2, health_col3 = st.columns(3)
        
        # Calculate health metrics
        voltage_health = sum(1 for cell in st.session_state.cells_data.values() 
                           if cell['min_voltage'] <= cell['voltage'] <= cell['max_voltage'])
        temp_health = sum(1 for cell in st.session_state.cells_data.values() 
                         if cell['temp'] <= 35)
        status_health = sum(1 for cell in st.session_state.cells_data.values() 
                          if cell['status'] == 'normal')
        
        health_metrics = [
            ("Voltage Health", voltage_health, total_cells, "⚡"),
            ("Thermal Health", temp_health, total_cells, "🌡️"),
            ("Overall Health", status_health, total_cells, "💚")
        ]
        
        for col, (label, healthy, total, icon) in zip([health_col1, health_col2, health_col3], health_metrics):
            with col:
                percentage = (healthy / total) * 100
                color = "#2ecc71" if percentage > 80 else "#f39c12" if percentage > 60 else "#e74c3c"
                
                st.markdown(f"""
                <div class="metric-card">
                    <div style="text-align: center;">
                        <div class="metric-icon">{icon}</div>
                        <div class="metric-label">{label}</div>
                        <div class="metric-value" style="color: {color};">{percentage:.0f}%</div>
                        <div style="color: #b0b0c4; font-size: 0.9rem;">{healthy}/{total} cells optimal</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        # Quick visualization
        st.markdown("### 📊 System Overview Charts")
        
        chart_col1, chart_col2 = st.columns(2)
        
        with chart_col1:
            # Cell type distribution
            cell_types = [cell['type'] for cell in st.session_state.cells_data.values()]
            type_counts = pd.Series(cell_types).value_counts()
            
            fig_types = px.pie(
                values=type_counts.values,
                names=[CELL_TYPES[t]['name'] for t in type_counts.index],
                title="🔋 Cell Type Distribution",
                color_discrete_sequence=['#3498db', '#2ecc71', '#9b59b6', '#f39c12'],
                template='plotly_dark'
            )
            fig_types.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='white'
            )
            st.plotly_chart(fig_types, use_container_width=True)
        
        with chart_col2:
            # Voltage distribution
            cell_names = list(st.session_state.cells_data.keys())
            voltages = [st.session_state.cells_data[cell]['voltage'] for cell in cell_names]
            colors = [CELL_TYPES[st.session_state.cells_data[cell]['type']]['color'] for cell in cell_names]
            
            fig_voltage = go.Figure(data=[
                go.Bar(x=cell_names, y=voltages, marker_color=colors, name="Voltage")
            ])
            fig_voltage.update_layout(
                title="⚡ Cell Voltage Overview",
                xaxis_title="Cells",
                yaxis_title="Voltage (V)",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='white',
                template='plotly_dark'
            )
            st.plotly_chart(fig_voltage, use_container_width=True)
    
    with tab2:
        st.markdown("### 🔋 Individual Cell Management")
        
        # Cell management interface
        for cell_key, cell_data in st.session_state.cells_data.items():
            with st.container():
                st.markdown(f"""
                <div class="cell-card">
                    <div style="display: flex; justify-content: between; align-items: center; margin-bottom: 1rem;">
                        <h4 style="color: {CELL_TYPES[cell_data['type']]['color']; margin: 0;">
                            {cell_key} - {CELL_TYPES[cell_data['type']]['name']}
                        </h4>
                        <div class="status-{cell_data['status']}">{cell_data['status'].upper()}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Cell parameters in columns
                col1, col2, col3, col4, col5 = st.columns(5)
                
                with col1:
                    st.metric("Voltage", f"{cell_data['voltage']:.2f}V", f"Range: {cell_data['min_voltage']}-{cell_data['max_voltage']}V")
                
                with col2:
                    st.metric("Current", f"{cell_data['current']:.2f}A")
                
                with col3:
                    st.metric("Temperature", f"{cell_data['temp']:.1f}°C")
                
                with col4:
                    st.metric("Capacity", f"{cell_data['capacity']:.2f}Wh")
                
                with col5:
                    col_a, col_b = st.columns(2)
                    with col_a:
                        if st.button("🔄", key=f"refresh_{cell_key}", help="Randomize cell data"):
                            st.session_state.cells_data[cell_key].update(
                                generate_cell_data(cell_data['type'])
                            )
                            st.rerun()
                    with col_b:
                        if st.button("🗑️", key=f"delete_{cell_key}", help="Remove cell"):
                            del st.session_state.cells_data[cell_key]
                            st.rerun()
                
                st.markdown("---")
    
    with tab3:
        st.markdown("### ⚡ Task Management System")
