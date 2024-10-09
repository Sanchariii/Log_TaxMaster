import streamlit as st
import pandas as pd

# Sample data for appointment requests
data = {
    "Client Name": ["Sanchari Ray", "Hydra Ray", "Pritam Sharma"],
    "Date": ["2024-01-10", "2024-01-15", "2024-01-20"],
    "Time Slot": ["Morning", "Afternoon", "Night"],
    "Status": ["Pending", "Pending", "Pending"]
}

# Create a DataFrame
df = pd.DataFrame(data)

# Streamlit app
st.set_page_config(page_title="Tax Advisor Dashboard", page_icon="📅", layout="wide")
st.title("📅 Tax Advisor Dashboard")

# Add some styling
st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
    }
    .client-box {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    .button-container {
        display: flex;
        justify-content: space-between;
    }
    .pretty-button {
        background-color: #DA70D6;
        border: none;
        color: white;
        padding: 15px 32px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 12px;
    }
    .pretty-button:hover {
        background-color: #45a049; /* Darker green */
    }
    </style>
    """, unsafe_allow_html=True)

# Display appointment requests
st.write("### Appointment Requests")
for index, row in df.iterrows():
    with st.container():
        st.markdown(f"""
            <div class="client-box">
                <p><strong>Client Name:</strong> {row["Client Name"]}</p>
                <p><strong>Date:</strong> {row["Date"]}</p>
                <p><strong>Time Slot:</strong> {row["Time Slot"]}</p>
                <p><strong>Status:</strong> {row["Status"]}</p>
                <div class="button-container">
                    <button class="pretty-button" onclick="window.location.href='?accept_{index}'">Accept</button>
                    <button class="pretty-button" onclick="window.location.href='?decline_{index}'">Decline</button>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        if f"accept_{index}" in st.query_params:
            df.at[index, "Status"] = "Accepted"
            st.success(f"Appointment with {row['Client Name']} on {row['Date']} during {row['Time Slot']} slot has been accepted.")
        
        if f"decline_{index}" in st.query_params:
            df.at[index, "Status"] = "Declined"
            st.warning(f"Appointment with {row['Client Name']} on {row['Date']} during {row['Time Slot']} slot has been declined.")

# Add a footer
st.markdown("""
    <hr>
    <div style='text-align: center;'>
        <small>© 2024 Tax Advisor Dashboard. All rights reserved.</small>
    </div>
    """, unsafe_allow_html=True)
