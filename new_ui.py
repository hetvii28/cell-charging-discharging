import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# --- Page Configuration ---
st.set_page_config(
    page_title="Student Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for dark theme styling ---
st.markdown("""
    <style>
        body {
            background-color: #121212;
            color: #FFFFFF;
        }
        .css-18e3th9 {
            background-color: #121212;
        }
        .css-1d391kg {
            color: #FFFFFF;
        }
        .stButton>button {
            background-color: #1E88E5;
            color: white;
        }
        .stSlider>div {
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

# --- Sidebar ---
st.sidebar.title("Navigation")
st.sidebar.markdown("Select options below:")

selected_subject = st.sidebar.selectbox("Choose Subject", ["Math", "Physics", "Biology"])
show_table = st.sidebar.checkbox("Show Raw Data", value=True)

# --- Header ---
st.title("📊 Student Project Dashboard")
st.markdown("A simple, dark-themed dashboard showcasing interactive charts and data tables for a sample student project.")

# --- Sample Data ---
np.random.seed(42)
data = pd.DataFrame({
    "Student": [f"Student {i}" for i in range(1, 21)],
    "Score": np.random.randint(50, 100, 20),
    "Subject": np.random.choice(["Math", "Physics", "Biology"], 20),
    "Grade": np.random.choice(["A", "B", "C", "D"], 20)
})

filtered_data = data[data["Subject"] == selected_subject]

# --- Metrics ---
average_score = int(filtered_data["Score"].mean())
max_score = filtered_data["Score"].max()
student_count = filtered_data.shape[0]

col1, col2, col3 = st.columns(3)
col1.metric("📈 Avg Score", f"{average_score}")
col2.metric("🏆 Max Score", f"{max_score}")
col3.metric("👥 Students", f"{student_count}")

# --- Chart ---
fig = px.bar(filtered_data, x="Student", y="Score", color="Grade",
             title=f"{selected_subject} Scores by Student",
             template="plotly_dark")
st.plotly_chart(fig, use_container_width=True)

# --- Data Table ---
if show_table:
    st.subheader("Raw Data")
    st.dataframe(filtered_data.style.set_properties(**{'background-color': '#2e2e2e', 'color': 'white'}))

# --- Footer ---
st.markdown("---")
st.markdown("Created by a Student | Powered by Streamlit | [GitHub Repo](#)")
