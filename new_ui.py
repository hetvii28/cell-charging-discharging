import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import random
import time
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Battery Cell Management Dashboard",
    page_icon="🔋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark theme and styling
st.markdown("""
<style>
    /* Dark theme styles */
    .main {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
    }
    
    .stApp {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
    }
    
    /* Custom metric cards */
    .metric-card {
        background: linear-gradient(145deg, #1e1e3f, #2a2a5a);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
        border: 1px solid #3a3a6b;
        margin: 10px 0;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(59, 130, 246, 0.2);
    }
    
    /* Title styling */
    .dashboard-title {
        background: linear-gradient(90deg, #3b82f6, #8b5cf6, #06b6d4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 30px;
    }
    
    /* Custom buttons */
    .stButton > button {
        background: linear-gradient(145deg, #3b82f6, #1d4ed8);
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        background: linear-gradient(145deg, #1d4ed8, #1e40af);
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(59, 130, 246, 0.3);
    }
    
    /* Input field styling */
    .stSelectbox > div > div {
        background: #2a2a5a;
        border: 1px solid #3a3a6b;
        border-radius: 8px;
    }
    
    .stNumberInput > div > div > input {
        background: #2a2a5a;
        border: 1px solid #3a3a6b;
        border-radius: 8px;
        color: white;
    }
    
    /* Status indicators */
    .status-good { color: #10b981; font-weight: bold; }
    .status-warning { color: #f59e0b; font-weight: bold; }
    .status-critical { color: #ef4444; font-weight: bold; }
    
    /* Animation for loading */
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    .pulse {
        animation: pulse 2s infinite;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'cells_data' not in st.session_state:
    st.session_state.cells_data = {}
if 'tasks_data' not in st.session_state:
    st.session_state.tasks_data = {}
if 'simulation_running' not in st.session_state:
    st.session_state.simulation_running = False

# Header
st.markdown('<h1 class="dashboard-title">🔋 Battery Cell Management Dashboard</h1>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### ⚙️ Control Panel")
    
    # Cell Management Section
    st.markdown("#### 🔬 Cell Configuration")
    
    num_cells = st.number_input("Number of Cells", min_value=1, max_value=20, value=3, step=1)
    
    cell_types = []
    for i in range(num_cells):
        cell_type = st.selectbox(f"Cell {i+1} Type", ["lfp", "nmc"], key=f"cell_type_{i}")
        cell_types.append(cell_type)
    
    if st.button("🔄 Generate Cells"):
        st.session_state.cells_data = {}
        for idx, cell_type in enumerate(cell_types, start=1):
            cell_key = f"cell_{idx}_{cell_type}"
            voltage = 3.2 if cell_type == "lfp" else 3.6
            min_voltage = 2.8 if cell_type == "lfp" else 3.2
            max_voltage = 3.6 if cell_type == "lfp" else 4.0
            current = round(random.uniform(0.5, 5.0), 2)
            temp = round(random.uniform(25, 40), 1)
            capacity = round(voltage * current, 2)
            
            st.session_state.cells_data[cell_key] = {
                "voltage": voltage,
                "current": current,
                "temp": temp,
                "capacity": capacity,
                "min_voltage": min_voltage,
                "max_voltage": max_voltage,
                "type": cell_type
            }
        st.success("✅ Cells generated successfully!")
    
    st.markdown("---")
    
    # Task Management Section
    st.markdown("#### 📋 Task Configuration")
    
    num_tasks = st.number_input("Number of Tasks", min_value=1, max_value=10, value=2, step=1)
    
    if st.button("➕ Configure Tasks"):
        st.session_state.show_task_config = True

# Main content
if st.session_state.cells_data:
    # Create tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "🔋 Cell Details", "⚡ Tasks", "📈 Analytics"])
    
    with tab1:
        # Key Metrics Row
        col1, col2, col3, col4 = st.columns(4)
        
        total_cells = len(st.session_state.cells_data)
        avg_voltage = np.mean([cell['voltage'] for cell in st.session_state.cells_data.values()])
        avg_temp = np.mean([cell['temp'] for cell in st.session_state.cells_data.values()])
        total_capacity = sum([cell['capacity'] for cell in st.session_state.cells_data.values()])
        
        with col1:
            st.markdown("""
            <div class="metric-card">
                <h3 style="color: #3b82f6; margin: 0;">Total Cells</h3>
                <h1 style="color: white; margin: 10px 0;">{}</h1>
                <p style="color: #94a3b8; margin: 0;">Active Monitoring</p>
            </div>
            """.format(total_cells), unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="metric-card">
                <h3 style="color: #10b981; margin: 0;">Avg Voltage</h3>
                <h1 style="color: white; margin: 10px 0;">{:.2f}V</h1>
                <p style="color: #94a3b8; margin: 0;">System Health</p>
            </div>
            """.format(avg_voltage), unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="metric-card">
                <h3 style="color: #f59e0b; margin: 0;">Avg Temperature</h3>
                <h1 style="color: white; margin: 10px 0;">{:.1f}°C</h1>
                <p style="color: #94a3b8; margin: 0;">Thermal Status</p>
            </div>
            """.format(avg_temp), unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
            <div class="metric-card">
                <h3 style="color: #8b5cf6; margin: 0;">Total Capacity</h3>
                <h1 style="color: white; margin: 10px 0;">{:.2f}Wh</h1>
                <p style="color: #94a3b8; margin: 0;">Energy Storage</p>
            </div>
            """.format(total_capacity), unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Charts Row
        col1, col2 = st.columns(2)
        
        with col1:
            # Voltage Distribution Chart
            cell_names = list(st.session_state.cells_data.keys())
            voltages = [st.session_state.cells_data[cell]['voltage'] for cell in cell_names]
            cell_types_chart = [st.session_state.cells_data[cell]['type'] for cell in cell_names]
            
            fig1 = px.bar(
                x=cell_names, 
                y=voltages,
                color=cell_types_chart,
                title="🔋 Cell Voltage Distribution",
                color_discrete_map={'lfp': '#10b981', 'nmc': '#3b82f6'}
            )
            fig1.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='white',
                title_font_size=16,
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)')
            )
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            # Temperature vs Current Scatter
            temps = [st.session_state.cells_data[cell]['temp'] for cell in cell_names]
            currents = [st.session_state.cells_data[cell]['current'] for cell in cell_names]
            
            fig2 = px.scatter(
                x=temps,
                y=currents,
                color=cell_types_chart,
                size=[10]*len(cell_names),
                title="🌡️ Temperature vs Current",
                labels={'x': 'Temperature (°C)', 'y': 'Current (A)'},
                color_discrete_map={'lfp': '#10b981', 'nmc': '#3b82f6'}
            )
            fig2.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='white',
                title_font_size=16,
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)')
            )
            st.plotly_chart(fig2, use_container_width=True)
    
    with tab2:
        st.markdown("### 🔋 Cell Details")
        
        # Convert to DataFrame for better display
        df_cells = pd.DataFrame.from_dict(st.session_state.cells_data, orient='index')
        df_cells.index.name = 'Cell ID'
        
        # Add status column based on voltage
        def get_status(row):
            if row['min_voltage'] <= row['voltage'] <= row['max_voltage']:
                return "🟢 Normal"
            elif row['voltage'] < row['min_voltage']:
                return "🔴 Low Voltage"
            else:
                return "🟡 High Voltage"
        
        df_cells['Status'] = df_cells.apply(get_status, axis=1)
        
        # Display as styled table
        st.dataframe(
            df_cells,
            use_container_width=True,
            height=400
        )
        
        # Individual cell monitoring
        st.markdown("### 📊 Individual Cell Monitoring")
        selected_cell = st.selectbox("Select Cell for Detailed View", list(st.session_state.cells_data.keys()))
        
        if selected_cell:
            cell_data = st.session_state.cells_data[selected_cell]
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                # Voltage gauge
                fig_gauge = go.Figure(go.Indicator(
                    mode = "gauge+number+delta",
                    value = cell_data['voltage'],
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    title = {'text': "Voltage (V)"},
                    delta = {'reference': (cell_data['min_voltage'] + cell_data['max_voltage'])/2},
                    gauge = {
                        'axis': {'range': [None, cell_data['max_voltage'] + 0.5]},
                        'bar': {'color': "#3b82f6"},
                        'steps': [
                            {'range': [0, cell_data['min_voltage']], 'color': "#ef4444"},
                            {'range': [cell_data['min_voltage'], cell_data['max_voltage']], 'color': "#10b981"}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': cell_data['max_voltage']
                        }
                    }
                ))
                fig_gauge.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font_color='white',
                    height=300
                )
                st.plotly_chart(fig_gauge, use_container_width=True)
            
            with col2:
                # Temperature gauge
                fig_temp = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = cell_data['temp'],
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    title = {'text': "Temperature (°C)"},
                    gauge = {
                        'axis': {'range': [None, 60]},
                        'bar': {'color': "#f59e0b"},
                        'steps': [
                            {'range': [0, 30], 'color': "#10b981"},
                            {'range': [30, 45], 'color': "#f59e0b"},
                            {'range': [45, 60], 'color': "#ef4444"}
                        ]
                    }
                ))
                fig_temp.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font_color='white',
                    height=300
                )
                st.plotly_chart(fig_temp, use_container_width=True)
            
            with col3:
                # Current and Capacity info
                st.markdown(f"""
                <div class="metric-card">
                    <h4 style="color: #8b5cf6;">⚡ Current</h4>
                    <h2 style="color: white;">{cell_data['current']} A</h2>
                    <hr style="border-color: #3a3a6b;">
                    <h4 style="color: #06b6d4;">🔋 Capacity</h4>
                    <h2 style="color: white;">{cell_data['capacity']} Wh</h2>
                    <hr style="border-color: #3a3a6b;">
                    <h4 style="color: #10b981;">📋 Type</h4>
                    <h2 style="color: white;">{cell_data['type'].upper()}</h2>
                </div>
                """, unsafe_allow_html=True)
    
    with tab3:
        st.markdown("### ⚡ Task Management")
        
        # Task creation interface
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("#### ➕ Add New Task")
            task_type = st.selectbox("Task Type", ["CC_CV", "IDLE", "CC_CD"])
            
            task_data = {"task_type": task_type}
            
            if task_type == "CC_CV":
                cc_input = st.text_input("CC Value (e.g., '5A' or '10W')", value="5A")
                cv_voltage = st.number_input("CV Voltage (V)", value=3.6, step=0.1)
                current = st.number_input("Current (A)", value=2.5, step=0.1)
                capacity = st.number_input("Capacity", value=10.0, step=0.1)
                time_seconds = st.number_input("Time (seconds)", value=3600, step=1)
                
                task_data.update({
                    "cc_cp": cc_input,
                    "cv_voltage": cv_voltage,
                    "current": current,
                    "capacity": capacity,
                    "time_seconds": time_seconds
                })
            
            elif task_type == "IDLE":
                time_seconds = st.number_input("Time (seconds)", value=1800, step=1)
                task_data.update({"time_seconds": time_seconds})
            
            elif task_type == "CC_CD":
                cc_input = st.text_input("CC Value (e.g., '5A' or '10W')", value="5A")
                voltage = st.number_input("Voltage (V)", value=3.2, step=0.1)
                capacity = st.number_input("Capacity", value=10.0, step=0.1)
                time_seconds = st.number_input("Time (seconds)", value=3600, step=1)
                
                task_data.update({
                    "cc_cp": cc_input,
                    "voltage": voltage,
                    "capacity": capacity,
                    "time_seconds": time_seconds
                })
            
            if st.button("➕ Add Task"):
                task_key = f"task_{len(st.session_state.tasks_data) + 1}"
                st.session_state.tasks_data[task_key] = task_data
                st.success(f"✅ Task {task_key} added successfully!")
        
        with col2:
            st.markdown("#### 📋 Current Tasks")
            if st.session_state.tasks_data:
                df_tasks = pd.DataFrame.from_dict(st.session_state.tasks_data, orient='index')
                st.dataframe(df_tasks, use_container_width=True)
                
                # Task visualization
                task_types = [task['task_type'] for task in st.session_state.tasks_data.values()]
                task_counts = pd.Series(task_types).value_counts()
                
                fig_tasks = px.pie(
                    values=task_counts.values,
                    names=task_counts.index,
                    title="📊 Task Distribution",
                    color_discrete_sequence=['#3b82f6', '#10b981', '#f59e0b']
                )
                fig_tasks.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='white'
                )
                st.plotly_chart(fig_tasks, use_container_width=True)
            else:
                st.info("No tasks configured yet. Add some tasks to get started!")
    
    with tab4:
        st.markdown("### 📈 Advanced Analytics")
        
        # Real-time simulation
        col1, col2 = st.columns([1, 3])
        
        with col1:
            st.markdown("#### 🔄 Live Simulation")
            if st.button("▶️ Start Simulation"):
                st.session_state.simulation_running = True
            if st.button("⏸️ Stop Simulation"):
                st.session_state.simulation_running = False
        
        with col2:
            if st.session_state.simulation_running:
                # Create placeholder for real-time chart
                chart_placeholder = st.empty()
                
                # Simulate real-time data
                time_data = []
                voltage_data = {cell: [] for cell in st.session_state.cells_data.keys()}
                
                for i in range(50):
                    time_data.append(i)
                    for cell in st.session_state.cells_data.keys():
                        base_voltage = st.session_state.cells_data[cell]['voltage']
                        noise = random.uniform(-0.1, 0.1)
                        voltage_data[cell].append(base_voltage + noise)
                    
                    # Create real-time chart
                    fig_realtime = go.Figure()
                    
                    colors = ['#3b82f6', '#10b981', '#f59e0b', '#8b5cf6', '#06b6d4']
                    for idx, (cell, voltages) in enumerate(voltage_data.items()):
                        fig_realtime.add_trace(go.Scatter(
                            x=time_data,
                            y=voltages,
                            mode='lines',
                            name=cell,
                            line=dict(color=colors[idx % len(colors)], width=2)
                        ))
                    
                    fig_realtime.update_layout(
                        title="🔴 Live Voltage Monitoring",
                        xaxis_title="Time (s)",
                        yaxis_title="Voltage (V)",
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font_color='white',
                        showlegend=True,
                        height=400
                    )
                    
                    chart_placeholder.plotly_chart(fig_realtime, use_container_width=True)
                    time.sleep(0.1)
                    
                    if not st.session_state.simulation_running:
                        break
        
        # Performance metrics
        st.markdown("#### 📊 Performance Metrics")
        
        # Create comparative analysis
        if len(st.session_state.cells_data) > 1:
            fig_comparison = make_subplots(
                rows=2, cols=2,
                subplot_titles=('Voltage Comparison', 'Current Comparison', 
                              'Temperature Distribution', 'Capacity Analysis'),
                specs=[[{"secondary_y": False}, {"secondary_y": False}],
                       [{"secondary_y": False}, {"secondary_y": False}]]
            )
            
            cell_names = list(st.session_state.cells_data.keys())
            voltages = [st.session_state.cells_data[cell]['voltage'] for cell in cell_names]
            currents = [st.session_state.cells_data[cell]['current'] for cell in cell_names]
            temps = [st.session_state.cells_data[cell]['temp'] for cell in cell_names]
            capacities = [st.session_state.cells_data[cell]['capacity'] for cell in cell_names]
            
            # Voltage comparison
            fig_comparison.add_trace(
                go.Bar(x=cell_names, y=voltages, name="Voltage", marker_color='#3b82f6'),
                row=1, col=1
            )
            
            # Current comparison
            fig_comparison.add_trace(
                go.Bar(x=cell_names, y=currents, name="Current", marker_color='#10b981'),
                row=1, col=2
            )
            
            # Temperature histogram
            fig_comparison.add_trace(
                go.Histogram(x=temps, name="Temperature", marker_color='#f59e0b'),
                row=2, col=1
            )
            
            # Capacity scatter
            fig_comparison.add_trace(
                go.Scatter(x=cell_names, y=capacities, mode='markers+lines', 
                          name="Capacity", marker_color='#8b5cf6'),
                row=2, col=2
            )
            
            fig_comparison.update_layout(
                height=600,
                showlegend=False,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='white'
            )
            
            st.plotly_chart(fig_comparison, use_container_width=True)

else:
    # Welcome screen
    st.markdown("""
    <div style="text-align: center; padding: 50px;">
        <h2 style="color: #3b82f6;">Welcome to Battery Cell Management Dashboard</h2>
        <p style="color: #94a3b8; font-size: 1.2rem;">
            Configure your battery cells in the sidebar to get started with monitoring and analysis.
        </p>
        <div class="pulse" style="font-size: 4rem; margin: 30px 0;">🔋</div>
        <p style="color: #94a3b8;">
            • Real-time cell monitoring<br>
            • Task management system<br>
            • Advanced analytics and visualization<br>
            • Interactive charts and gauges
        </p>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(
    '<p style="text-align: center; color: #94a3b8;">🔋 Battery Cell Management Dashboard | Built with Streamlit & Plotly</p>',
    unsafe_allow_html=True
)
