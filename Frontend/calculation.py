import streamlit as st
from PIL import Image
import base64
# Function to calculate tax
st.set_page_config(page_title="Tax Calculation", page_icon="💰")
def calculate_tax(income, deductions):
   taxable_income = income - deductions
   if taxable_income <= 250000:
       tax = 0
   elif taxable_income <= 500000:
       tax = (taxable_income - 250000) * 0.05
   elif taxable_income <= 1000000:
       tax = 12500 + (taxable_income - 500000) * 0.2
   else:
       tax = 112500 + (taxable_income - 1000000) * 0.3
   return tax
# Load favicon image
favicon_path = "C:/Users/SRay5/OneDrive - Rockwell Automation, Inc/Desktop/TaxMaster/Frontend/human_favicon.jpg"
# Encode image to base64
def get_base64_image(image_path):
   with open(image_path, "rb") as image_file:
       return base64.b64encode(image_file.read()).decode()
favicon_base64 = get_base64_image(favicon_path)
# Streamlit app
with st.container():
   st.markdown(
       f"""
<div style='background-color:#D1C4E9; padding:20px; border-radius: 15px; display: flex; align-items: center;'>
<img src='data:image/jpeg;base64,{favicon_base64}' width='50' style='margin-right: 10px;' alt='Favicon'>
<h1 style='color:#673AB7; text-align:center;'>Income Tax Calculator</h1>
</div>
       """,
       unsafe_allow_html=True,
   )
# Adding space between header and content
st.write("")  # This adds a blank line
# User inputs
age = st.number_input("Enter your age:", min_value=0)
income = st.number_input("Enter your annual income:", min_value=0)
deductions = st.number_input("Enter your deductions:", min_value=0)
# Calculate tax
if st.button("Calculate Tax", key="calc"):
   tax = calculate_tax(income, deductions)
   st.write(f"Your calculated tax is: ₹{tax}")
# Footer buttons with effects
st.markdown("---")
st.markdown("### Services For You!")
col1, col2, col3 = st.columns(3)
# Styling for buttons and container
button_style = """
<style>
   /* Style for buttons */
   .stButton button {
       background-color: #D1C4E9;
       color: white;
       padding: 10px;
       border-radius: 5px;
       border: none;
       cursor: pointer;
       transition: background-color 0.3s ease, transform 0.3s ease;
   }
   .stButton button:hover {
       background-color: #B39DDB;
       transform: scale(1.05);
   }
</style>
"""
st.markdown(button_style, unsafe_allow_html=True)
# Columns for buttons
with col1:
   if st.button("Check Tax Schemes"):
       st.write("Details about various tax schemes...")
with col2:
   if st.button("Generate PDF"):
       st.write("PDF generation functionality...")
with col3:
   if st.button("Contact Tax Consultants"):
       st.write("Contact details for tax consultants...")