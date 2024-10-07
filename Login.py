import streamlit as st
# Set the page configuration
st.set_page_config(page_title="Login Page", page_icon="🔐")
# Create the login page layout
def login_page():
   st.title("Log In")
   # User inputs
   name = st.text_input("Your Name", "")
   password = st.text_input("Password", type="password")
   forget_password = st.markdown("Forgot Password?")
   # Remember me checkbox
   remember_me = st.checkbox("Remember me")
   # Log in button
   if st.button("Log in"):
       if name and password:
           st.success(f"Welcome, {name}!")
       else:
           st.error("Please provide both name and password.")
   # Create account link
   st.markdown("Not an Existing User? [Create an account](#)")
#    # Social login options
#    st.markdown("---")
#    st.markdown("Or login with:")
#    col1, col2, col3 = st.columns(3)
#    with col1:
#        st.button("Facebook")
#    with col2:
#        st.button("Twitter")
#    with col3:
#        st.button("Google")
# Call the login page function
login_page()