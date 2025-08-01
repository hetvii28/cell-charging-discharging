import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import random
import time
from datetime import datetime, timedelta
import json

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Battery Management System | Professional Dashboard",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# DARK THEME STYLING
# ============================================================================

dark_theme_css = """
<style>
    /* Import modern fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Root variables for consistent theming */
    :root {
        --bg-primary: #121212;
        --bg-secondary: #1e1e1e;
        --bg-tertiary: #2d2d2d;
        --text-primary: #ffffff;
        --text-secondary: #b3b3b3;
        --accent-cyan: #00bcd4;
        --accent-teal: #009688;
        --accent-lime: #cddc39;
        --accent-orange: #ff9800;
        --border-color: #404040;
        --hover-bg: #333333;
    }
    
    /* Main app styling */
    .stApp {
        background-color: var(--bg-primary);
        color: var(--text-primary);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Fixed header */
    .main-header {
        position: sticky;
        top: 0;
        z-index: 1000;
        background: linear-gradient(135deg, var(--bg-secondary) 0%, var(--bg-tertiary) 100%);
        padding: 1.5rem 2rem;
        margin: -1rem -1rem 2rem -1rem;
        border-bottom: 2px solid var(--accent-cyan);
        box-shadow: 0 4px 20px rgba(0, 188, 212, 0.1);
    }
    
    .main-header h1 {
        margin: 0;
        font-size: 2.2rem;
        font-weight: 600;
        background: linear-gradient(45deg, var(--accent-cyan), var(--accent-teal));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .main-header p {
        margin: 0.5rem 0 0 0;
        color: var(--text-secondary);
        font-size: 1rem;
        font-weight: 300;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: var(--bg-secondary);
        border-right: 1px solid var(--border-color);
    }
    
    .css-1d391kg .css-17eq0hr {
        background-color: var(--bg-secondary);
        color: var(--text-primary);
    }
    
    /* Navigation items */
    .nav-item {
        background: var(--bg-tertiary);
        border: 1px solid var(--border-color);
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .nav-item:hover {
        background: var(--hover-bg);
        border-color: var(--accent-cyan);
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(0, 188, 212, 0.2);
    }
    
    .nav-item.active {
        background: linear-gradient(135deg, var(--accent-cyan), var(--accent-teal));
        border-color: transparent;
        color: var(--bg-primary);
        font-weight: 600;
    }
    
    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, var(--bg-secondary) 0%, var(--bg-tertiary) 100%);
        border: 1px solid var(--border-color);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        transition: all 0.3s ease;
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
        background: linear-gradient(90deg, var(--accent-cyan), var(--accent-teal), var(--accent-lime));
    }
    
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 30px rgba(0, 188, 212, 0.15);
        border-color: var(--accent-cyan);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: var(--accent-cyan);
        margin: 0;
        line-height: 1;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: var(--text-secondary);
        margin-top: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .metric-delta {
        font-size: 0.8rem;
        margin-top: 0.25rem;
        font-weight: 500;
    }
    
    /* Data cards */
    .data-card {
        background: var(--bg-secondary);
        border: 1px solid var(--border-color);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        transition: all 0.3s ease;
    }
    
    .data-card:hover {
        border-color: var(--accent-teal);
        box-shadow: 0 4px 20px rgba(0, 150, 136, 0.1);
    }
    
    .card-header {
        display: flex;
        justify-content: between;
        align-items: center;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid var(--border-color);
    }
    
    .card-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: var(--text-primary);
        margin: 0;
    }
    
    .status-badge {
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .status-online { background: var(--accent-teal); color: var(--bg-primary); }
    .status-charging { background: var(--accent-lime); color: var(--bg-primary); }
    .status-idle { background: var(--text-secondary); color: var(--bg-primary); }
    .status-warning { background: var(--accent-orange); color: var(--bg-primary); }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, var(--accent-cyan), var(--accent-teal));
        color: var(--bg-primary);
        border: none;
        border-radius: 10px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        font-size: 0.9rem;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 188, 212, 0.3);
        background: linear-gradient(135deg, var(--accent-teal), var(--accent-cyan));
    }
    
    /* Form inputs */
    .stSelectbox > div > div {
        background-color: var(--bg-secondary);
        border: 1px solid var(--border-color);
        border-radius: 8px;
        color: var(--text-primary);
    }
    
    .stNumberInput > div > div > input {
        background-color: var(--bg-secondary);
        border: 1px solid var(--border-color);
        border-radius: 8px;
        color: var(--text-primary);
    }
    
    /* Dataframe styling */
    .stDataFrame {
        background-color: var(--bg-secondary);
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid var(--border-color);
    }
    
    /* Plotly chart styling */
    .js-plotly-plot {
        background-color: transparent !important;
        border-radius: 12px;
    }
    
    /* Expanders */
    .streamlit-expanderHeader {
        background-color: var(--bg-secondary);
        border: 1px solid var(--border-color);
        border-radius: 8px;
        color: var(--text-primary);
    }
    
    .streamlit-expanderContent {
        background-color: var(--bg-secondary);
        border: 1px solid var(--border-color);
        border-top: none;
        border-radius: 0 0 8px 8px;
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--bg-secondary);
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--accent-cyan);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--accent-teal);
    }
    
    /* Mobile responsiveness */
    @media (max-width: 768px) {
        .main-header {
            padding: 1rem;
            margin: -1rem -1rem 1rem -1rem;
        }
        
        .main-header h1 {
            font-size: 1.8rem;
        }
        
        .metric-card {
            padding: 1rem;
        }
        
        .metric-value {
            font-size: 2rem;
        }
    }
</style>
"""

st.markdown(dark_theme_css, unsafe_allow_html=True)

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

def init_session_state():
    """Initialize session state variables"""
    defaults = {
        'cells_data': {},
        'tasks_data': {},
        'monitoring_active': False,
        'current_page': 'Dashboard',
        'history_data': [],
        'system_alerts': []
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def generate_sample_data():
    """Generate sample data for demonstration"""
    if not st.session_state.cells_data:
        sample_cells = [
            {'type': 'lfp', 'id': 1},
            {'type': 'lfp', 'id': 2},
            {'type': 'li-ion', 'id': 3},
            {'type': 'lfp', 'id': 4}
        ]
        
        for cell in sample_cells:
            cell_key = f"cell_{cell['id']}_{cell['type']}"
            
            specs = {
                'lfp': {'voltage': 3.2, 'min_v': 2.8, 'max_v': 3.6},
                'li-ion': {'voltage': 3.7, 'min_v': 3.2, 'max_v': 4.2}
            }
            
            spec = specs[cell['type']]
            
            st.session_state.cells_data[cell_key] = {
                'type': cell['type'],
                'voltage': round(spec['voltage'] + random.uniform(-0.2, 0.2), 2),
                'current': round(random.uniform(-2, 3), 2),
                'temp': round(random.uniform(25, 40), 1),
                'capacity': round(random.uniform(80, 120), 1),
                'min_voltage': spec['min_v'],
                'max_voltage': spec['max_v'],
                'health': round(random.uniform(85, 100), 1),
                'cycles': random.randint(50, 800),
                'status': random.choice(['Charging', 'Discharging', 'Idle']),
                'last_updated': datetime.now()
            }

def create_plotly_theme():
    """Create consistent Plotly theme"""
    return {
        'layout': {
            'paper_bgcolor': 'rgba(0,0,0,0)',
            'plot_bgcolor': 'rgba(0,0,0,0)',
            'font': {'color': '#ffffff', 'family': 'Inter'},
            'colorway': ['#00bcd4', '#009688', '#cddc39', '#ff9800', '#e91e63'],
            'xaxis': {
                'gridcolor': '#404040',
                'linecolor': '#404040',
                'tickcolor': '#404040'
            },
            'yaxis': {
                'gridcolor': '#404040',
                'linecolor': '#404040',
                'tickcolor': '#404040'
            }
        }
    }

# ============================================================================
# HEADER COMPONENT
# ============================================================================

def render_header():
    """Render the fixed header"""
    st.markdown("""
    <div class="main-header">
        <h1>⚡ Battery Management System</h1>
        <p>Professional Dashboard | Real-time Monitoring & Control</p>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# SIDEBAR NAVIGATION
# ============================================================================

def render_sidebar():
    """Render the sidebar navigation"""
    with st.sidebar:
        st.markdown("### 🎛️ Navigation")
        
        pages = {
            '📊 Dashboard': 'dashboard',
            '🔋 Cell Management': 'cells',
            '📋 Task Control': 'tasks',
            '📈 Analytics': 'analytics',
            '⚙️ Settings': 'settings'
        }
        
        for page_name, page_key in pages.items():
            if st.button(page_name, key=f"nav_{page_key}", use_container_width=True):
                st.session_state.current_page = page_name
        
        st.markdown("---")
        
        # Quick stats
        if st.session_state.cells_data:
            st.markdown("### ⚡ System Status")
            
            total_cells = len(st.session_state.cells_data)
            active_cells = sum(1 for cell in st.session_state.cells_data.values() 
                             if cell['status'] != 'Idle')
            avg_health = np.mean([cell['health'] for cell in st.session_state.cells_data.values()])
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Cells", total_cells)
                st.metric("Health", f"{avg_health:.0f}%")
            with col2:
                st.metric("Active", active_cells)
                st.metric("Status", "🟢 Online")
        
        # Sample data button
        st.markdown("---")
        if st.button("🎲 Load Sample Data", use_container_width=True):
            generate_sample_data()
            st.rerun()

# ============================================================================
# DASHBOARD PAGE
# ============================================================================

def render_dashboard():
    """Render the main dashboard"""
    st.markdown("## 📊 System Overview")
    
    if not st.session_state.cells_data:
        st.info("🎯 Load sample data from the sidebar to get started, or navigate to Cell Management to add cells.")
        return
    
    # Key metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    total_power = sum(cell['voltage'] * abs(cell['current']) for cell in st.session_state.cells_data.values())
    total_capacity = sum(cell['capacity'] for cell in st.session_state.cells_data.values())
    avg_temp = np.mean([cell['temp'] for cell in st.session_state.cells_data.values()])
    critical_alerts = sum(1 for cell in st.session_state.cells_data.values() 
                         if cell['temp'] > 35 or cell['health'] < 80)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{total_power:.1f}W</div>
            <div class="metric-label">Total Power</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{total_capacity:.0f}Ah</div>
            <div class="metric-label">Total Capacity</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{avg_temp:.1f}°C</div>
            <div class="metric-label">Avg Temperature</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        alert_color = "#ff9800" if critical_alerts > 0 else "#009688"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color: {alert_color}">{critical_alerts}</div>
            <div class="metric-label">Alerts</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Charts row
    col1, col2 = st.columns(2)
    
    with col1:
        # Voltage chart
        cell_names = list(st.session_state.cells_data.keys())
        voltages = [st.session_state.cells_data[cell]['voltage'] for cell in cell_names]
        
        fig_voltage = go.Figure()
        fig_voltage.add_trace(go.Bar(
            x=[name.split('_')[1] for name in cell_names],
            y=voltages,
            marker_color='#00bcd4',
            name='Voltage',
            hovertemplate='<b>Cell %{x}</b><br>Voltage: %{y:.2f}V<extra></extra>'
        ))
        
        fig_voltage.update_layout(
            title="🔋 Cell Voltages",
            xaxis_title="Cell ID",
            yaxis_title="Voltage (V)",
            height=400,
            **create_plotly_theme()['layout']
        )
        
        st.plotly_chart(fig_voltage, use_container_width=True)
    
    with col2:
        # Temperature vs Health scatter
        temps = [cell['temp'] for cell in st.session_state.cells_data.values()]
        healths = [cell['health'] for cell in st.session_state.cells_data.values()]
        cell_types = [cell['type'] for cell in st.session_state.cells_data.values()]
        
        fig_scatter = go.Figure()
        
        for cell_type in set(cell_types):
            type_temps = [temps[i] for i, t in enumerate(cell_types) if t == cell_type]
            type_healths = [healths[i] for i, t in enumerate(cell_types) if t == cell_type]
            
            fig_scatter.add_trace(go.Scatter(
                x=type_temps,
                y=type_healths,
                mode='markers',
                name=cell_type.upper(),
                marker=dict(size=12, opacity=0.8),
                hovertemplate=f'<b>{cell_type.upper()}</b><br>Temp: %{{x:.1f}}°C<br>Health: %{{y:.1f}}%<extra></extra>'
            ))
        
        fig_scatter.update_layout(
            title="🌡️ Temperature vs Health",
            xaxis_title="Temperature (°C)",
            yaxis_title="Health (%)",
            height=400,
            **create_plotly_theme()['layout']
        )
        
        st.plotly_chart(fig_scatter, use_container_width=True)
    
    # Data table
    st.markdown("### 📊 Cell Status Table")
    
    # Prepare data for table
    table_data = []
    for cell_key, cell_data in st.session_state.cells_data.items():
        table_data.append({
            'Cell ID': cell_key,
            'Type': cell_data['type'].upper(),
            'Voltage (V)': f"{cell_data['voltage']:.2f}",
            'Current (A)': f"{cell_data['current']:.2f}",
            'Temperature (°C)': f"{cell_data['temp']:.1f}",
            'Health (%)': f"{cell_data['health']:.1f}",
            'Status': cell_data['status'],
            'Cycles': cell_data['cycles']
        })
    
    df = pd.DataFrame(table_data)
    st.dataframe(df, use_container_width=True, hide_index=True)

# ============================================================================
# CELL MANAGEMENT PAGE
# ============================================================================

def render_cell_management():
    """Render cell management page"""
    st.markdown("## 🔋 Cell Management")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### ➕ Add New Cells")
        
        with st.form("add_cells_form"):
            num_cells = st.number_input("Number of cells", min_value=1, max_value=10, value=1)
            
            cell_configs = []
            for i in range(num_cells):
                st.markdown(f"**Cell {i+1} Configuration**")
                cell_type = st.selectbox(
                    f"Cell {i+1} type",
                    ["lfp", "li-ion", "nmc", "lto"],
                    key=f"cell_type_{i}"
                )
                cell_configs.append(cell_type)
            
            if st.form_submit_button("🔋 Add Cells", use_container_width=True):
                for i, cell_type in enumerate(cell_configs):
                    cell_id = len(st.session_state.cells_data) + i + 1
                    cell_key = f"cell_{cell_id}_{cell_type}"
                    
                    specs = {
                        'lfp': {'voltage': 3.2, 'min_v': 2.8, 'max_v': 3.6},
                        'li-ion': {'voltage': 3.7, 'min_v': 3.2, 'max_v': 4.2},
                        'nmc': {'voltage': 3.6, 'min_v': 3.0, 'max_v': 4.0},
                        'lto': {'voltage': 2.4, 'min_v': 1.5, 'max_v': 2.8}
                    }
                    
                    spec = specs[cell_type]
                    
                    st.session_state.cells_data[cell_key] = {
                        'type': cell_type,
                        'voltage': spec['voltage'],
                        'current': round(random.uniform(-1, 2), 2),
                        'temp': round(random.uniform(25, 40), 1),
                        'capacity': round(random.uniform(80, 120), 1),
                        'min_voltage': spec['min_v'],
                        'max_voltage': spec['max_v'],
                        'health': round(random.uniform(85, 100), 1),
                        'cycles': random.randint(0, 500),
                        'status': random.choice(['Charging', 'Discharging', 'Idle']),
                        'last_updated': datetime.now()
                    }
                
                st.success(f"✅ Successfully added {len(cell_configs)} cell(s)")
                st.rerun()
    
    with col2:
        st.markdown("### 🔋 Cell Overview")
        
        if st.session_state.cells_data:
            for cell_key, cell_data in st.session_state.cells_data.items():
                status_class = {
                    'Charging': 'status-charging',
                    'Discharging': 'status-warning',
                    'Idle': 'status-idle'
                }.get(cell_data['status'], 'status-idle')
                
                st.markdown(f"""
                <div class="data-card">
                    <div class="card-header">
                        <h3 class="card-title">📋 {task_key.upper()}</h3>
                        <span class="status-badge {status_class}">{task_data['status']}</span>
                    </div>
                    <div>
                        <strong>Type:</strong> {task_data['task_type']}<br>
                        <strong>Duration:</strong> {task_data['duration']}s<br>
                        <strong>Created:</strong> {task_data['created_at']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    if st.button("▶️ Start", key=f"start_{task_key}"):
                        st.session_state.tasks_data[task_key]["status"] = "Running"
                        st.rerun()
                
                with col_b:
                    if st.button("⏸️ Pause", key=f"pause_{task_key}"):
                        st.session_state.tasks_data[task_key]["status"] = "Paused"
                        st.rerun()
                
                with col_c:
                    if st.button("🗑️ Delete", key=f"delete_{task_key}"):
                        del st.session_state.tasks_data[task_key]
                        st.rerun()
        else:
            st.info("No tasks created yet. Create a task to get started!")

# ============================================================================
# ANALYTICS PAGE
# ============================================================================

def render_analytics():
    """Render analytics page"""
    st.markdown("## 📈 System Analytics")
    
    if not st.session_state.cells_data:
        st.info("No data available for analysis. Add cells first!")
        return
    
    # Performance metrics
    col1, col2, col3 = st.columns(3)
    
    total_energy = sum(cell['voltage'] * abs(cell['current']) for cell in st.session_state.cells_data.values())
    avg_efficiency = np.mean([cell['health'] for cell in st.session_state.cells_data.values()])
    total_cycles = sum(cell['cycles'] for cell in st.session_state.cells_data.values())
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{total_energy:.1f}W</div>
            <div class="metric-label">Total Energy</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{avg_efficiency:.1f}%</div>
            <div class="metric-label">Avg Efficiency</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{total_cycles}</div>
            <div class="metric-label">Total Cycles</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Cell type distribution
        cell_types = [cell['type'] for cell in st.session_state.cells_data.values()]
        type_counts = pd.Series(cell_types).value_counts()
        
        fig_pie = go.Figure(data=[go.Pie(
            labels=type_counts.index,
            values=type_counts.values,
            hole=0.4,
            marker_colors=['#00bcd4', '#009688', '#cddc39', '#ff9800']
        )])
        
        fig_pie.update_layout(
            title="🔋 Cell Type Distribution",
            height=400,
            **create_plotly_theme()['layout']
        )
        
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        # Health vs Cycles
        healths = [cell['health'] for cell in st.session_state.cells_data.values()]
        cycles = [cell['cycles'] for cell in st.session_state.cells_data.values()]
        
        fig_health = go.Figure()
        fig_health.add_trace(go.Scatter(
            x=cycles,
            y=healths,
            mode='markers+lines',
            marker=dict(size=10, color='#00bcd4'),
            line=dict(color='#009688'),
            name='Health vs Cycles'
        ))
        
        fig_health.update_layout(
            title="🏥 Battery Health vs Cycle Count",
            xaxis_title="Cycle Count",
            yaxis_title="Health (%)",
            height=400,
            **create_plotly_theme()['layout']
        )
        
        st.plotly_chart(fig_health, use_container_width=True)
    
    # Recommendations
    st.markdown("### 💡 System Recommendations")
    
    recommendations = []
    
    # Temperature check
    hot_cells = [cell for cell in st.session_state.cells_data.values() if cell['temp'] > 35]
    if hot_cells:
        recommendations.append("🌡️ High temperature detected - Consider implementing thermal management")
    
    # Health check
    unhealthy_cells = [cell for cell in st.session_state.cells_data.values() if cell['health'] < 80]
    if unhealthy_cells:
        recommendations.append(f"🏥 {len(unhealthy_cells)} cell(s) below 80% health - Schedule maintenance")
    
    # Cycle check
    aged_cells = [cell for cell in st.session_state.cells_data.values() if cell['cycles'] > 500]
    if aged_cells:
        recommendations.append(f"🔄 {len(aged_cells)} cell(s) with high cycle count - Monitor closely")
    
    if not recommendations:
        recommendations.append("✅ All systems operating within normal parameters")
    
    for rec in recommendations:
        st.info(rec)

# ============================================================================
# SETTINGS PAGE
# ============================================================================

def render_settings():
    """Render settings page"""
    st.markdown("## ⚙️ System Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🎛️ General Settings")
        
        auto_refresh = st.toggle("Auto-refresh monitoring", value=st.session_state.monitoring_active)
        if auto_refresh != st.session_state.monitoring_active:
            st.session_state.monitoring_active = auto_refresh
        
        refresh_interval = st.slider("Refresh interval (seconds)", 1, 30, 5)
        
        st.markdown("### 🚨 Alert Thresholds")
        temp_threshold = st.slider("Temperature alert (°C)", 30, 50, 35)
        health_threshold = st.slider("Health alert (%)", 50, 90, 80)
        voltage_tolerance = st.slider("Voltage tolerance (%)", 1, 20, 10)
        
    with col2:
        st.markdown("### 📊 Data Management")
        
        if st.button("📥 Export Data", use_container_width=True):
            if st.session_state.cells_data:
                export_data = {
                    'cells': st.session_state.cells_data,
                    'tasks': st.session_state.tasks_data,
                    'exported_at': datetime.now().isoformat()
                }
                st.download_button(
                    "💾 Download JSON",
                    data=json.dumps(export_data, indent=2),
                    file_name=f"bms_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
            else:
                st.warning("No data to export")
        
        if st.button("🗑️ Clear All Data", use_container_width=True):
            if st.button("⚠️ Confirm Clear All", use_container_width=True):
                st.session_state.cells_data = {}
                st.session_state.tasks_data = {}
                st.session_state.history_data = []
                st.success("All data cleared!")
                st.rerun()
        
        st.markdown("### ℹ️ System Information")
        st.info(f"""
        **Version:** 2.0.0  
        **Last Update:** {datetime.now().strftime('%Y-%m-%d %H:%M')}  
        **Active Cells:** {len(st.session_state.cells_data)}  
        **Active Tasks:** {len(st.session_state.tasks_data)}
        """)

# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    """Main application logic"""
    render_header()
    render_sidebar()
    
    # Route to appropriate page
    current_page = st.session_state.get('current_page', '📊 Dashboard')
    
    if current_page == '📊 Dashboard':
        render_dashboard()
    elif current_page == '🔋 Cell Management':
        render_cell_management()
    elif current_page == '📋 Task Control':
        render_task_control()
    elif current_page == '📈 Analytics':
        render_analytics()
    elif current_page == '⚙️ Settings':
        render_settings()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; padding: 2rem; color: #666; font-size: 0.9rem;'>
        ⚡ Professional Battery Management System | Built with Streamlit & Python<br>
        <strong>Portfolio Project</strong> • Ready for GitHub & LinkedIn
    </div>
    """, unsafe_allow_html=True)
    
    # Auto-refresh logic
    if st.session_state.monitoring_active and current_page == '📊 Dashboard':
        time.sleep(2)
        st.rerun()

if __name__ == "__main__":
    main() {cell_key.upper()}</h3>
                        <span class="status-badge {status_class}">{cell_data['status']}</span>
                    </div>
                    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem;">
                        <div>
                            <strong>Voltage:</strong> {cell_data['voltage']:.2f}V<br>
                            <strong>Current:</strong> {cell_data['current']:.2f}A
                        </div>
                        <div>
                            <strong>Temperature:</strong> {cell_data['temp']:.1f}°C<br>
                            <strong>Capacity:</strong> {cell_data['capacity']:.1f}Ah
                        </div>
                        <div>
                            <strong>Health:</strong> {cell_data['health']:.1f}%<br>
                            <strong>Cycles:</strong> {cell_data['cycles']}
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"🗑️ Remove {cell_key}", key=f"remove_{cell_key}"):
                    del st.session_state.cells_data[cell_key]
                    st.rerun()
        else:
            st.info("No cells configured. Add some cells to get started!")

# ============================================================================
# TASK CONTROL PAGE
# ============================================================================

def render_task_control():
    """Render task control page"""
    st.markdown("## 📋 Task Management")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### ➕ Create New Task")
        
        with st.form("task_form"):
            task_type = st.selectbox(
                "Task Type",
                ["CC_CV", "IDLE", "CC_CD"]
            )
            
            if task_type == "CC_CV":
                st.markdown("**CC_CV Parameters**")
                cc_value = st.number_input("CC Value (A)", value=2.0, step=0.1)
                cv_voltage = st.number_input("CV Voltage (V)", value=4.0, step=0.1)
                current = st.number_input("Current Limit (A)", value=1.0, step=0.1)
                capacity = st.number_input("Capacity (Ah)", value=10.0, step=0.1)
                duration = st.number_input("Duration (seconds)", value=3600, step=60)
                
            elif task_type == "IDLE":
                st.markdown("**IDLE Parameters**")
                duration = st.number_input("Duration (seconds)", value=1800, step=60)
                
            elif task_type == "CC_CD":
                st.markdown("**CC_CD Parameters**")
                cc_value = st.number_input("CC Value (A)", value=2.0, step=0.1)
                voltage = st.number_input("Cutoff Voltage (V)", value=2.8, step=0.1)
                capacity = st.number_input("Capacity (Ah)", value=10.0, step=0.1)
                duration = st.number_input("Duration (seconds)", value=3600, step=60)
            
            if st.form_submit_button("📋 Create Task", use_container_width=True):
                task_id = len(st.session_state.tasks_data) + 1
                task_key = f"task_{task_id}"
                
                task_data = {
                    "task_type": task_type,
                    "duration": duration,
                    "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "status": "Pending"
                }
                
                if task_type == "CC_CV":
                    task_data.update({
                        "cc_value": cc_value,
                        "cv_voltage": cv_voltage,
                        "current": current,
                        "capacity": capacity
                    })
                elif task_type == "CC_CD":
                    task_data.update({
                        "cc_value": cc_value,
                        "voltage": voltage,
                        "capacity": capacity
                    })
                
                st.session_state.tasks_data[task_key] = task_data
                st.success(f"✅ Task {task_key} created successfully!")
                st.rerun()
    
    with col2:
        st.markdown("### 📋 Task Queue")
        
        if st.session_state.tasks_data:
            for task_key, task_data in st.session_state.tasks_data.items():
                status_class = {
                    'Pending': 'status-idle',
                    'Running': 'status-charging',
                    'Paused': 'status-warning',
                    'Completed': 'status-online'
                }.get(task_data['status'], 'status-idle')
                
                st.markdown(f"""
                <div class="data-card">
                    <div class="card-header">
                        <h3 class="card-title">
