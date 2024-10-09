import streamlit as st
import pandas as pd

# Sample data for schedules
data = {
    "Date": ["2024-01-10", "2024-01-15", "2023-12-20", "2023-11-25"],
    "Time": ["10:00 AM", "02:00 PM", "11:00 AM", "03:00 PM"],
    "Consultant": ["Aarav Sharma", "Priya Patel", "Rohan Gupta", "Ananya Singh"],
    "Status": ["Upcoming", "Upcoming", "Completed", "Completed"]
}

# Create a DataFrame
df = pd.DataFrame(data)

# Streamlit app
st.set_page_config(page_title="User Schedules", page_icon="📅", layout="wide")
st.title("📅 Your Schedules")

# Add some styling
st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
    }
    .stTable {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    .stTable table {
        width: 100%;
    }
    .stTable th, .stTable td {
        padding: 10px;
        text-align: left;
    }
    .stTable th {
        background-color: #CF9FFF;
        color: white;
    }
    .stTable tr:nth-child(even) {
        background-color: #f2f2f2;
    }
    .stTable tr:hover {
        background-color: #ddd;
    }
    </style>
    """, unsafe_allow_html=True)

# Filter upcoming and previous schedules
upcoming_schedules = df[df["Status"] == "Upcoming"]
previous_schedules = df[df["Status"] == "Completed"]

# Display upcoming schedules
st.write("### Upcoming Schedules")
st.table(upcoming_schedules)

# Display previous schedules
st.write("### Previous Schedules")
st.table(previous_schedules)

# Add a footer
st.markdown("""
    <hr>
    <div style='text-align: center;'>
        <small>© 2024 User Schedules. All rights reserved.</small>
    </div>
    """, unsafe_allow_html=True)
