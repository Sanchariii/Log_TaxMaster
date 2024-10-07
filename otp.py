import streamlit as st
# Set the page title
st.title("Verification Code")
# Description
st.write("We have sent the verification code to your email address")
# Create 4 empty placeholders for each digit
cols = st.columns(6)
otp = ""
# Create input fields for each digit (this simulates the boxes in your screenshot)
for i, col in enumerate(cols):
   with col:
       digit = st.text_input(label=f"Digit {i+1}", max_chars=1, key=f"digit{i+1}")
       otp += digit if digit.isdigit() else ""
# Create a confirm button
if st.button("Confirm"):
   if len(otp) == 6:  # Ensure the user entered a 4-digit code
       st.success(f"OTP {otp} is confirmed!")
   else:
       st.error("Please enter a valid 6-digit OTP")


