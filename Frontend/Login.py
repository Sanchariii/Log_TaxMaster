import streamlit as st
# Set the page configuration
st.set_page_config(page_title="Login Page", page_icon="🔐")
# Add custom CSS
st.markdown("""
<style>
   /* Container for header */
   .header-container {
       background-color: #E6E6FA; /* Light violet color */
       padding: 20px;
       border-radius: 10px;
       margin-bottom: 20px;
       text-align: center;
       box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Subtle shadow effect */
   }
   /* Style for title */
   .header-container h1 {
       color: #2e3b4e; /* Darker blue for the title */
       font-family: 'Arial', sans-serif;
       font-size: 32px;
       font-weight: bold;
       margin: 0;
   }
   /* Container for forgot password */
   .forgot-password-container {
       text-align: right;
       margin-top: -10px;
       margin-bottom: 20px;
   }
   /* Style for footer container */
   .footer-container {
       background-color: #f7f9fc; /* Soft blue color */
       padding: 20px;
       border-radius: 10px;
       margin-top: 20px;
       text-align: center;
       box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Shadow effect for footer as well */
   }
   /* Style for input boxes */
   .stTextInput > div > input {
       border: 1px solid #ccc;
       padding: 10px;
       font-size: 16px;
       border-radius: 5px;
       width: 100%;
       margin-bottom: 10px;
   }
   /* Style for buttons */
   div.stButton > button {
       background-color: #4CAF50;
       color: white;
       padding: 10px 20px;
       font-size: 16px;
       border: none;
       border-radius: 5px;
       cursor: pointer;
   }
   div.stButton > button:hover {
       background-color: #45a049;
   }
   /* Style for checkboxes */
   .stCheckbox {
       margin-top: 10px;
       font-size: 16px;
   }
   /* Custom link style */
   a {
       color: #007BFF;
       text-decoration: none;
   }
   a:hover {
       text-decoration: underline;
   }
</style>
   """, unsafe_allow_html=True)
# Create the login page layout
def login_page():
   # Header container
   st.markdown('<div class="header-container"><h1>Log In</h1></div>', unsafe_allow_html=True)
   # User inputs
   name = st.text_input("Your Name", "")
   password = st.text_input("Password", type="password")
   # Forgot Password container (placed right below the password input)
   st.markdown("""
<div class="forgot-password-container">
<a href="#">Forgot Password?</a>
</div>
   """, unsafe_allow_html=True)
   # Remember me checkbox
   remember_me = st.checkbox("Remember me")
   # Log in button
   if st.button("Log in"):
       if name and password:
           st.success(f"Welcome, {name}!")
       else:
           st.error("Please provide both name and password.")
   # Footer container
   st.markdown("""
<div class="footer-container">
<p>Not an Existing User? <a href="#">Create an account</a></p>
</div>
   """, unsafe_allow_html=True)
# Call the login page function
login_page()