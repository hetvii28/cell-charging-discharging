import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import random
import time
from datetime import datetime, timedelta

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
    .main > div {
        padding-top: 2rem;
    }
    
    .stMetric {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .stMetric > div > div > div > div {
        color: white !important;
    }
    
    .battery-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 0.5rem 0;
        color: white;
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    .task-card {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 0.5rem 0;
        color: white;
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    .header-style {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'cells_data' not in st.session_state:
    st.session_state.cells_data = {}
if 'tasks_data' not in st.session_state:
    st.session_state.tasks_data = {}
if 'monitoring' not in st.session_state:
    st.session_state.monitoring = False
if 'history' not in st.session_state:
    st.session_state.history = []

# Header
st.markdown("""
<div class="header-style">
    <h1>⚡ Advanced Battery Management System</h1>
    <p>Monitor, Control & Optimize Your Battery Cells</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 🎛️ Control Panel")
    
    # Mode selection
    mode = st.selectbox(
        "Select Operation Mode",
        ["🔋 Cell Management", "📋 Task Configuration", "📊 Real-time Monitoring", "📈 Analytics"]
    )
    
    st.markdown("---")
    
    # Quick stats if cells exist
    if st.session_state.cells_data:
        st.markdown("### ⚡ Quick Stats")
        total_cells = len(st.session_state.cells_data)
        avg_temp = np.mean([cell['temp'] for cell in st.session_state.cells_data.values()])
        avg_voltage = np.mean([cell['voltage'] for cell in st.session_state.cells_data.values()])
        
        st.metric("Total Cells", total_cells)
        st.metric("Avg Temperature", f"{avg_temp:.1f}°C")
        st.metric("Avg Voltage", f"{avg_voltage:.1f}V")

# Main content based on mode
if mode == "🔋 Cell Management":
    st.markdown("## 🔋 Battery Cell Configuration")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### Add New Cells")
        
        with st.form("cell_form"):
            num_cells = st.number_input("Number of cells to add", min_value=1, max_value=20, value=1)
            cell_types = []
            
            for i in range(num_cells):
                cell_type = st.selectbox(
                    f"Cell {i+1} type", 
                    ["lfp", "li-ion", "nmc", "lto"],
                    key=f"cell_type_{i}"
                )
                cell_types.append(cell_type)
            
            submitted = st.form_submit_button("🔋 Add Cells", use_container_width=True)
            
            if submitted:
                for i, cell_type in enumerate(cell_types):
                    cell_id = len(st.session_state.cells_data) + 1
                    cell_key = f"cell_{cell_id}_{cell_type}"
                    
                    # Cell specifications based on type
                    specs = {
                        "lfp": {"voltage": 3.2, "min_v": 2.8, "max_v": 3.6, "capacity": 100},
                        "li-ion": {"voltage": 3.7, "min_v": 3.2, "max_v": 4.2, "capacity": 120},
                        "nmc": {"voltage": 3.6, "min_v": 3.0, "max_v": 4.0, "capacity": 110},
                        "lto": {"voltage": 2.4, "min_v": 1.5, "max_v": 2.8, "capacity": 80}
                    }
                    
                    spec = specs[cell_type]
                    
                    st.session_state.cells_data[cell_key] = {
                        "type": cell_type,
                        "voltage": spec["voltage"],
                        "current": round(random.uniform(0, 5), 2),
                        "temp": round(random.uniform(25, 40), 1),
                        "capacity": spec["capacity"],
                        "min_voltage": spec["min_v"],
                        "max_voltage": spec["max_v"],
                        "health": round(random.uniform(85, 100), 1),
                        "cycles": random.randint(0, 1000),
                        "status": random.choice(["Charging", "Discharging", "Idle"])
                    }
                
                st.success(f"✅ Added {num_cells} cell(s) successfully!")
                st.rerun()
    
    with col2:
        st.markdown("### 🔋 Cell Overview")
        
        if st.session_state.cells_data:
            # Create metrics row
            cols = st.columns(4)
            total_cells = len(st.session_state.cells_data)
            total_capacity = sum([cell['capacity'] for cell in st.session_state.cells_data.values()])
            avg_health = np.mean([cell['health'] for cell in st.session_state.cells_data.values()])
            critical_cells = sum([1 for cell in st.session_state.cells_data.values() if cell['temp'] > 35])
            
            with cols[0]:
                st.metric("Total Cells", total_cells, "")
            with cols[1]:
                st.metric("Total Capacity", f"{total_capacity}Ah", "")
            with cols[2]:
                st.metric("Avg Health", f"{avg_health:.1f}%", "")
            with cols[3]:
                st.metric("Critical Temp", critical_cells, "⚠️" if critical_cells > 0 else "✅")
            
            # Detailed cell cards
            st.markdown("### 📱 Individual Cell Status")
            
            for cell_key, cell_data in st.session_state.cells_data.items():
                with st.expander(f"🔋 {cell_key.upper()}", expanded=False):
                    col_a, col_b, col_c = st.columns(3)
                    
                    with col_a:
                        st.metric("Voltage", f"{cell_data['voltage']}V")
                        st.metric("Current", f"{cell_data['current']}A")
                    
                    with col_b:
                        st.metric("Temperature", f"{cell_data['temp']}°C")
                        st.metric("Capacity", f"{cell_data['capacity']}Ah")
                    
                    with col_c:
                        st.metric("Health", f"{cell_data['health']}%")
                        st.metric("Cycles", cell_data['cycles'])
                    
                    # Status indicator
                    status_color = {"Charging": "🟢", "Discharging": "🟡", "Idle": "⚪"}
                    st.markdown(f"**Status:** {status_color[cell_data['status']]} {cell_data['status']}")
                    
                    # Remove button
                    if st.button(f"🗑️ Remove {cell_key}", key=f"remove_{cell_key}"):
                        del st.session_state.cells_data[cell_key]
                        st.rerun()
        else:
            st.info("No cells configured yet. Add some cells to get started!")

elif mode == "📋 Task Configuration":
    st.markdown("## 📋 Task Management")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### Create New Task")
        
        with st.form("task_form"):
            task_type = st.selectbox(
                "Task Type",
                ["CC_CV (Constant Current/Constant Voltage)", "IDLE", "CC_CD (Constant Current/Constant Discharge)"]
            )
            
            if "CC_CV" in task_type:
                st.markdown("**CC_CV Parameters**")
                cc_value = st.number_input("CC Value (A)", value=2.0, step=0.1)
                cv_voltage = st.number_input("CV Voltage (V)", value=4.0, step=0.1)
                current = st.number_input("Current Limit (A)", value=1.0, step=0.1)
                capacity = st.number_input("Capacity (Ah)", value=10.0, step=0.1)
                duration = st.number_input("Duration (seconds)", value=3600, step=60)
                
            elif "IDLE" in task_type:
                st.markdown("**IDLE Parameters**")
                duration = st.number_input("Duration (seconds)", value=1800, step=60)
                
            elif "CC_CD" in task_type:
                st.markdown("**CC_CD Parameters**")
                cc_value = st.number_input("CC Value (A)", value=2.0, step=0.1)
                voltage = st.number_input("Cutoff Voltage (V)", value=2.8, step=0.1)
                capacity = st.number_input("Capacity (Ah)", value=10.0, step=0.1)
                duration = st.number_input("Duration (seconds)", value=3600, step=60)
            
            submitted = st.form_submit_button("📋 Create Task", use_container_width=True)
            
            if submitted:
                task_id = len(st.session_state.tasks_data) + 1
                task_key = f"task_{task_id}"
                
                task_data = {"task_type": task_type.split()[0], "duration": duration}
                
                if "CC_CV" in task_type:
                    task_data.update({
                        "cc_value": cc_value,
                        "cv_voltage": cv_voltage,
                        "current": current,
                        "capacity": capacity
                    })
                elif "CC_CD" in task_type:
                    task_data.update({
                        "cc_value": cc_value,
                        "voltage": voltage,
                        "capacity": capacity
                    })
                
                task_data["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                task_data["status"] = "Pending"
                
                st.session_state.tasks_data[task_key] = task_data
                st.success(f"✅ Task {task_key} created successfully!")
                st.rerun()
    
    with col2:
        st.markdown("### 📋 Task Queue")
        
        if st.session_state.tasks_data:
            for task_key, task_data in st.session_state.tasks_data.items():
                with st.expander(f"📋 {task_key.upper()}", expanded=False):
                    st.markdown(f"**Type:** {task_data['task_type']}")
                    st.markdown(f"**Duration:** {task_data['duration']}s")
                    st.markdown(f"**Status:** {task_data['status']}")
                    st.markdown(f"**Created:** {task_data['created_at']}")
                    
                    col_a, col_b, col_c = st.columns(3)
                    with col_a:
                        if st.button(f"▶️ Start", key=f"start_{task_key}"):
                            st.session_state.tasks_data[task_key]["status"] = "Running"
                            st.rerun()
                    
                    with col_b:
                        if st.button(f"⏸️ Pause", key=f"pause_{task_key}"):
                            st.session_state.tasks_data[task_key]["status"] = "Paused"
                            st.rerun()
                    
                    with col_c:
                        if st.button(f"🗑️ Delete", key=f"delete_{task_key}"):
                            del st.session_state.tasks_data[task_key]
                            st.rerun()
        else:
            st.info("No tasks created yet. Create a task to get started!")

elif mode == "📊 Real-time Monitoring":
    st.markdown("## 📊 Real-time Battery Monitoring")
    
    if st.session_state.cells_data:
        # Control buttons
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("▶️ Start Monitoring", use_container_width=True):
                st.session_state.monitoring = True
        with col2:
            if st.button("⏸️ Stop Monitoring", use_container_width=True):
                st.session_state.monitoring = False
        with col3:
            if st.button("🔄 Refresh Data", use_container_width=True):
                # Update cell data with random variations
                for cell_key, cell_data in st.session_state.cells_data.items():
                    st.session_state.cells_data[cell_key]['temp'] += random.uniform(-1, 1)
                    st.session_state.cells_data[cell_key]['voltage'] += random.uniform(-0.1, 0.1)
                    st.session_state.cells_data[cell_key]['current'] += random.uniform(-0.5, 0.5)
        
        # Create real-time charts
        if st.session_state.cells_data:
            # Voltage chart
            fig_voltage = go.Figure()
            cell_names = list(st.session_state.cells_data.keys())
            voltages = [st.session_state.cells_data[cell]['voltage'] for cell in cell_names]
            
            fig_voltage.add_trace(go.Bar(
                x=cell_names,
                y=voltages,
                marker_color='lightblue',
                name='Voltage'
            ))
            
            fig_voltage.update_layout(
                title="🔋 Cell Voltages",
                xaxis_title="Cells",
                yaxis_title="Voltage (V)",
                height=400
            )
            
            st.plotly_chart(fig_voltage, use_container_width=True)
            
            # Temperature chart
            fig_temp = go.Figure()
            temperatures = [st.session_state.cells_data[cell]['temp'] for cell in cell_names]
            
            fig_temp.add_trace(go.Scatter(
                x=cell_names,
                y=temperatures,
                mode='lines+markers',
                marker_color='red',
                name='Temperature'
            ))
            
            fig_temp.update_layout(
                title="🌡️ Cell Temperatures",
                xaxis_title="Cells",
                yaxis_title="Temperature (°C)",
                height=400
            )
            
            st.plotly_chart(fig_temp, use_container_width=True)
            
            # Health status pie chart
            health_ranges = {"Excellent (90-100%)": 0, "Good (80-89%)": 0, "Fair (70-79%)": 0, "Poor (<70%)": 0}
            
            for cell_data in st.session_state.cells_data.values():
                health = cell_data['health']
                if health >= 90:
                    health_ranges["Excellent (90-100%)"] += 1
                elif health >= 80:
                    health_ranges["Good (80-89%)"] += 1
                elif health >= 70:
                    health_ranges["Fair (70-79%)"] += 1
                else:
                    health_ranges["Poor (<70%)"] += 1
            
            fig_health = go.Figure(data=[go.Pie(
                labels=list(health_ranges.keys()),
                values=list(health_ranges.values()),
                hole=0.4
            )])
            
            fig_health.update_layout(
                title="🏥 Battery Health Distribution",
                height=400
            )
            
            st.plotly_chart(fig_health, use_container_width=True)
            
        # Auto-refresh for monitoring
        if st.session_state.monitoring:
            time.sleep(2)
            st.rerun()
    else:
        st.warning("⚠️ No cells available for monitoring. Please add cells first.")

elif mode == "📈 Analytics":
    st.markdown("## 📈 Battery Analytics & Insights")
    
    if st.session_state.cells_data:
        # Performance metrics
        st.markdown("### 🎯 Performance Metrics")
        
        cols = st.columns(4)
        
        # Calculate metrics
        total_energy = sum([cell['voltage'] * cell['current'] for cell in st.session_state.cells_data.values()])
        avg_efficiency = np.mean([cell['health'] for cell in st.session_state.cells_data.values()])
        total_cycles = sum([cell['cycles'] for cell in st.session_state.cells_data.values()])
        power_consumption = sum([abs(cell['current']) for cell in st.session_state.cells_data.values()])
        
        with cols[0]:
            st.metric("Total Energy", f"{total_energy:.2f}W", "")
        with cols[1]:
            st.metric("Avg Efficiency", f"{avg_efficiency:.1f}%", "")
        with cols[2]:
            st.metric("Total Cycles", f"{total_cycles}", "")
        with cols[3]:
            st.metric("Power Draw", f"{power_consumption:.2f}A", "")
        
        # Detailed analytics
        col1, col2 = st.columns(2)
        
        with col1:
            # Cell type distribution
            cell_types = [cell['type'] for cell in st.session_state.cells_data.values()]
            type_counts = {cell_type: cell_types.count(cell_type) for cell_type in set(cell_types)}
            
            fig_types = px.bar(
                x=list(type_counts.keys()),
                y=list(type_counts.values()),
                title="🔋 Cell Type Distribution",
                labels={'x': 'Cell Type', 'y': 'Count'}
            )
            st.plotly_chart(fig_types, use_container_width=True)
        
        with col2:
            # Voltage vs Temperature correlation
            voltages = [cell['voltage'] for cell in st.session_state.cells_data.values()]
            temperatures = [cell['temp'] for cell in st.session_state.cells_data.values()]
            
            fig_corr = px.scatter(
                x=temperatures,
                y=voltages,
                title="🌡️ Voltage vs Temperature",
                labels={'x': 'Temperature (°C)', 'y': 'Voltage (V)'}
            )
            st.plotly_chart(fig_corr, use_container_width=True)
        
        # Recommendations
        st.markdown("### 💡 AI Recommendations")
        
        recommendations = []
        
        # Check for high temperature cells
        hot_cells = [cell for cell in st.session_state.cells_data.values() if cell['temp'] > 35]
        if hot_cells:
            recommendations.append("🌡️ Consider cooling system - some cells are running hot")
        
        # Check for low health cells
        unhealthy_cells = [cell for cell in st.session_state.cells_data.values() if cell['health'] < 80]
        if unhealthy_cells:
            recommendations.append("🏥 Replace cells with health below 80%")
        
        # Check for high cycle count
        aged_cells = [cell for cell in st.session_state.cells_data.values() if cell['cycles'] > 800]
        if aged_cells:
            recommendations.append("🔄 Monitor high-cycle cells closely")
        
        if not recommendations:
            recommendations.append("✅ All systems operating normally")
        
        for rec in recommendations:
            st.info(rec)
        
    else:
        st.warning("⚠️ No data available for analytics. Please add cells first.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem;'>
    ⚡ Advanced Battery Management System v2.0 | Built with Streamlit & ❤️
</div>
""", unsafe_allow_html=True)
