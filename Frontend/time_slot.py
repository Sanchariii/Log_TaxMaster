import streamlit as st
import pandas as pd

# Sample data for tax consultants
data = {
    "Name": ["Aarav Sharma", "Priya Patel", "Rohan Gupta", "Ananya Singh", "Vikram Rao"],
    "Years of Experience": [5, 10, 3, 8, 12],
    "Gender": ["Male", "Female", "Male", "Female", "Male"]
}

# Create a DataFrame
df = pd.DataFrame(data)

# Streamlit app
st.set_page_config(page_title="Tax Consultant Booking", page_icon="📅", layout="wide")
st.title("📅 Get an Appointment with Your Desired Tax Consultant")

# Add some styling
st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
    }
    .stButton button {
        background-color: #D8BFD8;
        color: white;
        border: none;
        padding: 10px 24px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 12px;
    }
    .stButton button:hover {
        background-color: #DA70D6;
    }
    </style>
    """, unsafe_allow_html=True)

# Display the table with column names and a button for each consultant
st.write("### Tax Consultants")
for index, row in df.iterrows():
    col1, col2, col3, col4 = st.columns([3, 3, 2, 2])
    if index == 0:
        col1.write("**Name**")
        col2.write("**Years of Experience**")
        col3.write("**Gender**")
        col4.write("**Action**")
    col1.write(row["Name"])
    col2.write(row["Years of Experience"])
    col3.write(row["Gender"])
    if col4.button("Book Appointment", key=index):
        st.session_state['selected_consultant'] = row['Name']
        st.session_state['booking'] = True

# Booking section
if 'booking' in st.session_state and st.session_state['booking']:
    st.write(f"### Booking an appointment with {st.session_state['selected_consultant']}")
    
    # Date selection
    date = st.date_input("Select your preferred date")
    
    # Slot selection
    slot = st.selectbox("Select your preferred slot", ["Morning", "Afternoon", "Night"])
    
    if st.button("Submit Request"):
        st.info(f"Your request for an appointment with {st.session_state['selected_consultant']} on {date} during {slot} slot has been submitted. TaxMaster will call and try to schedule an appointment in your preferred slot or the next available slot.")
        del st.session_state['booking']

# Add a footer
st.markdown("""
    <hr>
    <div style='text-align: center;'>
        <small>© 2024 Tax Consultant Booking. All rights reserved.</small>
    </div>
    """, unsafe_allow_html=True)
