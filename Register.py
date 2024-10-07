import streamlit as st
from PIL import Image
# Set page configuration
st.set_page_config(page_title="Registration Page", layout="wide")
# Load background image
bg_image = Image.open("C:/Users/SRay5/OneDrive - Rockwell Automation, Inc/Desktop/TaxMaster/Templates/Register.jpg")  # Update with the correct path
# Customize the layout
st.markdown(
   """
<style>
   .stApp {
       background-size: cover;
       background-attachment: fixed;
   }
   .container {
       display: flex;
       justify-content: space-between;
       align-items: flex-start;
       padding: 20px;
   }
   .main {
       background: rgba(255, 255, 255, 0.8);
       padding: 50px;
       border-radius: 15px;
       width: 45%;
       box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
   }
   .image-container {
       width: 25%;
       text-align: center;
   }
   .image-container img {
       max-width: 100%;
       border-radius: 15px;
       box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
   }
   .register-btn {
       width: 100%;
       background-color: #6c63ff;
       color: white;
       font-size: 16px;
       border: none;
       padding: 10px;
       cursor: pointer;
       border-radius: 5px;
       transition: background-color 0.3s ease;
   }
   .register-btn:hover {
       background-color: #564dcc;
   }
   .oval {
       background-color: #DA70D6;
       color: white;
       padding: 10px 20px;
       border-radius: 50px;
       text-align: center;
       display: inline-block;
       font-size: 1.5em;
       margin-bottom: 20px;
       box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
   }
   .form-container {
       display: flex;
       flex-direction: column;
       gap: 15px;
   }
   .form-container input {
       padding: 10px;
       border-radius: 5px;
       border: 1px solid #ccc;
       font-size: 1em;
       max-width: 300px;
   }
</style>
   """,
   unsafe_allow_html=True
)
# Main Registration form
with st.container():
   st.markdown("<div class='container'>", unsafe_allow_html=True)
   # Left side: Registration form
   st.markdown("<div class='main' id='register'><div class='oval'>New User Registration</div>", unsafe_allow_html=True)
   with st.form("registration_form"):
       st.markdown("<div class='form-container'>", unsafe_allow_html=True)
       username = st.text_input("Username")
       name1 = st.text_input("First Name")
       name2 = st.text_input("Last Name")
       email = st.text_input("Email")
       password = st.text_input("Password", type="password")
       confirm_password = st.text_input("Re-enter Password", type="password")
       st.markdown("</div>", unsafe_allow_html=True)
       register = st.form_submit_button("Register")
       if register:
           st.success(f"Welcome {name1}! You have successfully registered.")
   st.markdown("</div>", unsafe_allow_html=True)
   # Right side: Image container
   st.markdown("<div class='image-container'>", unsafe_allow_html=True)
   st.image(bg_image, use_column_width=True)
   st.markdown("</div>", unsafe_allow_html=True)
   st.markdown("</div>", unsafe_allow_html=True)
# Footer section
st.markdown("<div style='text-align: center; margin-top: 10px;'>Already have an account? <a href='#'>Log In</a></div>", unsafe_allow_html=True)