import streamlit as st

# Function to calculate tax
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

# Streamlit app
st.title("Income Tax Calculator")

# User inputs
age = st.number_input("Enter your age:", min_value=0)
income = st.number_input("Enter your annual income:", min_value=0)
deductions = st.number_input("Enter your deductions:", min_value=0)

# Calculate tax
if st.button("Calculate Tax"):
    tax = calculate_tax(income, deductions)
    st.write(f"Your calculated tax is: ₹{tax}")

# Footer buttons
st.markdown("---")
st.markdown("### Services For You!")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Tax Schemes"):
        st.write("Details about various tax schemes...")

with col2:
    if st.button("Generate PDF"):
        st.write("PDF generation functionality...")

with col3:
    if st.button("Contact Tax Consultants"):
        st.write("Contact details for tax consultants...")


